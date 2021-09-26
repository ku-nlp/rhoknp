from typing import TYPE_CHECKING

from .chunk import Chunk
from .morpheme import Morpheme
from .phrase import Phrase
from .unit import Unit

if TYPE_CHECKING:
    from .document import Document
    from .sentence import Sentence


class Clause(Unit):
    count = 0

    def __init__(self, sentence: "Sentence"):
        super().__init__(sentence)

        self.__chunks: list["Chunk"] = None

        self.index = self.count
        Clause.count += 1

    def __str__(self) -> str:
        return self.text

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
        if self.__chunks is None:
            raise AttributeError("This attribute is not available before applying KNP")
        return self.__chunks

    @chunks.setter
    def chunks(self, chunks: list["Chunk"]):
        self.__chunks = chunks

    @property
    def phrases(self) -> list[Phrase]:
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self) -> list[Morpheme]:
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @classmethod
    def from_knp(cls, knp_text: str, sentence: "Sentence") -> "Clause":
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
        ret = ""
        for chunk in self.chunks:
            ret += chunk.to_knp()
        return ret
