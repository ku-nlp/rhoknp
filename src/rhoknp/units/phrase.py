from typing import TYPE_CHECKING, Optional

from .unit import Unit
from rhoknp.units.morpheme import Morpheme

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk


class Phrase(Unit):
    def __init__(self, parent: "Chunk"):
        super().__init__(parent)
        self.sentence = parent.sentence
        self.clause = parent.clause
        self.chunk = parent

        self.__morphemes: list["Morpheme"] = None

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        return self.morphemes

    @property
    def text(self):
        return "".join(str(child_unit) for child_unit in self.child_units)

    @property
    def morphemes(self):
        return self.__morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list["Morpheme"]):
        self.__morphemes = morphemes

    @classmethod
    def from_knp(cls,
                 knp_text: str,
                 parent: "Chunk"
                 ) -> "Phrase":
        phrase = cls(parent)
        morphemes: list[Morpheme] = []
        for line in knp_text.split("\n"):
            if line.startswith("+"):
                continue  # TODO: extract feature
            morpheme = Morpheme(line, phrase.sentence)
            morphemes.append(morpheme)
        phrase.morphemes = morphemes
        return phrase
