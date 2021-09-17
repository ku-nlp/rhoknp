from typing import TYPE_CHECKING, Optional

from rhoknp.units.morpheme import Morpheme
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document


class Sentence(Unit):

    count = 0

    def __init__(self, document: Optional["Document"] = None):
        super().__init__(document)

        self.index = self.count

        self.__text: str = None
        self.comment: str = None
        self.clauses: list["Clause"] = None
        self.morphemes: list["Morpheme"] = None

        Sentence.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        if self.clauses is not None:
            return self.clauses
        else:
            return self.morphemes

    @property
    def text(self):
        if self.__text is not None:
            return self.__text
        else:
            return "".join(str(child_unit) for child_unit in self.child_units)

    @text.setter
    def text(self, text: str):
        self.__text = text

    def to_jumanpp(self):
        jumanpp_text = ""
        if self.comment is not None:
            jumanpp_text += self.comment + "\n"
        jumanpp_text += (
            "\n".join(morpheme.to_jumanpp() for morpheme in self.morphemes) + "\nEOS"
        )
        return jumanpp_text

    @classmethod
    def from_string(
        cls, text: str, document: Optional["Document"] = None
    ) -> "Sentence":
        sentence = cls(document)
        sentence.text = text
        return sentence

    @classmethod
    def from_jumanpp(
        cls, jumanpp_text: str, document: Optional["Document"] = None
    ) -> "Sentence":
        sentence = cls(document)

        if jumanpp_text.startswith("#"):
            comment, jumanpp_text = jumanpp_text.split("\n", maxsplit=1)
            sentence.comment = comment

        morphemes = []
        for line in jumanpp_text.split("\n"):
            if line.startswith("#"):
                continue
            if line.strip() == "EOS":
                break
            morphemes.append(Morpheme(line, sentence))
        sentence.morphemes = morphemes
        return sentence
