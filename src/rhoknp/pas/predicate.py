from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rhoknp.pas.pas import Pas
    from rhoknp.units.phrase import Phrase


class Predicate:
    def __init__(self, unit: "Phrase", cfid: Optional[str] = None):
        self.unit: "Phrase" = unit
        self.cfid = cfid
        self._pas: Optional["Pas"] = None

    @property
    def phrase(self) -> "Phrase":
        return self.unit

    @property
    def pas(self) -> "Pas":
        if self._pas is None:
            raise AttributeError("pas has not been set")
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        self._pas = pas
