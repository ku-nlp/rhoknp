from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence


class Unit(ABC):
    def __init__(self) -> None:
        self._index: Optional[int] = None

        self._text: Optional[str] = None

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(index={repr(self.index)}, text={repr(self.text)})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            if self.parent_unit != other.parent_unit:
                return False
            return self.index == other.index
        return False

    @property
    def parent_unit(self) -> Optional["Unit"]:
        raise NotImplementedError

    @property
    @abstractmethod
    def child_units(self) -> Optional[Sequence["Unit"]]:
        raise NotImplementedError

    @property
    def index(self) -> int:
        assert self._index is not None
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        self._index = index

    @property
    def text(self) -> str:
        if self.child_units is not None:
            return "".join(str(child_unit) for child_unit in self.child_units)
        elif self._text is not None:
            return self._text
        raise AssertionError

    @text.setter
    def text(self, text: str) -> None:
        self._text = text
