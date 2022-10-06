import logging
from subprocess import PIPE, run
from typing import List, Optional, Union

from rhoknp.processors.processor import Processor
from rhoknp.units import Document, Sentence

logger = logging.getLogger(__name__)


class KWJA(Processor):
    """KWJA クラス．

    Args:
        executable: KWJA のパス．
        options: KWJA のオプション．

    Example:

        >>> from rhoknp import KWJA
        <BLANKLINE>
        >>> kwja = KWJA()
        >>> document = kwja.apply("電気抵抗率は電気の通しにくさを表す物性値である。")
    """

    def __init__(
        self,
        executable: str = "kwja",
        options: Optional[List[str]] = None,
    ):
        self.executable = executable  #: KWJA のパス．
        self.options = options  #: KWJA のオプション．

    def __repr__(self) -> str:
        arg_string = f"executable={repr(self.executable)}"
        if self.options is not None:
            arg_string += f", options={repr(self.options)}"
        return f"{self.__class__.__name__}({arg_string})"

    def apply_to_document(self, document: Union[Document, str]) -> Document:
        """文書に KWJA を適用する．

        Args:
            document: 文書．
        """
        if isinstance(document, str):
            document = Document(document)

        p = run(self.run_command + [f"{document.to_raw_text()}"], stdout=PIPE, encoding="utf-8")
        return Document.from_knp(p.stdout)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に KWJA を適用する．

        Args:
            sentence: 文．
        """
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        p = run(self.run_command + [f"{sentence.to_raw_text()}"], stdout=PIPE, encoding="utf-8")
        return Sentence.from_knp(p.stdout)

    def is_available(self) -> bool:
        """KWJA が利用可能であれば True を返す．"""
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
            command += ["--text"]
        return command

    @property
    def version_command(self) -> List[str]:
        """バージョン確認時に実行するコマンド．"""
        return [self.executable, "--version"]
