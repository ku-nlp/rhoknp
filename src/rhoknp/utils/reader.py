import logging
import re
from typing import Callable, Iterator, List, Literal, Optional, TextIO, Union

from rhoknp import Sentence

logger = logging.getLogger(__name__)


def chunk_by_sentence(f: TextIO) -> Iterator[str]:
    """解析結果ファイルを文ごとに分割するジェネレータ．

    Args:
        f: 分割するファイル．

    Example:
        >>> from rhoknp.units import Sentence
        >>> from rhoknp.utils.reader import chunk_by_sentence
        >>> with open("example.knp") as f:
        ...     for knp in chunk_by_sentence(f):
        ...         sentence = Sentence.from_knp(knp)
    """
    buffer = []
    for line in f:
        if line.strip() == "":
            continue
        buffer.append(line)
        if line.rstrip("\n") == Sentence.EOS:
            yield "".join(buffer)
            buffer = []
    if buffer:
        yield "".join(buffer)


def chunk_by_document(
    f: TextIO, doc_id_format: Union[Literal["default", "kwdlc", "wac"], Callable] = "default"
) -> Iterator[str]:
    """解析結果ファイルを文書ごとに分割するジェネレータ．

    Args:
        f: 分割するファイル．
        doc_id_format: 文書IDのフォーマット．

    Example:
        >>> from rhoknp.units import Document
        >>> from rhoknp.utils.reader import chunk_by_document
        >>> with open("example.knp") as f:
        ...     for knp in chunk_by_document(f):
        ...         document = Document.from_knp(knp)

    .. note::
        文書IDのフォーマットとして指定可能なのは以下の通り：
            * "default": 文ID (S-ID) の最後のハイフン以前を文書IDとみなす．
                (例) # S-ID:A-X-1 -> 文書ID: A-X
            * "kwdlc": KWDLCの文IDから文書IDを取り出す．
                (例) # S-ID:w201106-0000060050-1 -> 文書ID: w201106-0000060050
            * "wac": WACの文IDから文書IDを取り出す．
                (例) # S-ID:wiki00100176-00 -> 文書ID: wiki00100176

        関数が指定された場合，文解析結果の先頭行から文書IDを取り出す関数とみなす．
        例えば default 相当の処理を行うには以下のような関数を渡す．

            >>> def default_doc_id_format(line: str) -> str:
            ...     return line.lstrip("# S-ID:").rsplit("-", maxsplit=1)[0]
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
        raise TypeError(f"Invalid doc_id_format: {doc_id_format}")

    prev_doc_id: Optional[str] = None
    buffer: List[str] = []
    for sentence in chunk_by_sentence(f):
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
            sid_string = match_sid[1]
            match = pat.match(sid_string)
            if match is None:
                logger.warning(f"Invalid S-ID: {sid_string}")
                return None
            return match["did"]
        return None

    return extract_doc_id
