from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence


class Unit(ABC):
    """言語単位の基底クラス・"""

    def __init__(self) -> None:
        self._text: Optional[str] = None

    def __post_init__(self) -> None:
        if self.child_units is not None:
            for child_unit in self.child_units:
                child_unit.__post_init__()

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {repr(self.text)}>"

    @property
    @abstractmethod
    def parent_unit(self) -> Optional["Unit"]:
        """上位の言語単位．"""
        raise NotImplementedError

    @property
    @abstractmethod
    def child_units(self) -> Optional[Sequence["Unit"]]:
        """下位の言語単位．"""
        raise NotImplementedError

    @property
    def text(self) -> str:
        """言語単位の表層文字列．"""
        if self._text is not None:
            return self._text
        if self.child_units is not None:
            self._text = "".join(str(child_unit) for child_unit in self.child_units)
            return self._text
        raise AttributeError

    @text.setter
    def text(self, text: str) -> None:
        """言語単位の表層文字列．

        Args:
            text: 言語単位の表層文字列．
        """
        self._text = text
