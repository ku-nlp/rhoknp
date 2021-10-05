import re
from dataclasses import astuple, dataclass, fields
from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, List, Optional, Union

from .unit import Unit
from .utils import Features, Semantics

if TYPE_CHECKING:
    from .chunk import Chunk
    from .clause import Clause
    from .document import Document
    from .phrase import Phrase
    from .sentence import Sentence


@dataclass(frozen=True)
class MorphemeAttributes:
    JUMANPP_PATTERN: ClassVar[re.Pattern] = re.compile(
        r"(?P<attrs>([^ ]+ [^ ]+ [^ ]+ \w+ \d+ \D+ \d+ \D+ \d+ \D+ \d+))"
    )

    surf: str
    reading: str
    lemma: str
    pos: str
    pos_id: int
    subpos: str
    subpos_id: int
    conjtype: str
    conjtype_id: int
    conjform: str
    conjform_id: int

    @classmethod
    def from_jumanpp(cls, jumanpp_line: str) -> "MorphemeAttributes":
        kwargs = {}
        for field, value in zip(fields(cls), jumanpp_line.split(" ")):
            kwargs[field.name] = field.type(value)
        assert len(kwargs) == len(fields(cls)), f"malformed line: {jumanpp_line}"
        return cls(**kwargs)

    def to_jumanpp(self) -> str:
        return " ".join(str(item) for item in astuple(self))


class Morpheme(Unit):
    JUMANPP_PATTERN: re.Pattern = re.compile(
        (
            rf"^({MorphemeAttributes.JUMANPP_PATTERN.pattern})"
            + rf"(\s{Semantics.PATTERN.pattern})?"
            + rf"(\s{Features.PATTERN.pattern})?$"
        )
    )

    count = 0

    def __init__(
        self,
        attributes: MorphemeAttributes,
        semantics: Semantics,
        features: Features,
        sentence: Optional["Sentence"] = None,
        phrase: Optional["Phrase"] = None,
        homograph: bool = False,
    ):
        super().__init__()

        self._phrase = phrase
        self._sentence = sentence

        self._attributes = attributes
        self.semantics = semantics
        self.features = features
        self.homographs: List["Morpheme"] = []

        self.text = attributes.surf

        self.index = self.count
        if homograph is False:
            Morpheme.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional[Union["Phrase", "Sentence"]]:
        if self._phrase is not None:
            return self._phrase
        if self._sentence is not None:
            return self._sentence
        return None

    @property
    def child_units(self) -> None:
        return None

    @property
    def document(self) -> "Document":
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        if self._sentence is not None:
            return self._sentence
        if self._phrase is not None:
            return self.clause.sentence
        raise AttributeError("sentence has not been set")

    @property
    def clause(self) -> "Clause":
        return self.chunk.clause

    @property
    def chunk(self) -> "Chunk":
        return self.phrase.chunk

    @property
    def phrase(self) -> "Phrase":
        if self._phrase is None:
            raise AttributeError("not available before applying KNP")
        return self._phrase

    @property
    def surf(self) -> str:
        return self._attributes.surf

    @property
    def reading(self) -> str:
        return self._attributes.reading

    @property
    def lemma(self) -> str:
        return self._attributes.lemma

    @property
    def canon(self) -> Optional[str]:
        return self.semantics.get("代表表記", None)

    @property
    def pos(self) -> str:
        return self._attributes.pos

    @property
    def subpos(self) -> str:
        return self._attributes.subpos

    @property
    def conjtype(self) -> str:
        return self._attributes.conjtype

    @property
    def conjform(self) -> str:
        return self._attributes.conjform

    @property
    def sstring(self) -> str:
        return self.semantics.to_sstring()

    @property
    def fstring(self) -> str:
        return self.features.to_fstring()

    @cached_property
    def parent(self) -> Optional["Morpheme"]:
        if self.phrase.head == self:
            if self.phrase.parent is not None:
                return self.phrase.parent.head
            return None
        return self.phrase.head

    @cached_property
    def children(self) -> list["Morpheme"]:
        return [morpheme for morpheme in self.sentence.morphemes if morpheme.parent == self]

    @classmethod
    def from_jumanpp(
        cls,
        jumanpp_text: str,
        sentence: Optional["Sentence"] = None,
        phrase: Optional["Phrase"] = None,
    ) -> "Morpheme":
        first_line, *lines = jumanpp_text.rstrip().split("\n")
        morpheme = cls.from_jumanpp_line(first_line, sentence=sentence, phrase=phrase)
        for line in lines:
            assert line.startswith("@ ")
            homograph = cls.from_jumanpp_line(line[2:], sentence=sentence, phrase=phrase, homograph=True)
            morpheme.homographs.append(homograph)
        return morpheme

    @classmethod
    def from_jumanpp_line(
        cls,
        jumanpp_line: str,
        sentence: Optional["Sentence"] = None,
        phrase: Optional["Phrase"] = None,
        homograph: bool = False,
    ) -> "Morpheme":
        assert "\n" not in jumanpp_line.strip()
        match = cls.JUMANPP_PATTERN.match(jumanpp_line)
        if match is None:
            raise ValueError(f"malformed line: {jumanpp_line}")
        attributes = MorphemeAttributes.from_jumanpp(match.group("attrs"))
        semantics = Semantics.from_sstring(match.group("sems") or "")
        features = Features.from_fstring(match.group("feats") or "")
        if phrase is not None:
            return cls(attributes, semantics, features, phrase=phrase, homograph=homograph)
        else:
            return cls(attributes, semantics, features, sentence=sentence, homograph=homograph)

    def to_jumanpp(self) -> str:
        ret = self._attributes.to_jumanpp()
        if self.semantics:
            ret += f" {self.semantics}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        for homograph in self.homographs:
            ret += f"@ {homograph.to_jumanpp()}"
        return ret
