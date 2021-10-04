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

    def __init__(
        self,
        parent_index: int,
        dep_type: DepType,
        features: Features,
        clause: Optional["Clause"] = None,
    ):
        super().__init__()

        self._clause = clause

        self._phrases: Optional[list[Phrase]] = None
        self.parent_index: int = parent_index
        self.dep_type: DepType = dep_type
        self.features: Features = features

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
        assert self._phrases is not None
        return self._phrases

    @phrases.setter
    def phrases(self, phrases: list[Phrase]) -> None:
        self._phrases = phrases

    @property
    def morphemes(self) -> list[Morpheme]:
        return [morpheme for phrase in self.phrases for morpheme in phrase.morphemes]

    @property
    def parent(self) -> Optional["Chunk"]:
        if self.parent_index == -1:
            return None
        return self.sentence.chunks[self.parent_index]

    @property
    def children(self) -> list["Chunk"]:
        return [chunk for chunk in self.sentence.chunks if chunk.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str, clause: Optional["Clause"] = None) -> "Chunk":
        first_line, *lines = knp_text.split("\n")
        match = cls.KNP_PATTERN.match(first_line)
        if match is None:
            raise ValueError(f"malformed line: {first_line}")
        parent_index = int(match.group("pid"))
        dep_type = DepType(match.group("dtype"))
        features = Features(match.group("feats"))
        chunk = cls(parent_index, dep_type, features, clause)

        phrases: list[Phrase] = []
        phrase_lines: list[str] = []
        for line in lines:
            if not line.strip():
                continue
            if line.startswith("+") and phrase_lines:
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
        ret = f"* {self.parent_index}{self.dep_type.value} {self.features}\n"
        ret += "".join(phrase.to_knp() for phrase in self.phrases)
        return ret
