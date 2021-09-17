from typing import TYPE_CHECKING

from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk
    from rhoknp.units.morpheme import Morpheme


class Phrase(Unit):
    def __init__(self, parent: "Chunk", analysis: str):
        super().__init__(parent)
        self.sentence = parent.sentence
        self.clause = parent.clause
        self.chunk = parent

        self.__analysis = analysis

        self.__morphemes: list["Morpheme"] = None

    @property
    def morphemes(self):
        return self.__morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list["Morpheme"]):
        self.__morphemes = morphemes
