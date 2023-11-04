from typing import ClassVar, List

from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexer import RegexLexer
from pygments.token import Comment, Keyword, Number, Operator, String, Text

from rhoknp import Document


class KNPLexer(RegexLexer):
    """KNP の出力を色付けするための Lexer."""

    name: ClassVar[str] = "KNP"
    url: ClassVar[str] = "https://github.com/ku-nlp/knp"
    filenames: ClassVar[List[str]] = ["*.knp", "*.kwja"]
    mimetypes: ClassVar[List[str]] = ["text/plain"]

    tokens = {  # noqa: RUF012
        # "root": [
        #     (Phrase.PAT.pattern, Generic.Heading),
        #     (BasePhrase.PAT.pattern, Generic.Subheading),
        #     (Morpheme.PAT.pattern, Text),
        #     (r"^#.*$", Comment.Single),
        #     (r"^EOS$", Keyword.Reserved),
        # ],
        "root": [
            # Keywords
            (r"<", Keyword, "feature"),
            (r"^\+", Keyword, "tag_bnst"),
            (r"^\*", Keyword, "tag_bnst"),
            # EOS constant
            (r"^EOS$", Keyword.Constant),
            # Strings
            (r"\"", String, "string"),
            # Comments
            (r"^#", Comment, "comment"),
            # Other text
            (r"^[^+*\#\"<> ]+", Text),
            (r"(?<=\s)[^+*\#\"<> ]+", Text),
            (r".", Text),
        ],
        "string": [
            (r'[^"]+', String),
            (r"\"", String, "#pop"),
        ],
        "comment": [
            (r"[^\n]+", Comment),
            (r"\n", Text, "#pop"),
        ],
        "tag_bnst": [
            (r"(-1|\d+)[DPAI]", Number.Integer, "#pop"),
            (r"<", Keyword, "feature"),
            (r"\n", Text, "#pop"),
        ],
        "feature": [
            (r"\"", String, "string"),
            (r">", Keyword, "#pop"),
            (r":", Keyword),
            (r"=", Operator),
            # Feature value context is not yet defined in the .sublime-syntax sample provided
            # Assuming it could be similar to 'string' context for now
            (r'[^\s=>"]+', Text),  # Catch all for other text within a feature
        ],
    }


def print_document(document: Document) -> None:
    """KNP ファイルを色付きで表示．

    Args:
        document (Document): 文書．
    """
    print(highlight(document.to_knp(), KNPLexer(), TerminalFormatter()))
