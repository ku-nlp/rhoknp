from typing import ClassVar, List

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexer import RegexLexer, bygroups, default
from pygments.token import Comment, Generic, Literal, Name, Number, String, Text, Whitespace

from rhoknp import BasePhrase, Document, Morpheme, Phrase


class KNPLexer(RegexLexer):
    """KNP の出力を色付けするための Lexer."""

    name: ClassVar[str] = "KNP"
    url: ClassVar[str] = "https://github.com/ku-nlp/knp"
    filenames: ClassVar[List[str]] = ["*.knp", "*.kwja"]
    mimetypes: ClassVar[List[str]] = ["text/plain"]

    tokens = {  # noqa: RUF012
        "root": [
            (r"\s+", Whitespace),
            (rf"(?={Phrase.PAT.pattern})", Text, "phrase"),
            (rf"(?={BasePhrase.PAT.pattern})", Text, "base_phrase"),
            (rf"(?={Morpheme.PAT.pattern})", Text, "morpheme"),
            (r"^#.*$", Comment.Single),
            (r"^EOS$", Generic.Subheading),
        ],
        "phrase": [
            (r"\s+", Whitespace),
            (r"^\*", Generic.Heading),
            (r"(-?\d+)([DPAI])", bygroups(Number, Literal.String)),
            (r"<", Name.Tag, "tag"),
            default("#pop"),
        ],
        "base_phrase": [
            (r"\s+", Whitespace),
            (r"^\+", Generic.Heading),
            (r"(-?\d+)([DPAI])", bygroups(Number, Literal.String)),
            (r"<rel", Name.Tag, "rel_tag"),
            (r"<", Name.Tag, "tag"),
            default("#pop"),
        ],
        "morpheme": [
            (r"\s+", Whitespace),
            (
                r"^(\S+)(\s)"  # Surface
                r"(\S+)(\s)"  # Reading
                r"(\S+)(\s)"  # Lemma
                r"(\S+)(\s)(\d+)(\s)"  # Pos
                r"(\S+)(\s)(\d+)(\s)"  # Subpos
                r"(\S+)(\s)(\d+)(\s)"  # Conjtype
                r"(\S+)(\s)(\d+)",  # Conjform
                bygroups(
                    Text,
                    Whitespace,
                    Text,
                    Whitespace,
                    Text,
                    Whitespace,
                    Literal.String,
                    Whitespace,
                    Literal.Number,
                    Whitespace,
                    Literal.String,
                    Whitespace,
                    Literal.Number,
                    Whitespace,
                    Literal.String,
                    Whitespace,
                    Literal.Number,
                    Whitespace,
                    Literal.String,
                    Whitespace,
                    Literal.Number,
                ),
            ),
            (r'"[^"]+?"', String),
            (r"NIL", String),
            (r"<", Name.Tag, "tag"),
            default("#pop"),
        ],
        "tag": [
            (r"\s+", Whitespace),
            (r"([^>:]+)(:)?([^>]+)?", bygroups(Name.Tag, Name.Tag, Name.Attribute)),
            (r">", Name.Tag, "#pop"),
        ],
        "rel_tag": [
            (r"\s+", Whitespace),
            (r'(\S+=)("\S+?")', bygroups(Name.Attribute, String)),
            (r"/>", Name.Tag, "#pop"),
        ],
    }


def print_document(document: Document, is_dark: bool = False) -> None:
    """KNP ファイルを色付きで表示．

    Args:
        document (Document): 文書．
        is_dark (bool, optional): ターミナルの背景色が dark なら True．デフォルトは False．
    """
    formatter = TerminalFormatter(bg="dark" if is_dark else "light")
    print(highlight(document.to_knp(), KNPLexer(), formatter), end="")
