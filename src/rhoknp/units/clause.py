from typing import TYPE_CHECKING, Optional

from .chunk import Chunk

from .unit import Unit

if TYPE_CHECKING:
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
    def chunks(self) -> list[Chunk]:
        return self.__chunks

    @chunks.setter
    def chunks(self, chunks: list["Chunk"]):
        self.__chunks = chunks

    @property
    def phrases(self):
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self):
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @classmethod
    def from_knp(cls, knp_text: str, sentence: "Sentence") -> "Clause":
        clause = cls(sentence)
        chunk = Chunk.from_knp(knp_text, clause)
        clause.chunks = [chunk]
        return clause
