from typing import ClassVar, List

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Generic, Keyword, Literal, Number, Punctuation, Text, Whitespace

from rhoknp import BasePhrase, Document, Morpheme, Phrase


class KNPLexer(RegexLexer):
    """KNP の出力を色付けするための Lexer."""

    name: ClassVar[str] = "KNP"
    url: ClassVar[str] = "https://github.com/ku-nlp/knp"
    filenames: ClassVar[List[str]] = ["*.knp", "*.kwja"]
    mimetypes: ClassVar[List[str]] = ["text/plain"]

    tokens = {  # noqa: RUF012
        "root": [
            (rf"(?={Phrase.PAT.pattern})", Text, "phrase"),
            (rf"(?={BasePhrase.PAT.pattern})", Text, "base_phrase"),
            (rf"(?={Morpheme.PAT.pattern})", Text, "morpheme"),
            (r"^#.*$", Comment.Single),
            (r"^EOS$", Keyword.Constant),
        ],
        "phrase": [
            (r"\s", Whitespace),
            (r"^(\*)", Generic.Heading),
            (r"(-?\d+)([DPAI])", bygroups(Number, Literal)),
            (r"<", Punctuation, "feature"),
            (r"", Text, "#pop"),
        ],
        "base_phrase": [
            (r"\s", Whitespace),
            (r"^(\+)", Generic.Subheading),
            (r"(-?\d+)([DPAI])", bygroups(Number, Literal)),
            (r"<", Punctuation, "feature"),
            (r"", Text, "#pop"),
        ],
        "morpheme": [
            (r"\s", Whitespace),
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
            (r'"', Punctuation, "semantics"),
            (r"NIL", Text),
            (r"<", Punctuation, "feature"),
            (r"", Text, "#pop"),
        ],
        "semantics": [
            (r"\s", Whitespace),
            (r'[^\s:"]+', Literal.String),
            (r":", Punctuation),
            (r'"', Punctuation, "#pop"),
        ],
        "feature": [
            (r"[^>:]+", Literal.String),
            (r":", Punctuation),
            (r">", Punctuation, "#pop"),
        ],
    }


def print_document(document: Document) -> None:
    """KNP ファイルを色付きで表示．

    Args:
        document (Document): 文書．
    """
    print(highlight(document.to_knp(), KNPLexer(), TerminalFormatter()))
