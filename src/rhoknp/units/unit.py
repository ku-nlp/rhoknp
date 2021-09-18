from typing import Optional
import weakref


class Unit:
    def __init__(self, parent_unit: Optional["Unit"]):
        self.parent_unit = parent_unit and weakref.ref(parent_unit)

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        raise NotImplementedError