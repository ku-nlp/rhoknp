import re
from dataclasses import astuple, dataclass, fields
from typing import TYPE_CHECKING, ClassVar, Optional

from .utils import Features

from .unit import Unit

if TYPE_CHECKING:
    from .sentence import Sentence


@dataclass(frozen=True)
class MorphemeAttributes:
    JUMANPP_PATTERN: ClassVar[re.Pattern] = re.compile(r"(?P<attrs>(\S+?\s){10}\S+?)")

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
    ):
        super().__init__(sentence)
        self._attributes = attributes
        self.semantics = semantics
        self.features = features

        self.sentence = self.parent_unit
        self.clause = None
        self.chunk = None
        self.phrase = None

        self.text = attributes.surf

        self.index = self.count
        Morpheme.count += 1

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
    def child_units(self) -> Optional[list["Unit"]]:
        return None

    @classmethod
    def from_jumanpp(
        cls,
        jumanpp_text: str,
        sentence: Optional["Sentence"] = None,
    ) -> "Morpheme":
        match = cls.JUMANPP_PATTERN.match(jumanpp_text)
        if match is None:
            raise ValueError(f"malformed line: {jumanpp_text}")
        attributes = MorphemeAttributes.from_jumanpp(match.group("attrs"))
        semantics: str = (match.group("sems") or "").strip('"')
        features = Features.from_fstring(match.group("feats") or "")
        return cls(attributes, semantics, features, sentence=sentence)

    def to_jumanpp(self) -> str:
        ret = ""
        ret += self._attributes.to_jumanpp()
        if self.semantics:
            ret += f' "{self.semantics}"' if self.semantics != "NIL" else " NIL"
        if self.features:
            ret += f" {self.features.to_fstring()}"
        return ret

    def __str__(self) -> str:
        return self.text
