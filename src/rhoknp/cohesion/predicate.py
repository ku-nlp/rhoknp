from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from rhoknp.cohesion.pas import Pas
    from rhoknp.units.base_phrase import BasePhrase


class Predicate:
    """述語を表すクラス．

    Args:
        unit: 述語の基本句．
        cfid: 格フーレムID．
    """

    def __init__(self, unit: "BasePhrase", cfid: Optional[str] = None) -> None:
        self.unit: "BasePhrase" = unit  #: 述語の基本句．
        self.cfid: Optional[str] = cfid  #: 格フーレムID．
        self._pas: Optional["Pas"] = None

    @property
    def base_phrase(self) -> "BasePhrase":
        """基本句．"""
        return self.unit

    @property
    def text(self) -> str:
        """表層文字列．"""
        return self.unit.text

    @property
    def sid(self) -> str:
        """文 ID．"""
        if self.unit.sentence is None:
            raise AttributeError("sentence has not been set")
        return self.unit.sentence.sid

    @property
    def pas(self) -> "Pas":
        """述語項構造．"""
        if self._pas is None:
            raise AttributeError("pas has not been set")
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        """述語項構造．

        Args:
            pas: 述語項構造．
        """
        self._pas = pas

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {repr(self.text)}>"
