import logging
import select
import subprocess
import threading
import time
from subprocess import PIPE, Popen
from threading import Lock
from typing import Optional, Union

try:
    from typing import override  # type: ignore[attr-defined]
except ImportError:
    from typing_extensions import override

from rhoknp.processors.processor import Processor
from rhoknp.processors.senter import RegexSenter
from rhoknp.units import Document, Sentence

logger = logging.getLogger(__name__)


class Jumanpp(Processor):
    """Jumanpp クラス．

    Args:
        executable: Juman++ のパス．
        options: Juman++ のオプション．
        senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割する．
            未設定なら RegexSenter を使って文分割する．
        skip_sanity_check: True なら，Juman++ の起動時に sanity check をスキップする．

    Example:
        >>> from rhoknp import Jumanpp
        >>> jumanpp = Jumanpp()
        >>> document = jumanpp.apply("電気抵抗率は電気の通しにくさを表す物性値である。")

    .. note::
        使用するには `Juman++ <https://github.com/ku-nlp/jumanpp>`_ がインストールされている必要がある．
    """

    def __init__(
        self,
        executable: str = "jumanpp",
        options: Optional[list[str]] = None,
        senter: Optional[Processor] = None,
        skip_sanity_check: bool = False,
    ) -> None:
        self.executable = executable  #: Juman++ のパス．
        self.options: list[str] = options or []  #: Juman++ のオプション．
        self.senter = senter
        self._lock = Lock()
        self._proc: Optional[Popen] = None
        self.start_process(skip_sanity_check)

    def __repr__(self) -> str:
        arg_string = f"executable={self.executable!r}"
        if self.options:
            arg_string += f", options={self.options!r}"
        if self.senter is not None:
            arg_string += f", senter={self.senter!r}"
        return f"{self.__class__.__name__}({arg_string})"

    def __del__(self) -> None:
        try:
            if self._proc is not None:
                self._proc.terminate()
        except AttributeError:  # pragma: no cover
            # for free-threaded Python interpreters
            pass  # pragma: no cover

    def start_process(self, skip_sanity_check: bool = False) -> None:
        """Juman++ を開始する．

        .. note::
            Juman++ が既に起動している場合は再起動する．
            skip_sanity_check: True なら，Juman++ の起動時に sanity check をスキップする．
        """
        if self._proc is not None:
            self._proc.terminate()
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
            if skip_sanity_check is False:
                _ = self.apply(Sentence.from_raw_text(""))
        except Exception as e:
            logger.warning(f"failed to start Juman++: {e}")

    def is_available(self) -> bool:
        """Jumanpp が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    @override
    def apply_to_document(self, document: Union[Document, str], timeout: int = 10) -> Document:
        """文書に Jumanpp を適用する．

        Args:
            document: 文書．
            timeout: 最大処理時間．

        .. note::
            文分割がまだなら，先に初期化時に設定した senter で文分割する．
            未設定なら RegexSenter で文分割する．
        """
        if not self.is_available():
            raise RuntimeError("Juman++ is not available.")

        start = time.time()

        if isinstance(document, str):
            document = Document(document)
        doc_id = document.doc_id

        if document.is_senter_required():
            if self.senter is None:
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document, timeout=timeout - int(time.time() - start))

        sentences: list[Sentence] = []
        for sentence in document.sentences:
            sentences.append(self.apply_to_sentence(sentence, timeout=timeout - int(time.time() - start)))
        ret = Document.from_sentences(sentences)
        if doc_id != "":
            ret.doc_id = doc_id
            for sentence in ret.sentences:
                sentence.doc_id = doc_id
        return ret

    @override
    def apply_to_sentence(self, sentence: Union[Sentence, str], timeout: int = 10) -> Sentence:
        """文に Jumanpp を適用する．

        Args:
            sentence: 文．
            timeout: 最大処理時間．
        """
        if not self.is_available():
            raise RuntimeError("Juman++ is not available.")

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        stdout_text: str = ""

        def worker() -> None:
            nonlocal stdout_text
            assert self._proc is not None
            assert self._proc.stdin is not None
            assert self._proc.stdout is not None
            assert self._proc.stderr is not None

            self._proc.stdin.write(sentence.to_raw_text())
            self._proc.stdin.flush()

            stdout_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                stdout_text += line
                if line.strip() == Sentence.EOS:
                    break

                # Non-blocking read from stderr
                stderr_text: str = ""
                while self._proc.stderr in select.select([self._proc.stderr], [], [], 0)[0]:
                    line = self._proc.stderr.readline()
                    if line.strip() == "":
                        break
                    stderr_text += line
                if stderr_text.strip() != "":
                    logger.debug(stderr_text.strip())

        with self._lock:
            thread = threading.Thread(target=worker, daemon=True)
            thread.start()
            thread.join(timeout)

            if thread.is_alive():
                self.start_process(skip_sanity_check=True)
                raise TimeoutError(f"Operation timed out after {timeout} seconds.")

            if not self.is_available():
                self.start_process(skip_sanity_check=True)
                raise RuntimeError("Juman++ exited unexpectedly.")

        ret = Sentence.from_jumanpp(stdout_text)
        if sentence.text and not ret.text:
            raise RuntimeError(f"Juman++ returned empty result for input: '{sentence.text}'")

        return ret

    def get_version(self) -> str:
        """Juman++ のバージョンを返す．"""
        if not self.is_available():
            raise RuntimeError("Juman++ is not available.")
        p = subprocess.run(self.version_command, capture_output=True, encoding="utf-8", check=True)
        return p.stdout.strip()

    @property
    def run_command(self) -> list[str]:
        """解析時に実行するコマンド．"""
        return [self.executable, *self.options]

    @property
    def version_command(self) -> list[str]:
        """バージョンを確認するコマンド．"""
        return [self.executable, "--version"]
