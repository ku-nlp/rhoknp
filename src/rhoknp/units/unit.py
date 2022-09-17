from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence


class Unit(ABC):
    def __init__(self) -> None:
        self.index: int = -1
        self._text: Optional[str] = None

    def __post_init__(self) -> None:
        if self.child_units is not None:
            for child_unit in self.child_units:
                child_unit.__post_init__()

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {repr(self.index)}, {repr(self.text)}>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False:
            return False
        if self.parent_unit != other.parent_unit:
            return False
        return self.index == other.index

    @property
    def parent_unit(self) -> Optional["Unit"]:
        raise NotImplementedError

    @property
    @abstractmethod
    def child_units(self) -> Optional[Sequence["Unit"]]:
        raise NotImplementedError

    @property
    def text(self) -> str:
        if self._text is not None:
            return self._text
        elif self.child_units is not None:
            self._text = "".join(str(child_unit) for child_unit in self.child_units)
            return self._text
        raise AssertionError

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
