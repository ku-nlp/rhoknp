import logging
from subprocess import PIPE, Popen, run
from typing import List, Optional, Sequence, Union

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

    Attributes:
        executable: Juman++ のパス．
        options: Juman++ のオプション．
        senter: 文分割器のインスタンス．文分割がまだなら，先にこのインスタンスを用いて文分割する．
            未設定なら RegexSenter を使って文分割する．

    Example:

        >>> from rhoknp import Jumanpp
        <BLANKLINE>
        >>> jumanpp = Jumanpp()
        >>> sentence = jumanpp.apply("電気抵抗率は、どんな材料が電気を通しにくいかを比較するために、用いられる物性値である。")
    """

    def __init__(
        self,
        executable: str = "jumanpp",
        options: Optional[List[str]] = None,
        senter: Optional[Processor] = None,
    ) -> None:
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

    def apply(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に解析器を適用する．

        Args:
            sentence (Union[Sentence, str]): 文．
        """
        return self.apply_to_sentence(sentence)

    def batch_apply(self, sentences: Sequence[Union[Sentence, str]], processes: int = 0) -> List[Sentence]:
        """複数文に解析器を適用する．

        Args:
            sentences (Sequence[Union[Sentence, str]]): 文のリスト．
            processes (int, optional): 並列処理数．0以下の場合はシングルプロセスで処理する．
        """
        return self.batch_apply_to_sentences(sentences, processes)

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
                logger.debug("senter is not specified; use RegexSenter")
                self.senter = RegexSenter()
            document = self.senter.apply_to_document(document)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            jumanpp_text, _ = p.communicate(input=document.to_raw_text())
        return Document.from_jumanpp(jumanpp_text)

    def apply_to_sentence(self, sentence: Union[Sentence, str]) -> Sentence:
        """文に Jumanpp を適用する．

        Args:
            sentence: 文．
        """
        if isinstance(sentence, str):
            sentence = Sentence(sentence)

        with Popen(self.run_command, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
            jumanpp_text, _ = p.communicate(input=sentence.to_raw_text())
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
    def run_command(self) -> List[str]:
        """解析時に実行するコマンド．"""
        command = [self.executable]
        if self.options:
            command += self.options
        return command

    @property
    def version_command(self) -> List[str]:
        """バージョン確認時に実行するコマンド．"""
        return [self.executable, "-v"]
