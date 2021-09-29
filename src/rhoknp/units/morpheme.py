import re
from dataclasses import astuple, dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Optional, Union

from .unit import Unit
from .utils import Features

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
    # language=RegExp
    _SEMANTICS_PATTERN: str = r'(?P<sems>("([^"]|\\")+?")|NIL)'
    JUMANPP_PATTERN: re.Pattern = re.compile(
        (
            rf"^({MorphemeAttributes.JUMANPP_PATTERN.pattern})"
            + rf"(\s{_SEMANTICS_PATTERN})?"
            + rf"(\s{Features.PATTERN.pattern})?$"
        )
    )

    count = 0

    def __init__(
        self,
        attributes: MorphemeAttributes,
        semantics: str,
        features: Features,
        sentence: Optional["Sentence"] = None,
        phrase: Optional["Phrase"] = None,
    ):
        super().__init__()

        self.__phrase = phrase
        self.__sentence = sentence

        self._attributes = attributes
        self.semantics = semantics
        self.features = features

        self.text = attributes.surf

        self.index = self.count
        Morpheme.count += 1

    def __str__(self) -> str:
        return self.text

    @property
    def parent_unit(self) -> Optional[Union["Phrase", "Sentence"]]:
        if self.__phrase is not None:
            return self.__phrase
        if self.__sentence is not None:
            return self.__sentence
        return None

    @property
    def child_units(self) -> None:
        return None

    @property
    def document(self) -> "Document":
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        if self.__sentence is not None:
            return self.__sentence
        if self.__phrase is not None:
            return self.clause.sentence
        raise AttributeError("This attribute has not been set")

    @property
    def clause(self) -> "Clause":
        return self.chunk.clause

    @property
    def chunk(self) -> "Chunk":
        return self.phrase.chunk

    @property
    def phrase(self) -> "Phrase":
        if self.__phrase is None:
            raise AttributeError("This attribute is not available before applying KNP")
        return self.__phrase

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
    def fstring(self) -> str:
        return self.features.to_fstring()

    @classmethod
    def from_jumanpp(
        cls,
        jumanpp_text: str,
        sentence: Optional["Sentence"] = None,
        phrase: Optional["Phrase"] = None,
    ) -> "Morpheme":
        match = cls.JUMANPP_PATTERN.match(jumanpp_text)
        if match is None:
            raise ValueError(f"malformed line: {jumanpp_text}")
        attributes = MorphemeAttributes.from_jumanpp(match.group("attrs"))
        semantics: str = (match.group("sems") or "").strip('"')
        features = Features.from_fstring(match.group("feats") or "")
        if phrase is not None:
            return cls(attributes, semantics, features, phrase=phrase)
        else:
            return cls(attributes, semantics, features, sentence=sentence)

    def to_jumanpp(self) -> str:
        ret = ""
        ret += self._attributes.to_jumanpp()
        if self.semantics:
            ret += f' "{self.semantics}"' if self.semantics != "NIL" else " NIL"
        if self.features:
            ret += f" {self.features.to_fstring()}"
        return ret
