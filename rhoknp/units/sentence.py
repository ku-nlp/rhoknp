from typing import TYPE_CHECKING

from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.morpheme import Morpheme


class Sentence(Unit):
    def __init__(self, parent: "Document"):
        super().__init__(parent.document)

        self.__text: str = None
        self.__clauses: list["Clause"] = None
        self.__morphemes: list["Morpheme"] = None

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text

    @property
    def clauses(self):
        return [clause for clause in self.__clauses]

    @property
    def chunks(self):
        return [chunk for clause in self.clauses for chunk in clause.chunks]

    @property
    def phrases(self):
        return [phrase for chunk in self.chunks for phrase in chunk.phrases]

    @property
    def morphemes(self):
        return self.__morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list["Morpheme"]):
        self.__morphemes = morphemes

    def to_jumanpp(self):
        return "\n".join(morpheme.to_jumanpp() for morpheme in self.morphemes) + "\nEOS"
