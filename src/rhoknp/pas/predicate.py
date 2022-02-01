import weakref
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rhoknp.pas.pas import Pas
    from rhoknp.units.base_phrase import BasePhrase


class Predicate:
    def __init__(self, unit: "BasePhrase", cfid: Optional[str] = None):
        self.unit: "BasePhrase" = unit
        self.cfid = cfid
        self._pas: Optional["Pas"] = None

    @property
    def phrase(self) -> "BasePhrase":
        return self.unit

    @property
    def text(self) -> str:
        return self.unit.text

    @property
    def pas(self) -> "Pas":
        if self._pas is None:
            raise AttributeError("pas has not been set")
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        self._pas = weakref.proxy(pas)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text={repr(self.text)})"
