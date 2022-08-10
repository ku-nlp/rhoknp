import logging
import re
from dataclasses import dataclass, field
from typing import ClassVar

logger = logging.getLogger(__name__)


@dataclass
class DiscourseRelationTagValue:
    sid: str
    base_phrase_index: int
    label: str

    def to_fstring(self) -> str:
        return f"{self.sid}/{self.base_phrase_index}/{self.label}"


@dataclass
class DiscourseRelationTag:
    """関係タグ付きコーパスにおける <談話関係> タグを表すクラス．"""

    PAT: ClassVar[re.Pattern[str]] = re.compile(r"<談話関係:(?P<values>[^/]+/\d+/[^/]+(;[^/]+/\d+/[^/]+)*)>")
    values: list[DiscourseRelationTagValue] = field(default_factory=list)

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
        if self.values:
            return f'<談話関係:{";".join(value.to_fstring() for value in self.values)}>'
        return ""

    def __str__(self) -> str:
        return self.to_fstring()
