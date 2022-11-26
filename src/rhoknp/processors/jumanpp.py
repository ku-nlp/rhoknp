import logging
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
    ) -> None:
        self.executable = executable  #: Juman++ のパス．
        self.options = options  #: Juman++ のオプション．
        self.senter = senter
        self._proc: Optional[Popen] = None
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
        except Exception as e:
            logger.warning(f"failed to start Juman++: {e}")
        self._lock = Lock()

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options is not None:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        return f"{self.__class__.__name__}({arg_string})"

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

        if document.need_senter is True:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document)

        with self._lock:
            jumanpp_text = ""
            for sentence in document.sentences:
                self._proc.stdin.write(sentence.to_raw_text())
                self._proc.stdin.flush()
                while self.is_available():
                    line = self._proc.stdout.readline()
                    jumanpp_text += line
                    if line.strip() == Sentence.EOS:
                        break
            return Document.from_jumanpp(jumanpp_text)

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

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        with self._lock:
            self._proc.stdin.write(sentence.to_raw_text())
            self._proc.stdin.flush()
            jumanpp_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                jumanpp_text += line
                if line.strip() == Sentence.EOS:
                    break
            return Sentence.from_jumanpp(jumanpp_text)

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        command = [self.executable]
        if self.options:
            command += self.options
        return command
