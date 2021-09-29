import re
from enum import Enum
from typing import TYPE_CHECKING, Optional

from .morpheme import Morpheme
from .unit import Unit
from .utils import Features

if TYPE_CHECKING:
    from .chunk import Chunk
    from .clause import Clause
    from .document import Document
    from .sentence import Sentence


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
        fr"^\+ (?P<pid>-1|\d+)(?P<dtype>[{''.join(e.value for e in DepType)}]) {Features.PATTERN.pattern}$"
    )
    count = 0

    def __init__(self, chunk: "Chunk"):
        super().__init__()

        self.__chunk = chunk

        self.__morphemes: Optional[list["Morpheme"]] = None
        self.parent_id: Optional[int] = None
        self.dep_type: Optional[DepType] = None
        self.features: Optional[Features] = None

        self.index = self.count
        Phrase.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional["Chunk"]:
        return self.__chunk

    @property
    def child_units(self) -> list[Morpheme]:
        return self.morphemes

    @property
    def document(self) -> "Document":
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        return self.clause.sentence

    @property
    def clause(self) -> "Clause":
        return self.chunk.clause

    @property
    def chunk(self) -> "Chunk":
        if self.parent_unit is None:
            raise AttributeError("This attribute has not been set")
        return self.parent_unit

    @property
    def morphemes(self) -> list[Morpheme]:
        if self.__morphemes is None:
            raise AttributeError("This attribute is not available before applying KNP")
        return self.__morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list["Morpheme"]):
        self.__morphemes = morphemes

    @classmethod
    def from_knp(cls, knp_text: str, chunk: "Chunk") -> "Phrase":
        phrase = cls(chunk)
        morphemes: list[Morpheme] = []
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
            if line.startswith("+"):
                match = cls.KNP_PATTERN.match(line)
                if match is None:
                    raise ValueError(f"malformed line: {line}")
                phrase.parent_id = int(match.group("pid"))
                phrase.dep_type = DepType.value_of(match.group("dtype"))
                phrase.features = Features(match.group("feats"))
                continue
            morpheme = Morpheme.from_jumanpp(line, phrase=phrase)
            morphemes.append(morpheme)
        phrase.morphemes = morphemes
        return phrase

    def to_knp(self) -> str:
        if self.parent_id is None or self.dep_type is None or self.features is None:
            raise AttributeError
        ret = "+ {pid}{dtype} {feats}\n".format(
            pid=self.parent_id,
            dtype=self.dep_type.value,
            feats=self.features.to_fstring(),
        )
        for morpheme in self.morphemes:
            ret += morpheme.to_jumanpp() + "\n"
        return ret
