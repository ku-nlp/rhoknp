from logging import getLogger
from subprocess import PIPE, Popen, run
from typing import Optional, Union

from rhoknp.units import Document, Sentence

from .processor import Processor
from .senter import RegexSenter

logger = getLogger(__file__)


class Jumanpp(Processor):
    def __init__(
        self,
        executable: str = "jumanpp",
        options: Optional[list[str]] = None,
        senter: Optional[Processor] = None,
    ):
        """Jumanppクラスのインスタンスを初期化．

        Args:
            executable: Juman++ のパス．
            options: Juman++ のオプション．
            senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割を行う．
                未設定の場合， RegexSenter が適用される．
        """
        self.executable = executable
        self.options = options

        self.senter = senter

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

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            jumanpp_text, _ = p.communicate(input=document.to_plain())
        return Document.from_jumanpp(jumanpp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            jumanpp_text, _ = p.communicate(input=sentence.to_plain())
        return Sentence.from_jumanpp(jumanpp_text)

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
        return f"{self.__class__.__name__}({arg_string})"
