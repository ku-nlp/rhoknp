import logging
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, List, Optional

if TYPE_CHECKING:
    from rhoknp import Clause, Sentence

logger = logging.getLogger(__name__)


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

    PAT: ClassVar[re.Pattern] = re.compile(r"<談話関係:(?P<values>[^/]+/\d+/[^/]+(;[^/]+/\d+/[^/]+)*)>")
    values: List[DiscourseRelationTagValue] = field(default_factory=list)

    def __str__(self) -> str:
        return self.to_fstring()

    def __bool__(self) -> bool:
        return len(self.values) > 0

    def __len__(self) -> int:
        return len(self.values)

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


@dataclass
class DiscourseRelation:
    """談話関係クラス"""

    sid: str
    base_phrase_index: int
    label: str
    modifier: "Clause"
    head: "Clause"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.sid}, {self.base_phrase_index}, {self.label})"

    @classmethod
    def from_discourse_relation_tag_value(
        cls,
        value: DiscourseRelationTagValue,
        modifier: "Clause",
    ) -> Optional["DiscourseRelation"]:
        head_sentence: Optional["Sentence"] = None
        if modifier.sentence.has_document:
            sentences = modifier.document.sentences
        else:
            sentences = [modifier.sentence]
        for sentence in sentences:
            if sentence.sid == value.sid:
                head_sentence = sentence
                break
        if head_sentence is None:
            logger.warning(f"{value.sid} not found")
            return None
        if value.base_phrase_index >= len(head_sentence.base_phrases):
            logger.warning(f"index out of range in {value.sid}")
            return None
        head_base_phrase = head_sentence.base_phrases[value.base_phrase_index]
        head = head_base_phrase.clause
        if head.end != head_base_phrase:
            logger.warning(f"invalid clause tag in {value.sid}")
            return None
        return cls(value.sid, value.base_phrase_index, value.label, modifier, head)

    def to_discourse_relation_tag_value(self) -> DiscourseRelationTagValue:
        return DiscourseRelationTagValue(self.sid, self.base_phrase_index, self.label)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return self.to_discourse_relation_tag_value().to_fstring()
