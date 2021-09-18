from typing import TYPE_CHECKING, Optional
import re

from .unit import Unit
from rhoknp.units.phrase import Phrase, DepType

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.phrase import Phrase


class Chunk(Unit):
    KNP_PATTERN: re.Pattern = re.compile(r"^\* (?P<pid>-1|\d+)(?P<dtype>[DPAI]) (?P<features>(<.+>)*)$")

    def __init__(self, parent: "Clause"):
        super().__init__(parent)
        self.sentence = parent.sentence
        self.clause = parent

        self.__phrases: list["Phrase"] = None
        self.parent_id: Optional[int] = None
        self.dep_type: DepType = None
        self.features: str = None

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        return self.phrases

    @property
    def text(self):
        return "".join(str(child_unit) for child_unit in self.child_units)

    @property
    def phrases(self):
        return self.__phrases

    @phrases.setter
    def phrases(self, phrases: list["Phrase"]):
        self.__phrases = phrases

    @property
    def morphemes(self):
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @property
    def child_units(self):
        return self.__phrases

    @classmethod
    def from_knp(cls,
                 knp_text: str,
                 parent: "Clause"
                 ) -> "Chunk":
        chunk = cls(parent)
        phrases: list[Phrase] = []
        phrase_lines = []
        for line in knp_text.split("\n"):
            if line.startswith("*"):
                match = cls.KNP_PATTERN.match(line)
                if match is None:
                    raise ValueError(f"malformed line: {line}")
                chunk.parent_id = int(match["pid"])
                chunk.dep_type = DepType.value_of(match["dtype"])
                chunk.features = match["features"]
                continue
            if line.startswith("+"):
                if phrase_lines:
                    phrase = Phrase.from_knp("\n".join(phrase_lines), parent=chunk)
                    phrases.append(phrase)
                    phrase_lines = []
            phrase_lines.append(line)
        else:
            phrase = Phrase.from_knp("\n".join(phrase_lines), parent=chunk)
            phrases.append(phrase)

        chunk.phrases = phrases
        return chunk
