import re
from enum import Enum
from typing import TYPE_CHECKING, Optional

from rhoknp.units.morpheme import Morpheme
from .utils import Features

from .unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.chunk import Chunk


class DepType(Enum):
    dependency = "D"
    parallel = "P"
    apposition = "A"
    imperfect_parallel = "I"

    @classmethod
    def value_of(cls, val) -> "DepType":
        for e in cls:
            if e.value == val:
                return e
        raise ValueError(f"invalid dependency type name: {val}")


class Phrase(Unit):
    KNP_PATTERN: re.Pattern = re.compile(
        fr"^\+ (?P<pid>-1|\d+)(?P<dtype>[DPAI]) {Features.PATTERN.pattern}$"
    )

    def __init__(self, parent: "Chunk"):
        super().__init__(parent)
        self.sentence = parent.sentence
        self.clause = parent.clause
        self.chunk = parent

        self.__morphemes: list["Morpheme"] = None
        self.parent_id: Optional[int] = None
        self.dep_type: DepType = None
        self.features: Features = None

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
    def from_knp(cls, knp_text: str, parent: "Chunk") -> "Phrase":
        phrase = cls(parent)
        morphemes: list[Morpheme] = []
        for line in knp_text.split("\n"):
            if line.startswith("+"):
                match = cls.KNP_PATTERN.match(line)
                if match is None:
                    raise ValueError(f"malformed line: {line}")
                phrase.parent_id = int(match.group("pid"))
                phrase.dep_type = DepType.value_of(match.group("dtype"))
                phrase.features = Features(match.group("feats"))
                continue
            morpheme = Morpheme.from_jumanpp(line, phrase.sentence)
            morphemes.append(morpheme)
        phrase.morphemes = morphemes
        return phrase
