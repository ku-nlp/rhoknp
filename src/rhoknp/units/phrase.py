import re
import weakref
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from .morpheme import Morpheme
from .unit import Unit
from .utils import DepType, Features, Rels

if TYPE_CHECKING:
    from .chunk import Chunk
    from .clause import Clause
    from .document import Document
    from .sentence import Sentence


class Phrase(Unit):
    KNP_PATTERN: re.Pattern = re.compile(
        fr"^\+ (?P<pid>-1|\d+)(?P<dtype>[{''.join(e.value for e in DepType)}])( {Features.PATTERN.pattern})?$"
    )
    count = 0

    def __init__(self, parent_index: int, dep_type: DepType, features: Features, rels: Rels):
        super().__init__()

        # parent unit
        self._chunk: Optional["Chunk"] = None

        # child units
        self._morphemes: Optional[list[Morpheme]] = None

        self.parent_index: int = parent_index
        self.dep_type: DepType = dep_type
        self.features: Features = features
        self.rels: Rels = rels

        self.index = self.count
        Phrase.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional["Chunk"]:
        return self._chunk

    @property
    def child_units(self) -> Optional[list[Morpheme]]:
        return self._morphemes

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
        if self._chunk is None:
            raise AttributeError("chunk has not been set")
        return self._chunk

    @chunk.setter
    def chunk(self, chunk: "Chunk") -> None:
        self._chunk = chunk

    @property
    def morphemes(self) -> list[Morpheme]:
        if self._morphemes is None:
            raise AttributeError("morphemes have not been set")
        return self._morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]):
        for morpheme in morphemes:
            morpheme.phrase = weakref.proxy(self)
        self._morphemes = morphemes

    @cached_property
    def head(self) -> Morpheme:
        head = None
        for morpheme in self.morphemes:
            if morpheme.features is None:
                continue
            if "内容語" in morpheme.features and head is None:
                # Consider the first content word as the head
                head = morpheme
            if "準内容語" in morpheme.features:
                # Sub-content words overwrite the head
                head = morpheme
        if head:
            return head
        return self.morphemes[0]

    @property
    def parent(self) -> Optional["Phrase"]:
        if self.parent_index == -1:
            return None
        return self.sentence.phrases[self.parent_index]

    @cached_property
    def children(self) -> list["Phrase"]:
        return [phrase for phrase in self.sentence.phrases if phrase.parent == self]

    @classmethod
    def from_knp(cls, knp_text: str) -> "Phrase":
        first_line, *lines = knp_text.split("\n")
        match = cls.KNP_PATTERN.match(first_line)
        if match is None:
            raise ValueError(f"malformed line: {first_line}")
        parent_index = int(match.group("pid"))
        dep_type = DepType(match.group("dtype"))
        features = Features(match.group("feats") or "")
        rels = Rels.from_fstring(match.group("feats") or "")
        phrase = cls(parent_index, dep_type, features, rels)

        morphemes: list[Morpheme] = []
        for line in lines:
            if not line.strip():
                continue
            morpheme = Morpheme.from_jumanpp(line)
            morphemes.append(morpheme)
        phrase.morphemes = morphemes
        return phrase

    def to_knp(self) -> str:
        ret = f"+ {self.parent_index}{self.dep_type.value}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        ret += "".join(morpheme.to_jumanpp() for morpheme in self.morphemes)
        return ret
