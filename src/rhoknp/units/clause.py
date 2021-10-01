from typing import TYPE_CHECKING, Optional

from .chunk import Chunk
from .morpheme import Morpheme
from .phrase import Phrase
from .unit import Unit

if TYPE_CHECKING:
    from .document import Document
    from .sentence import Sentence


class Clause(Unit):
    count = 0

    def __init__(self, sentence: Optional["Sentence"] = None):
        super().__init__()

        self._sentence = sentence

        self._chunks: Optional[list[Chunk]] = None

        self.index = self.count
        Clause.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional["Sentence"]:
        return self._sentence

    @property
    def child_units(self) -> list[Chunk]:
        return self.chunks

    @property
    def document(self) -> "Document":
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        if self.parent_unit is None:
            raise AttributeError("This attribute has not been set")
        return self.parent_unit

    @property
    def chunks(self) -> list[Chunk]:
        if self._chunks is None:
            raise AttributeError("This attribute is not available before applying KNP")
        return self._chunks

    @chunks.setter
    def chunks(self, chunks: list[Chunk]):
        self._chunks = chunks

    @property
    def phrases(self) -> list[Phrase]:
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @property
    def head(self) -> Phrase:
        for phrase in self.phrases:
            if phrase.features and "節-主辞" in phrase.features:
                return phrase
        raise AssertionError

    @property
    def parent(self) -> Optional["Clause"]:
        head_parent = self.head.parent
        while head_parent in self.phrases:
            head_parent = head_parent.parent
        for clause in self.sentence.clauses:
            if head_parent in clause.phrases:
                return clause
        return None

    @property
    def children(self) -> list["Clause"]:
        return [clause for clause in self.sentence.clauses if clause.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str, sentence: Optional["Sentence"] = None) -> "Clause":
        clause = cls(sentence)
        chunks = []
        chunk_lines: list[str] = []
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("*") and chunk_lines:
                chunk = Chunk.from_knp("\n".join(chunk_lines), clause)
                chunks.append(chunk)
                chunk_lines = []
            chunk_lines.append(line)
        else:
            chunk = Chunk.from_knp("\n".join(chunk_lines), clause)
            chunks.append(chunk)
        clause.chunks = chunks
        return clause

    def to_knp(self) -> str:
        return "".join(chunk.to_knp() for chunk in self.chunks)
