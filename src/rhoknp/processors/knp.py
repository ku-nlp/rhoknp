import logging
from subprocess import PIPE, Popen, run
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

    Example::

        from rhoknp import KNP

        knp = KNP()
        sentence = knp.apply("電気抵抗率は、どんな材料が電気を通しにくいかを比較するために、用いられる物性値である。")
    """

    def __init__(
        self,
        executable: str = "knp",
        options: Optional[List[str]] = None,
        senter: Optional[Processor] = None,
        jumanpp: Optional[Processor] = None,
    ):
        self.executable = executable
        self.options = options
        self.senter = senter
        self.jumanpp = jumanpp

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options is not None:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        if self.jumanpp is not None:
            arg_string += f", jumanpp={repr(self.jumanpp)}"
        return f"{self.__class__.__name__}({arg_string})"

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
        if isinstance(document, str):
            document = Document(document)

        if document.need_senter:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
                logger.debug(self.senter)
            document = self.senter.apply_to_document(document)

        if document.need_jumanpp:
            logger.debug("document needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info("jumanpp is not specified; use Jumanpp")
                self.jumanpp = Jumanpp()
                logger.debug(self.jumanpp)
            document = self.jumanpp.apply_to_document(document)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            knp_text, _ = p.communicate(input=document.to_jumanpp() if document.need_knp else document.to_knp())
        return Document.from_knp(knp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に KNP を適用する．

        Args:
            sentence: 文．

        .. note::
            形態素解析がまだなら，先に初期化時に設定した jumanpp で形態素解析する．
            未設定なら Jumanpp （オプションなし）で形態素解析する．
        """
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        if sentence.need_jumanpp:
            logger.debug("sentence needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info("jumanpp is not specified when initializing KNP: use Jumanpp with no option")
                self.jumanpp = Jumanpp()
            sentence = self.jumanpp.apply_to_sentence(sentence)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            knp_text, _ = p.communicate(input=sentence.to_jumanpp() if sentence.need_knp else sentence.to_knp())
        return Sentence.from_knp(knp_text)

    def is_available(self) -> bool:
        """KNP が利用可能であれば True を返す．"""
        try:
            p = run(self.version_command, stdout=PIPE, stdin=PIPE, encoding="utf-8")
            logger.info(p.stdout.strip())
            return True
        except Exception as e:
            logger.warning(e)
            return False

    @property
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        command = [self.executable]
        if self.options:
            command += self.options
        else:
            command += ["-tab"]
        return command

    @property
    def version_command(self) -> List[str]:
        """バージョン確認時に実行するコマンド．"""
        return [self.executable, "-v"]
