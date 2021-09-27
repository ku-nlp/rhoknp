from abc import ABC, abstractmethod
from typing import Optional


class Unit(ABC):
    def __init__(self, parent_unit: Optional["Unit"]):
        self.parent_unit = parent_unit

        self.__text: Optional[str] = None

    @property
    @abstractmethod
    def child_units(self) -> Optional[list["Unit"]]:
        raise NotImplementedError

    @property
    def text(self) -> str:
        if self.child_units is not None:
            return "".join(str(child_unit) for child_unit in self.child_units)
        elif self.__text is not None:
            return self.__text
        else:
            raise ValueError("Failed to construct a text representation")

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text
