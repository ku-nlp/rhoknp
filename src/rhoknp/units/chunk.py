import re
from typing import TYPE_CHECKING, Optional

from .morpheme import Morpheme
from .phrase import DepType, Phrase
from .unit import Unit
from .utils import Features

if TYPE_CHECKING:
    from .clause import Clause
    from .document import Document
    from .sentence import Sentence


class Chunk(Unit):
    KNP_PATTERN: re.Pattern = re.compile(fr"^\* (?P<pid>-1|\d+)(?P<dtype>[DPAI]) {Features.PATTERN.pattern}$")
    count = 0

    def __init__(self, clause: Optional["Clause"] = None):
        super().__init__()

        self._clause = clause

        self._phrases: Optional[list[Phrase]] = None
        self.parent_id: Optional[int] = None
        self.dep_type: Optional[DepType] = None
        self.features: Optional[Features] = None

        self.index = self.count
        Chunk.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional["Clause"]:
        return self._clause

    @property
    def child_units(self) -> list[Phrase]:
        return self.phrases

    @property
    def document(self) -> "Document":
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        return self.clause.sentence

    @property
    def clause(self) -> "Clause":
        if self.parent_unit is None:
            raise AttributeError("This attribute has not been set")
        return self.parent_unit

    @property
    def phrases(self) -> list[Phrase]:
        if self._phrases is None:
            raise AttributeError("This attribute is not available before applying KNP")
        return self._phrases

    @phrases.setter
    def phrases(self, phrases: list[Phrase]) -> None:
        self._phrases = phrases

    @property
    def morphemes(self) -> list[Morpheme]:
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @classmethod
    def from_knp(cls, knp_text: str, clause: Optional["Clause"] = None) -> "Chunk":
        chunk = cls(clause)
        phrases: list[Phrase] = []
        phrase_lines: list[str] = []
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
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
                    phrase = Phrase.from_knp("\n".join(phrase_lines), chunk)
                    phrases.append(phrase)
                    phrase_lines = []
            phrase_lines.append(line)
        else:
            phrase = Phrase.from_knp("\n".join(phrase_lines), chunk)
            phrases.append(phrase)

        chunk.phrases = phrases
        return chunk

    def to_knp(self) -> str:
        if self.parent_id is None or self.dep_type is None or self.features is None:
            raise AttributeError
        ret = "* {pid}{dtype} {feats}\n".format(
            pid=self.parent_id,
            dtype=self.dep_type.value,
            feats=self.features.to_fstring(),
        )
        for phrase in self.phrases:
            ret += phrase.to_knp()
        return ret
