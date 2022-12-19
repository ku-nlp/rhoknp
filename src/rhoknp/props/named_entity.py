import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, List, Optional

if TYPE_CHECKING:
    from rhoknp.units.morpheme import Morpheme

logger = logging.getLogger(__name__)


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
        """有効な固有表現カテゴリであれば True．

        Args:
            value: 固有表現のカテゴリ．
        """
        return any(value == item.value for item in cls)


@dataclass
class NamedEntity:
    """固有表現を表すクラス．"""

    PAT: ClassVar[re.Pattern] = re.compile(r"(?P<cat>\w+):(?P<name>[^>]+)")

    category: NamedEntityCategory
    morphemes: List["Morpheme"]

    def __str__(self) -> str:
        return self.text

    @property
    def text(self) -> str:
        """固有表現の表層文字列．"""
        return "".join(m.text for m in self.morphemes)

    @classmethod
    def from_fstring(cls, fstring: str, candidate_morphemes: List["Morpheme"]) -> Optional["NamedEntity"]:
        """KNP における素性文字列からオブジェクトを作成．"""
        match = cls.PAT.match(fstring)
        if match is None:
            logger.warning(f"{fstring} is not a valid NE fstring")
            return None
        category: str = match["cat"]
        if not NamedEntityCategory.has_value(category):
            logger.warning(f"{candidate_morphemes[0].sentence.sid}: unknown NE category: {category}")
            return None
        name: str = match["name"]
        if (span := cls._find_morpheme_span(name, candidate_morphemes)) is None:
            logger.warning(f"{candidate_morphemes[0].sentence.sid}: morpheme span of '{name}' not found")
            return None
        return NamedEntity(NamedEntityCategory(category), candidate_morphemes[span.start : span.stop])

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f"<NE:{self.category.value}:{self.text}>"

    @staticmethod
    def _find_morpheme_span(name: str, candidates: List["Morpheme"]) -> Optional[range]:
        """固有表現の文字列にマッチする形態素の範囲を返す．

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
