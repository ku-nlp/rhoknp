import logging
import re
from typing import IO, Callable, Iterator, List, Literal, Optional, Union

from rhoknp import Sentence

logger = logging.getLogger(__name__)


class Reader:
    """言語解析結果を読み込むクラス．

    Args:
        f: 読み込むファイル．

    Examples:

        >>> from rhoknp.units import Sentence
        >>> from rhoknp.utils.reader import Reader
        <BLANKLINE>
        >>> with open("example.knp") as f:
        ...     reader = Reader(f)
        ...     for knp in reader():
        ...         sentence = Sentence.from_knp(knp)
    """

    def __init__(self, f: IO) -> None:
        self.f = f

    def __call__(self) -> Iterator[str]:
        return self.read_as_sentences()

    def read_as_sentences(self) -> Iterator[str]:
        """ファイルを文に対する解析結果の集合として読み込む．

        Examples:

            >>> from rhoknp.units import Sentence
            >>> from rhoknp.utils.reader import Reader
            <BLANKLINE>
            >>> with open("example.knp") as f:
            ...     reader = Reader(f)
            ...     for knp in reader.read_as_sentences():
            ...         sentence = Sentence.from_knp(knp)
        """
        buffer = []
        for line in self.f:
            if line.strip() == "":
                continue
            buffer.append(line)
            if line.strip() == Sentence.EOS_PAT:
                yield "".join(buffer)
                buffer = []
        if buffer:
            yield "".join(buffer)

    def read_as_documents(
        self, doc_id_format: Union[Literal["default", "kwdlc", "wac"], Callable] = "default"
    ) -> Iterator[str]:
        """ファイルを文書に対する解析結果の集合として読み込む．

        Args:
            doc_id_format: 文書IDのフォーマット．

        Examples:

            >>> from rhoknp.units import Document
            >>> from rhoknp.utils.reader import Reader
            <BLANKLINE>
            >>> with open("example.knp") as f:
            ...     reader = Reader(f)
            ...     for knp in reader.read_as_documents():
            ...         document = Document.from_knp(knp)


        .. note::
            文書IDのフォーマットとして指定可能なのは以下の通り．
                * "default": 文ID (S-ID) の最初のハイフン以前を文書IDとみなす．
                    (例) # S-ID:A-1 -> 文書ID: A
                * "kwdlc": KWDLCの文IDから文書IDを取り出す．
                    (例) # S-ID:w201106-0000060050-1 -> 文書ID: w201106-0000060050
                * "wac": WACの文IDから文書IDを取り出す．
                    (例) # S-ID:wiki00100176-00 -> 文書ID: wiki00100176

            関数が指定された場合， S-ID から文書IDを取り出す関数とみなす．
        """
        if isinstance(doc_id_format, str):
            if doc_id_format == "default":
                extract_doc_id = _extract_doc_id(Sentence.SID_PAT)
            elif doc_id_format == "kwdlc":
                extract_doc_id = _extract_doc_id(Sentence.SID_PAT_KWDLC)
            elif doc_id_format == "wac":
                extract_doc_id = _extract_doc_id(Sentence.SID_PAT_WAC)
            else:
                raise ValueError(f"Invalid doc_id_format: {doc_id_format}")
        elif callable(doc_id_format):
            extract_doc_id = doc_id_format
        else:
            raise ValueError(f"Invalid doc_id_format: {doc_id_format}")

        prev_doc_id: Optional[str] = None
        buffer: List[str] = []
        for sentence in self.read_as_sentences():
            doc_id = extract_doc_id(sentence.split("\n")[0])
            if buffer and (prev_doc_id != doc_id or doc_id is None):
                yield "".join(buffer)
                buffer = []
            buffer.append(sentence)
            prev_doc_id = doc_id
        if buffer:
            yield "".join(buffer)


def _extract_doc_id(pat: re.Pattern) -> Callable[[str], Optional[str]]:
    """文書IDを抽出する関数を返す．

    Args:
        pat: 文書IDを抽出する正規表現．
    """

    def extract_doc_id(line: str) -> Optional[str]:
        if match_sid := re.match(r"# S-ID: ?(\S*)( .+)?$", line):
            sid_string = match_sid.group(1)
            match = pat.match(sid_string)
            if match is None:
                logger.warning(f"Invalid S-ID: {sid_string}")
                return None
            return match.group("did")
        return None

    return extract_doc_id
