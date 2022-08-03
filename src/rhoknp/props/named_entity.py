from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp import Morpheme


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
