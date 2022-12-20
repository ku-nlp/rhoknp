from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from rhoknp.cohesion.pas import Pas
    from rhoknp.units.base_phrase import BasePhrase


class Predicate:
    """述語を表すクラス．

    Args:
        base_phrase: 述語の基本句．
        cfid: 格フーレムID．
    """

    def __init__(self, base_phrase: "BasePhrase", cfid: Optional[str] = None) -> None:
        self.base_phrase: "BasePhrase" = base_phrase  #: 述語の基本句．
        self.cfid: Optional[str] = cfid  #: 格フーレムID．
        self._pas: Optional["Pas"] = None

    @property
    def text(self) -> str:
        """表層文字列．"""
        return self.base_phrase.text

    @property
    def sid(self) -> str:
        """文 ID．"""
        return self.base_phrase.sentence.sid

    @property
    def pas(self) -> "Pas":
        """述語項構造．"""
        assert self._pas is not None
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

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False or self.base_phrase != other.base_phrase:
            return False
        if self.cfid is None or other.cfid is None:
            return True
        return self.cfid == other.cfid
