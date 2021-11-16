from logging import getLogger
from subprocess import PIPE, Popen, run
from typing import Optional, Union

from rhoknp.processors.processor import Processor
from rhoknp.processors.senter import RegexSenter
from rhoknp.units import Document, Sentence

logger = getLogger(__file__)


class Jumanpp(Processor):
    """Jumanpp クラス．

    Args:
        executable: Juman++ のパス．
        options: Juman++ のオプション．
        senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割する．
            未設定なら RegexSenter を使って文分割する．

    Example::

        from rhoknp import Jumanpp

        jumanpp = Jumanpp()
        sentence = jumanpp.apply("電気抵抗率は、どんな材料が電気を通しにくいかを比較するために、用いられる物性値である。")
    """

    def __init__(
        self,
        executable: str = "jumanpp",
        options: Optional[list[str]] = None,
        senter: Optional[Processor] = None,
    ):
        self.executable = executable
        self.options = options

        self.senter = senter

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options is not None:
            arg_string += f", options={repr(self.options)}"
        if self.senter is not None:
            arg_string += f", senter={repr(self.senter)}"
        return f"{self.__class__.__name__}({arg_string})"

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に Jumanpp を適用する．

        Args:
            document: 文書．

        .. note::
            文分割がまだなら，先に初期化時に設定した senter で文分割する．
            未設定なら RegexSenter で文分割する．
        """
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
        """文に Jumanpp を適用する．

        Args:
            sentence: 文．
        """
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            jumanpp_text, _ = p.communicate(input=sentence.to_plain())
        return Sentence.from_jumanpp(jumanpp_text)

    def is_available(self) -> bool:
        """Jumanpp が利用可能であれば True を返す．"""
        try:
            p = run(self.version_command, stdout=PIPE, stdin=PIPE, encoding="utf-8")
            logger.info(p.stdout.strip())
            return True
        except Exception as e:
            logger.warning(e)
            return False

    @property
    def run_command(self) -> list[str]:
        """解析時に実行するコマンド．"""
        command = [self.executable]
        if self.options:
            command += self.options
        return command

    @property
    def version_command(self) -> list[str]:
        """バージョン確認時に実行するコマンド．"""
        return [self.executable, "-v"]
