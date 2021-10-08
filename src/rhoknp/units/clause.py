import weakref
from functools import cached_property
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

    def __init__(self):
        super().__init__()

        # parent unit
        self._sentence: Optional["Sentence"] = None

        # child units
        self._chunks: Optional[list[Chunk]] = None

        self.index = self.count
        Clause.count += 1

    @property
    def parent_unit(self) -> Optional["Sentence"]:
        return self._sentence

    @property
    def child_units(self) -> Optional[list[Chunk]]:
        return self._chunks

    @property
    def document(self) -> "Document":
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        if self.parent_unit is None:
            raise AttributeError("sentence has not been set")
        return self.parent_unit

    @sentence.setter
    def sentence(self, sentence: "Sentence") -> None:
        self._sentence = sentence

    @property
    def chunks(self) -> list[Chunk]:
        if self._chunks is None:
            raise AttributeError("chunks have not been set")
        return self._chunks

    @chunks.setter
    def chunks(self, chunks: list[Chunk]):
        for chunk in chunks:
            chunk.clause = weakref.proxy(self)
        self._chunks = chunks

    @property
    def phrases(self) -> list[Phrase]:
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @cached_property
    def head(self) -> Phrase:
        for phrase in self.phrases:
            if phrase.features and "節-主辞" in phrase.features:
                return phrase
        raise AssertionError

    @cached_property
    def parent(self) -> Optional["Clause"]:
        head_parent = self.head.parent
        while head_parent in self.phrases:
            head_parent = head_parent.parent
        for clause in self.sentence.clauses:
            if head_parent in clause.phrases:
                return clause
        return None

    @cached_property
    def children(self) -> list["Clause"]:
        return [clause for clause in self.sentence.clauses if clause.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Clause":
        clause = cls()
        chunks = []
        chunk_lines: list[str] = []
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("*") and chunk_lines:
                chunk = Chunk.from_knp("\n".join(chunk_lines))
                chunks.append(chunk)
                chunk_lines = []
            chunk_lines.append(line)
        else:
            chunk = Chunk.from_knp("\n".join(chunk_lines))
            chunks.append(chunk)
        clause.chunks = chunks
        return clause

    def to_knp(self) -> str:
        return "".join(chunk.to_knp() for chunk in self.chunks)
