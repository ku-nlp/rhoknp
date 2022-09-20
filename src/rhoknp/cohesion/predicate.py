from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rhoknp.cohesion.pas import Pas
    from rhoknp.units.base_phrase import BasePhrase


class Predicate:
    def __init__(self, unit: "BasePhrase", cfid: Optional[str] = None):
        self.unit: "BasePhrase" = unit
        self.cfid: Optional[str] = cfid
        self._pas: Optional["Pas"] = None

    @property
    def base_phrase(self) -> "BasePhrase":
        return self.unit

    @property
    def text(self) -> str:
        return self.unit.text

    @property
    def sid(self) -> str:
        if self.unit.sentence is None:
            raise AttributeError("sentence has not been set")
        if self.unit.sentence.sid is None:
            raise AttributeError(f"sid of sentence: {repr(self.unit.sentence)} has not been set")
        return self.unit.sentence.sid

    @property
    def pas(self) -> "Pas":
        if self._pas is None:
            raise AttributeError("pas has not been set")
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        self._pas = pas

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {repr(self.text)}>"
