from typing import Optional


class Unit:
    def __init__(self, parent_unit: Optional["Unit"]):
        self.parent_unit = parent_unit

    @property
    def child_units(self) -> Optional[list["Unit"]]:
        raise NotImplementedError
