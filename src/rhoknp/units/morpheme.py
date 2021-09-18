import re
from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, fields, astuple

from .unit import Unit
from rhoknp.utils.features import Features

if TYPE_CHECKING:
    from rhoknp.units.sentence import Sentence


@dataclass
class MorphemeAttributes:
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
    _ATTRIBUTES_PATTERN: str = r"(?P<attrs>(\S+?\s){10}\S+?)"
    # language=RegExp
    _SEMANTICS_PATTERN: str = r'(?P<sems>("([^"]|\\")+?")|NIL)'
    # language=RegExp
    _FEATURES_PATTERN: str = r"(?P<feats>(<.+>)*)"
    JUMANPP_PATTERN: re.Pattern = re.compile(
        rf"^({_ATTRIBUTES_PATTERN})\s({_SEMANTICS_PATTERN})(\s{_FEATURES_PATTERN})?$"
    )

    count = 0

    def __init__(self,
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

    def __str__(self) -> str:
        return self.text

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        return None

    @classmethod
    def from_jumanpp(cls,
                     jumanpp_text: str,
                     sentence: Optional["Sentence"] = None,
                     ) -> "Morpheme":
        match = cls.JUMANPP_PATTERN.match(jumanpp_text)
        if match is None:
            raise ValueError(f"malformed line: {jumanpp_text}")
        attributes = MorphemeAttributes.from_jumanpp(match.group("attrs"))
        semantics: str = match.group("sems").strip('"')
        features = Features.from_fstring(match.group("feats") or "")
        return cls(attributes, semantics, features, sentence=sentence)

    def to_jumanpp(self) -> str:
        ret = ""
        ret += self._attributes.to_jumanpp()
        ret += f' "{self.semantics}"'
        ret += f" {self.features.to_fstring()}"
        return ret
