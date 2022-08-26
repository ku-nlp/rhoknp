import logging
import re
from collections.abc import MutableSequence
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Iterable, Optional, Union, overload

if TYPE_CHECKING:
    from rhoknp.units.morpheme import Morpheme

logger = logging.getLogger(__name__)


@dataclass
class NETag:
    """関係タグ付きコーパスにおける <NE> タグを表すクラス．"""

    PAT: ClassVar[re.Pattern[str]] = re.compile(r"<NE:(?P<cat>\w+):(?P<name>[^>]+)>")
    category: str
    name: str

    def to_fstring(self) -> str:
        return f"<NE:{self.category}:{self.name}>"


class NETagList(list[NETag]):
    """関係タグ付きコーパスにおける <NE> タグの列を表すクラス．"""

    @classmethod
    def from_fstring(cls, fstring: str) -> "NETagList":
        """KNP における素性文字列からオブジェクトを作成．"""
        rels = []
        for match in NETag.PAT.finditer(fstring):
            rels.append(NETag(category=match["cat"], name=match["name"]))
        return cls(rels)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return "".join(rel.to_fstring() for rel in self)

    def __str__(self) -> str:
        return self.to_fstring()


class NamedEntityCategory(Enum):
    """固有表現カテゴリを表す列挙体．"""

    ORGANIZATION = "ORGANIZATION"
    PERSON = "PERSON"
    LOCATION = "LOCATION"
    ARTIFACT = "ARTIFACT"
    DATE = "DATE"
    TIME = "TIME"
    MONEY = "MONEY"
    PERCENT = "PERCENT"
    OPTIONAL = "OPTIONAL"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return any(value == item.value for item in cls)


@dataclass
class NamedEntity:
    """固有表現を表すクラス．"""

    category: NamedEntityCategory
    morphemes: list["Morpheme"]

    @property
    def text(self) -> str:
        return "".join(m.text for m in self.morphemes)

    def __str__(self) -> str:
        return self.text

    @classmethod
    def from_ne_tag(cls, ne_tag: NETag, candidate_morphemes: list["Morpheme"]) -> Optional["NamedEntity"]:
        """NETag オブジェクトから初期化．"""
        if not NamedEntityCategory.has_value(ne_tag.category):
            logger.warning(f"{candidate_morphemes[0].sentence.sid}: unknown NE category: {ne_tag.category}")
            return None
        if (morpheme_range := cls._find_morpheme_span(ne_tag.name, candidate_morphemes)) is None:
            logger.warning(f"{candidate_morphemes[0].sentence.sid}: morpheme span of '{ne_tag.name}' not found")
            return None
        return NamedEntity(
            NamedEntityCategory(ne_tag.category),
            candidate_morphemes[morpheme_range.start : morpheme_range.stop],
        )

    def to_ne_tag(self) -> NETag:
        """NETag オブジェクトに変換．"""
        assert isinstance(self.category.value, str)
        return NETag(category=self.category.value, name=self.text)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return self.to_ne_tag().to_fstring()

    @staticmethod
    def _find_morpheme_span(name: str, candidates: list["Morpheme"]) -> Optional[range]:
        """name にマッチする形態素の範囲を返す．

        Args:
            name: 固有表現の文字列
            candidates: 固有表現を構成する候補形態素のリスト
        """
        stop = len(candidates)
        while stop > 0:
            for start in reversed(range(stop)):
                if "".join(m.text for m in candidates[start:stop]) == name:
                    return range(start, stop)
            stop -= 1
        return None


class NamedEntityList(MutableSequence[NamedEntity]):
    def __init__(self, items: list[NamedEntity] = None) -> None:
        self._items: list[NamedEntity] = items if items is not None else []

    def insert(self, index: int, value: NamedEntity) -> None:
        current_ne_tags = value.morphemes[-1].base_phrase.ne_tags
        ne_tag = value.to_ne_tag()
        if ne_tag not in current_ne_tags:
            current_ne_tags.append(ne_tag)
        self._items.insert(index, value)

    @overload
    def __getitem__(self, index: int) -> NamedEntity:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[NamedEntity]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[NamedEntity, list[NamedEntity]]:
        return self._items[index]

    @overload
    def __setitem__(self, index: int, value: NamedEntity) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[NamedEntity]) -> None:
        ...

    def __setitem__(self, index: Union[int, slice], value: Union[NamedEntity, Iterable[NamedEntity]]) -> None:
        if isinstance(index, int) and isinstance(value, NamedEntity):
            self._items[index] = value
            named_entities = [value]
        elif isinstance(index, slice) and isinstance(value, Iterable):
            value = list(value)
            self._items[index] = value
            named_entities = value
        else:
            raise TypeError(f"cannot assign {value} at {index}")
        for named_entity in named_entities:
            if isinstance(named_entity, NamedEntity):
                current_ne_tags = named_entity.morphemes[-1].base_phrase.ne_tags
                ne_tag = named_entity.to_ne_tag()
                if ne_tag not in current_ne_tags:
                    current_ne_tags.append(ne_tag)

    @overload
    def __delitem__(self, index: int) -> None:
        ...

    @overload
    def __delitem__(self, index: slice) -> None:
        ...

    def __delitem__(self, index: Union[int, slice]) -> None:
        for item in self._items[index] if isinstance(index, slice) else [self._items[index]]:
            item.morphemes[-1].base_phrase.ne_tags.remove(item.to_ne_tag())
        del self._items[index]

    def __str__(self) -> str:
        return str(self._items)

    def __len__(self) -> int:
        return len(self._items)
