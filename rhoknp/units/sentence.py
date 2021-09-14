from typing import TYPE_CHECKING, Optional

from rhoknp.units.unit import Unit
from rhoknp.units.morpheme import Morpheme

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document


class Sentence(Unit):
    def __init__(self, document: Optional["Document"] = None):
        super().__init__(document)

        self.__text: str = None
        self.clauses: list["Clause"] = None
        self.morphemes: list["Morpheme"] = None

    @property
    def text(self):
        if self.__text is not None:
            return self.__text
        else:
            return "".join(str(m) for m in self.morphemes)

    # @property
    # def text(self):
    #     if self.child_units is not None:
    #         return "".join(str(m) for m in self.child_units)

    @text.setter
    def text(self, text: str):
        self.__text = text

    def to_jumanpp(self):
        return "\n".join(morpheme.to_jumanpp() for morpheme in self.morphemes) + "\nEOS"

    @classmethod
    def from_string(cls, text: str) -> "Sentence":
        sent = cls()
        sent.text = text
        return sent

    @classmethod
    def from_jumanpp(cls, jumanpp_text: str) -> "Sentence":
        sent = cls()
        morphemes = []
        for line in jumanpp_text.split("\n"):
            if line.strip() == "EOS":
                break
            morphemes.append(Morpheme(sent, line))
        sent.morphemes = morphemes
        sent.text = "".join(str(m) for m in morphemes)
        return sent

    def __str__(self) -> str:
        return self.__text
