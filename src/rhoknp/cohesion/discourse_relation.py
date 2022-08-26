import logging
import re
from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, ClassVar, Iterable, Optional, Union, overload

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

    PAT: ClassVar[re.Pattern[str]] = re.compile(r"<談話関係:(?P<values>[^/]+/\d+/[^/]+(;[^/]+/\d+/[^/]+)*)>")
    values: list[DiscourseRelationTagValue] = field(default_factory=list)

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


class DiscourseRelationList(MutableSequence[DiscourseRelation]):
    """談話関係リストクラス"""

    def __init__(self, values: list[DiscourseRelation] = None) -> None:
        self._items: list[DiscourseRelation] = values if values is not None else []

    def insert(self, index: int, value: DiscourseRelation) -> None:
        current_tag = value.modifier.end.discourse_relation_tag
        if (tag_value := value.to_discourse_relation_tag_value()) not in current_tag.values:
            current_tag.values.append(tag_value)
        self._items.insert(index, value)

    @overload
    def __getitem__(self, index: int) -> DiscourseRelation:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[DiscourseRelation]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[DiscourseRelation, list[DiscourseRelation]]:
        return self._items[index]

    @overload
    def __setitem__(self, index: int, value: DiscourseRelation) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[DiscourseRelation]) -> None:
        ...

    def __setitem__(
        self, index: Union[int, slice], value: Union[DiscourseRelation, Iterable[DiscourseRelation]]
    ) -> None:
        if isinstance(index, int) and isinstance(value, DiscourseRelation):
            self._items[index] = value
            discourse_relations = [value]
        elif isinstance(index, slice) and isinstance(value, Iterable):
            value = list(value)
            self._items[index] = value
            discourse_relations = value
        else:
            raise TypeError(f"cannot assign {value} at {index}")
        for discourse_relation in discourse_relations:
            if isinstance(discourse_relation, DiscourseRelation):
                current_tag = discourse_relation.modifier.end.discourse_relation_tag
                if (tag_value := discourse_relation.to_discourse_relation_tag_value()) not in current_tag.values:
                    current_tag.values.append(tag_value)

    @overload
    def __delitem__(self, index: int) -> None:
        ...

    @overload
    def __delitem__(self, index: slice) -> None:
        ...

    def __delitem__(self, index: Union[int, slice]) -> None:
        for item in self._items[index] if isinstance(index, slice) else [self._items[index]]:
            item.modifier.end.discourse_relation_tag.values.remove(item.to_discourse_relation_tag_value())
        del self._items[index]

    def __str__(self) -> str:
        return str(self._items)

    def __len__(self) -> int:
        return len(self._items)
