import logging
import select
import subprocess
import sys
from subprocess import PIPE, Popen
from threading import Lock
from typing import List, Optional, Union

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
        options: Optional[List[str]] = None,
        senter: Optional[Processor] = None,
        skip_sanity_check: bool = False,
        debug: bool = False,
    ) -> None:
        self.executable = executable  #: Juman++ のパス．
        self.options: List[str] = options or []  #: Juman++ のオプション．
        self.senter = senter
        self.debug: bool = debug  #: True ならデバッグモード．
        self._lock = Lock()
        self._proc: Optional[Popen] = None
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
            if skip_sanity_check is False:
                _ = self.apply(Sentence.from_raw_text(""))
        except Exception as e:
            logger.warning(f"failed to start Juman++: {e}")

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        return f"{self.__class__.__name__}({arg_string})"

    def __del__(self) -> None:
        if self._proc is not None:
            self._proc.kill()

    def is_available(self) -> bool:
        """Jumanpp が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に Jumanpp を適用する．

        Args:
            document: 文書．

        .. note::
            文分割がまだなら，先に初期化時に設定した senter で文分割する．
            未設定なら RegexSenter で文分割する．
        """
        if not self.is_available():
            raise RuntimeError("Juman++ is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None

        if isinstance(document, str):
            document = Document(document)

        if document.is_senter_required() is True:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document)

        sentences: List[Sentence] = []
        for sentence in document.sentences:
            sentences.append(self.apply_to_sentence(sentence))
        return Document.from_sentences(sentences)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に Jumanpp を適用する．

        Args:
            sentence: 文．
        """
        if not self.is_available():
            raise RuntimeError("Juman++ is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None
        assert self._proc.stderr is not None

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        with self._lock:
            self._proc.stdin.write(sentence.to_raw_text())
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
                    stderr_text += self._proc.stderr.readline()
                if self.debug is True and stderr_text.strip() != "":
                    print(stderr_text.strip(), file=sys.stderr)

            return Sentence.from_jumanpp(stdout_text)

    def get_version(self) -> str:
        """Juman++ のバージョンを返す．"""
        if not self.is_available():
            raise RuntimeError("Juman++ is not available.")
        p = subprocess.run(self.version_command, capture_output=True, encoding="utf-8")
        return p.stdout.strip()

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        return [self.executable] + self.options

    @property
    def version_command(self) -> List[str]:
        """バージョンを確認するコマンド．"""
        return [self.executable, "--version"]
