from logging import getLogger
from subprocess import PIPE, Popen, run
from typing import Optional, Union

from rhoknp.units import Document, Sentence

from .jumanpp import Jumanpp
from .processor import Processor
from .senter import RegexSenter

logger = getLogger(__file__)


class KNP(Processor):
    def __init__(
        self,
        executable: str = "knp",
        options: Optional[list[str]] = None,
        senter: Optional[Processor] = None,
        jumanpp: Optional[Processor] = None,
    ):
        """KNPクラスのインスタンスを初期化．

        Args:
            executable: KNP のパス．
            options: KNP のオプション．
            senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割を行う．
                未設定の場合， RegexSenter が適用される．
            jumanpp: Jumanpp のインスタンス．形態素解析がまだなら，先にこのインスタンスを用いて形態素解析を行う．
                未設定の場合， Jumanpp （オプションなし）が適用される．
        """
        self.executable = executable
        self.options = options
        self.senter = senter
        self.jumanpp = jumanpp

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        if isinstance(document, str):
            document = Document(document)

        if document.need_senter:
            logger.debug("document needs to be split into sentences")
            if self.senter is None:
                logger.debug(
                    "senter is not specified when initializing KNP: use RegexSenter with no option"
                )
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document)

        if document.need_jumanpp:
            logger.debug("document needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info(
                    "jumanpp is not specified when initializing KNP: use Jumanpp with no option"
                )
                self.jumanpp = Jumanpp()
            document = self.jumanpp.apply_to_document(document)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            knp_text, _ = p.communicate(input=document.to_jumanpp())
        return Document.from_knp(knp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        if sentence.need_jumanpp:
            logger.debug("sentence needs to be processed by Juman++")
            if self.jumanpp is None:
                logger.info(
                    "jumanpp is not specified when initializing KNP: use Jumanpp with no option"
                )
                self.jumanpp = Jumanpp()
            sentence = self.jumanpp.apply_to_sentence(sentence)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            knp_text, _ = p.communicate(input=sentence.to_jumanpp())
        return Sentence.from_knp(knp_text)

    def is_available(self) -> bool:
        try:
            p = run(self.version_command, stdout=PIPE, stdin=PIPE, encoding="utf-8")
            logger.info(p.stdout.strip())
            return True
        except Exception as e:
            logger.warning(e)
            return False

    @property
    def run_command(self) -> list[str]:
        command = [self.executable]
        if self.options:
            command += self.options
        else:
            command += ["-tab"]
        return command

    @property
    def version_command(self) -> list[str]:
        return [self.executable, "-v"]

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options is not None:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        if self.jumanpp is not None:
            arg_string += f", jumanpp={repr(self.jumanpp)}"
        return f"{self.__class__.__name__}({arg_string})"
