from typing import TYPE_CHECKING, Optional

from .unit import Unit
from rhoknp.units.chunk import Chunk

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk
    from rhoknp.units.sentence import Sentence


class Clause(Unit):
    def __init__(self, parent: "Sentence"):
        super().__init__(parent)
        self.sentence = parent

        self.__chunks: list["Chunk"] = None

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        return self.chunks

    @property
    def text(self):
        return "".join(str(child_unit) for child_unit in self.child_units)

    @property
    def chunks(self):
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
    def from_knp(cls,
                 knp_text: str,
                 parent: "Sentence"
                 ) -> "Clause":
        clause = cls(parent)
        chunk = Chunk.from_knp(knp_text, parent=clause)
        clause.chunks = [chunk]
        return clause
