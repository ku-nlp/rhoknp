import re
from typing import TYPE_CHECKING, Optional

from .phrase import DepType, Phrase
from .utils import Features

from .unit import Unit

if TYPE_CHECKING:
    from .clause import Clause


class Chunk(Unit):
    KNP_PATTERN: re.Pattern = re.compile(
        fr"^\* (?P<pid>-1|\d+)(?P<dtype>[DPAI]) {Features.PATTERN.pattern}$"
    )

    def __init__(self, parent: "Clause"):
        super().__init__(parent)
        self.sentence = parent.sentence
        self.clause = parent

        self.__phrases: list["Phrase"] = None
        self.parent_id: Optional[int] = None
        self.dep_type: DepType = None
        self.features: Features = None

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

    @classmethod
    def from_knp(cls, knp_text: str, parent: "Clause") -> "Chunk":
        chunk = cls(parent)
        phrases: list[Phrase] = []
        phrase_lines = []
        for line in knp_text.split("\n"):
            if line.startswith("*"):
                match = cls.KNP_PATTERN.match(line)
                if match is None:
                    raise ValueError(f"malformed line: {line}")
                chunk.parent_id = int(match.group("pid"))
                chunk.dep_type = DepType.value_of(match.group("dtype"))
                chunk.features = Features(match.group("feats"))
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
