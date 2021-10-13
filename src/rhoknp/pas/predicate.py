from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rhoknp.units.phrase import Phrase


class Predicate:
    def __init__(self, unit: "Phrase", cfid: Optional[str] = None):
        self.unit: "Phrase" = unit
        self.cfid = cfid

    @property
    def phrase(self) -> "Phrase":
        return self.unit
