from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rhoknp import Morpheme


@dataclass
class NamedEntity:
    """固有表現を表すクラス．"""

    category: str
    morphemes: list["Morpheme"]

    @property
    def text(self) -> str:
        return "".join(m.text for m in self.morphemes)

    def __str__(self) -> str:
        return self.text
