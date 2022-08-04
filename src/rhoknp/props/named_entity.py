import re
from collections.abc import MutableSequence
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp import Morpheme


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

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f"<NE:{self.category.value}:{self.text}>"

    def to_ne_tag(self) -> NETag:
        """NETag オブジェクトに変換．"""
        return NETag(category=self.category.value, name=self.text)

    @staticmethod
    def find_morpheme_span(name: str, candidates: list["Morpheme"]) -> Optional[range]:
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


class NamedEntityList(MutableSequence):
    def __init__(self, items: list[NamedEntity] = None) -> None:
        if items is None:
            items = []
        self._items: list[NamedEntity] = items

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __delitem__(self, i) -> None:
        self._items[i].morphemes[-1].base_phrase.ne_tags.remove(self._items[i].to_ne_tag())
        del self._items[i]

    def __setitem__(self, i, v) -> None:
        if isinstance(v, NamedEntity):
            current_ne_tags = v.morphemes[-1].base_phrase.ne_tags
            ne_tag = v.to_ne_tag()
            if ne_tag not in current_ne_tags:
                current_ne_tags.append(ne_tag)
        self._items[i] = v

    def insert(self, i, v) -> None:
        if isinstance(v, NamedEntity):
            current_ne_tags = v.morphemes[-1].base_phrase.ne_tags
            ne_tag = v.to_ne_tag()
            if ne_tag not in current_ne_tags:
                current_ne_tags.append(ne_tag)
        self._items.insert(i, v)

    def __str__(self) -> str:
        return str(self._items)
