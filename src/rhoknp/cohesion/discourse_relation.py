import logging
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp import Clause

logger = logging.getLogger(__name__)


@dataclass
class DiscourseRelation:
    """談話関係クラス"""

    PAT: ClassVar[re.Pattern[str]] = re.compile(r"(?P<sid>.+?)/(?P<base_phrase_index>\d+?)/(?P<label>[^;]+);?")
    sid: str
    base_phrase_index: int
    label: str
    modifier: Optional["Clause"] = None
    head: Optional["Clause"] = None

    def __str__(self) -> str:
        return self.to_fstring()

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f"<談話関係:{self.sid}/{self.base_phrase_index}/{self.label}>"


class DiscourseRelationList(list[DiscourseRelation]):
    """談話関係リストクラス"""

    def __str__(self) -> str:
        return self.to_fstring()

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f'<談話関係:{";".join(f"{r.sid}/{r.base_phrase_index}/{r.label}" for r in self)}>'


@dataclass
class DiscourseRelationTagValue:
    """関係タグ付きコーパスにおける <談話関係> タグの値を表すクラス．"""

    sid: str
    base_phrase_index: int
    label: str

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f"{self.sid}/{self.base_phrase_index}/{self.label}"


@dataclass
class DiscourseRelationTag:
    """関係タグ付きコーパスにおける <談話関係> タグを表すクラス．"""

    PAT: ClassVar[re.Pattern[str]] = re.compile(r"<談話関係:(?P<values>[^/]+/\d+/[^/]+(;[^/]+/\d+/[^/]+)*)>")
    values: list[DiscourseRelationTagValue] = field(default_factory=list)

    def __str__(self) -> str:
        return self.to_fstring()

    def __bool__(self) -> bool:
        return len(self.values) > 0

    @classmethod
    def from_fstring(cls, fstring: str) -> "DiscourseRelationTag":
        """KNP における素性文字列からオブジェクトを作成．"""
        match = cls.PAT.search(fstring)
        values = []
        if match:
            for value in match.group("values").split(";"):
                sid, base_phrase_index, label = value.split("/")
                values.append(DiscourseRelationTagValue(sid, int(base_phrase_index), label))
        return cls(values)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        if self.values:
            return f'<談話関係:{";".join(value.to_fstring() for value in self.values)}>'
        return ""
