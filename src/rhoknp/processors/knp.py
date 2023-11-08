import logging
import select
import subprocess
import threading
import time
from subprocess import PIPE, Popen
from threading import Lock
from typing import List, Optional, Union

try:
    from typing import override  # type: ignore
except ImportError:
    from typing_extensions import override

from rhoknp.processors.jumanpp import Jumanpp
from rhoknp.processors.processor import Processor
from rhoknp.processors.senter import RegexSenter
from rhoknp.units import Document, Sentence

logger = logging.getLogger(__name__)


class KNP(Processor):
    """KNP クラス．

    Args:
        executable: KNP のパス．
        options: KNP のオプション．
        senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割する．
            未設定なら RegexSenter を使って文分割する．
        jumanpp: Jumanpp のインスタンス．形態素解析がまだなら，先にこのインスタンスを用いて形態素解析する．
            未設定なら Jumanpp （オプションなし）を使って形態素解析する．
        skip_sanity_check: True なら，KNP の起動時に sanity check をスキップする．

    Example:
        >>> from rhoknp import KNP
        >>> knp = KNP()
        >>> document = knp.apply("電気抵抗率は電気の通しにくさを表す物性値である。")

    .. note::
        使用するには `KNP <https://github.com/ku-nlp/knp>`_ がインストールされている必要がある．
    """

    def __init__(
        self,
        executable: str = "knp",
        options: Optional[List[str]] = None,
        senter: Optional[Processor] = None,
        jumanpp: Optional[Processor] = None,
        skip_sanity_check: bool = False,
    ) -> None:
        self.executable = executable  #: KNP のパス．
        self.options = options or ["-tab"]  #: KNP のオプション．
        self.senter = senter
        self.jumanpp = jumanpp
        self._lock = Lock()
        self._proc: Optional[Popen] = None
        if "-tab" not in self.options:
            raise ValueError("`-tab` option is required when you use KNP.")
        self.start_process(skip_sanity_check)

    def __repr__(self) -> str:
        arg_string = f"executable={self.executable!r}"
        if self.options:
            arg_string += f", options={self.options!r}"
        if self.senter is not None:
            arg_string += f", senter={self.senter!r}"
        if self.jumanpp is not None:
            arg_string += f", jumanpp={self.jumanpp!r}"
        return f"{self.__class__.__name__}({arg_string})"

    def __del__(self) -> None:
        if self._proc is not None:
            self._proc.terminate()

    def start_process(self, skip_sanity_check: bool = False) -> None:
        """KNP を起動する．

        .. note::
            KNP がすでに起動している場合は再起動する．
            skip_sanity_check: True なら，KNP の起動時に sanity check をスキップする．
        """
        if self._proc is not None:
            self._proc.terminate()
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
            if skip_sanity_check is False:
                _ = self.apply(Sentence.from_jumanpp("EOS"))
        except Exception as e:
            logger.warning(f"failed to start KNP: {e}")

    def is_available(self) -> bool:
        """KNP が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    @override
    def apply_to_document(self, document: Union[Document, str], timeout: int = 10) -> Document:
        """文書に KNP を適用する．

        Args:
            document: 文書．
            timeout: 最大処理時間．

        .. note::
            文分割がまだなら，先に初期化時に設定した senter で文分割する．
            未設定なら RegexSenter で文分割する．
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if not self.is_available():
            raise RuntimeError("KNP is not available.")

        start: float = time.time()

        if isinstance(document, str):
            document = Document(document)
        doc_id = document.doc_id

        if document.is_senter_required():
            if self.senter is None:
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document, timeout=timeout - int(time.time() - start))

        sentences: List[Sentence] = []
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
        """文に KNP を適用する．

        Args:
            sentence: 文．
            timeout: 最大処理時間．

        .. note::
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if self.is_available() is False:
            raise RuntimeError("KNP is not available.")

        start: float = time.time()

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        if sentence.is_jumanpp_required():
            if self.jumanpp is None:
                logger.debug("jumanpp is not specified when initializing KNP: use Jumanpp with no option")
                self.jumanpp = Jumanpp()
            sentence = self.jumanpp.apply_to_sentence(sentence, timeout=timeout - int(time.time() - start))

        stdout_text: str = ""
        done_event: threading.Event = threading.Event()

        def worker() -> None:
            nonlocal stdout_text
            assert self._proc is not None
            assert self._proc.stdin is not None
            assert self._proc.stdout is not None
            assert self._proc.stderr is not None

            if sentence.is_knp_required():
                self._proc.stdin.write(sentence.to_jumanpp())
            else:
                self._proc.stdin.write(sentence.to_knp())
            self._proc.stdin.flush()

            stdout_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                stdout_text += line
                if line.strip() == Sentence.EOS:
                    break

                # Non-blocking read from stderr
                stderr_text = ""
                while self._proc.stderr in select.select([self._proc.stderr], [], [], 0)[0]:
                    line = self._proc.stderr.readline()
                    if line.strip() == "":
                        break
                    stderr_text += line
                if stderr_text.strip() != "":
                    logger.debug(stderr_text.strip())
            done_event.set()

        with self._lock:
            thread = threading.Thread(target=worker)
            thread.start()
            done_event.wait(timeout - int(time.time() - start))

            if thread.is_alive():
                thread.join()
                self.start_process(skip_sanity_check=True)
                raise TimeoutError("Operation timed out.")

            if not self.is_available():
                self.start_process(skip_sanity_check=True)
                raise RuntimeError("KNP exited unexpectedly.")

        ret = Sentence.from_knp(stdout_text)
        if sentence.text and not ret.text:
            raise RuntimeError(f"KNP returned empty result for input: '{sentence.text}'")

        return ret

    def get_version(self) -> str:
        """Juman++ のバージョンを返す．"""
        if not self.is_available():
            raise RuntimeError("KNP is not available.")
        p = subprocess.run(self.version_command, capture_output=True, encoding="utf-8", check=True)
        return p.stderr.strip()

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        return [self.executable, *self.options]

    @property
    def version_command(self) -> List[str]:
        """バージョンを確認するコマンド．"""
        return [self.executable, "-v"]
