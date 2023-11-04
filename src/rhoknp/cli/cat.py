from typing import ClassVar, List

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexer import RegexLexer
from pygments.token import Comment, Generic, Keyword, Text

from rhoknp import Document
from rhoknp.units import BasePhrase, Morpheme, Phrase


class KNPLexer(RegexLexer):
    """KNP の出力を色付けするための Lexer."""

    name: ClassVar[str] = "KNP"
    url: ClassVar[str] = "https://github.com/ku-nlp/knp"
    filenames: ClassVar[List[str]] = ["*.knp", "*.kwja"]
    mimetypes: ClassVar[List[str]] = ["text/plain"]

    tokens = {  # noqa: RUF012
        "root": [
            (Phrase.PAT.pattern, Generic.Heading),
            (BasePhrase.PAT.pattern, Generic.Subheading),
            (Morpheme.PAT.pattern, Text),
            (r"^#.*$", Comment.Single),
            (r"^EOS$", Keyword.Reserved),
        ],
    }


def print_document(document: Document) -> None:
    """KNP ファイルを色付きで表示．

    Args:
        document (Document): 文書．
    """
    print(highlight(document.to_knp(), KNPLexer(), TerminalFormatter()))
