from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rhoknp.units.document import Document


class Unit:
    def __init__(self, parent_unit: Optional["Unit"]):
        self.parent_unit = parent_unit
        self.__text = None
