import weakref
from typing import Optional


class Unit:
    def __init__(self, parent_unit: Optional["Unit"]):
        self.parent_unit = parent_unit and weakref.ref(parent_unit)

        self.__text: str = None

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        raise NotImplementedError

    @property
    def text(self) -> str:
        if self.child_units is not None:
            return "".join(str(child_unit) for child_unit in self.child_units)
        else:
            return self.__text

    @text.setter
    def text(self, text: str):
        self.__text = text
