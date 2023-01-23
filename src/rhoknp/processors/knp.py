import logging
from subprocess import PIPE, Popen
from threading import Lock
from typing import List, Optional, Union

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
    ) -> None:
        self.executable = executable  #: KNP のパス．
        self.options = options  #: KNP のオプション．
        self.senter = senter
        self.jumanpp = jumanpp
        self._proc: Optional[Popen] = None
        try:
            self._proc = Popen(self.run_command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
        except Exception as e:
            logger.warning(f"failed to start KNP: {e}")
        self._lock = Lock()

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options is not None:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        if self.jumanpp is not None:
            arg_string += f", jumanpp={repr(self.jumanpp)}"
        return f"{self.__class__.__name__}({arg_string})"

    def is_available(self) -> bool:
        """KNP が利用可能であれば True を返す．"""
        return self._proc is not None and self._proc.poll() is None

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に KNP を適用する．

        Args:
            document: 文書．

        .. note::
            文分割がまだなら，先に初期化時に設定した senter で文分割する．
            未設定なら RegexSenter で文分割する．
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if not self.is_available():
            raise RuntimeError("KNP is not available.")
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
                logger.debug(self.senter)
            document = self.senter.apply_to_document(document)

        if document.need_jumanpp is True:
            logger.debug("document needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info("jumanpp is not specified; use Jumanpp")
                self.jumanpp = Jumanpp()
                logger.debug(self.jumanpp)
            document = self.jumanpp.apply_to_document(document)

        with self._lock:
            knp_text = ""
            for sentence in document.sentences:
                self._proc.stdin.write(sentence.to_jumanpp() if sentence.need_knp is True else sentence.to_knp())
                self._proc.stdin.flush()
                while self.is_available():
                    line = self._proc.stdout.readline()
                    knp_text += line
                    if line.strip() == Sentence.EOS:
                        break
            return Document.from_knp(knp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に KNP を適用する．

        Args:
            sentence: 文．

        .. note::
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if not self.is_available():
            raise RuntimeError("KNP is not available.")
        assert self._proc is not None
        assert self._proc.stdin is not None
        assert self._proc.stdout is not None

        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        if sentence.need_jumanpp is True:
            logger.debug("sentence needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info("jumanpp is not specified when initializing KNP: use Jumanpp with no option")
                self.jumanpp = Jumanpp()
            sentence = self.jumanpp.apply_to_sentence(sentence)

        with self._lock:
            self._proc.stdin.write(sentence.to_jumanpp() if sentence.need_knp is True else sentence.to_knp())
            self._proc.stdin.flush()
            knp_text = ""
            while self.is_available():
                line = self._proc.stdout.readline()
                knp_text += line
                if line.strip() == Sentence.EOS:
                    break
            return Sentence.from_knp(knp_text)

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        command = [self.executable]
        if self.options:
            command += self.options
        else:
            command += ["-tab"]
        return command
