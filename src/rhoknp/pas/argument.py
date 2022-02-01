import weakref
from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional

from rhoknp.units.base_phrase import BasePhrase

if TYPE_CHECKING:
    from rhoknp.pas.pas import Pas
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.phrase import Phrase
    from rhoknp.units.sentence import Sentence


class ArgumentType(Enum):
    """
    ref: https://nlp.ist.i.kyoto-u.ac.jp/index.php?KNP%2F%E6%A0%BC%E8%A7%A3%E6%9E%90%E7%B5%90%E6%9E%9C%E6%9B%B8%E5%BC%8F
    """

    CASE_EXPLICIT = "C"  # a.k.a. overt
    CASE_HIDDEN = "N"
    OMISSION = "O"
    DEMONSTRATIVE = "D"
    EXOPHOR = "E"
    UNASSIGNED = "U"


class BaseArgument(ABC):
    """A base class for all kinds of arguments"""

    def __init__(self, arg_type: ArgumentType):
        self.type: ArgumentType = arg_type
        self.optional = False
        self._pas: Optional["Pas"] = None

    @property
    def is_special(self) -> bool:
        return self.type == ArgumentType.EXOPHOR

    @property
    def pas(self) -> "Pas":
        if self._pas is None:
            raise AttributeError("pas has not been set")
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        self._pas = weakref.proxy(pas)

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError


class Argument(BaseArgument):
    def __init__(self, base_phrase: BasePhrase, arg_type: ArgumentType):
        super().__init__(arg_type)
        self.base_phrase: BasePhrase = base_phrase

    @property
    def unit(self) -> BasePhrase:
        return self.base_phrase

    @property
    def document(self) -> "Document":
        return self.base_phrase.document

    @property
    def sentence(self) -> "Sentence":
        return self.base_phrase.sentence

    @property
    def clause(self) -> "Clause":
        return self.base_phrase.clause

    @property
    def phrase(self) -> "Phrase":
        return self.base_phrase.phrase

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base_phrase={repr(self.base_phrase)}, arg_type={repr(self.type)})"

    def __str__(self) -> str:
        return self.base_phrase.text

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Argument) and self.base_phrase == other.base_phrase


class SpecialArgument(BaseArgument):
    """外界を指す項を表すクラス

    Args:
        exophor (str): 外界照応詞 (不特定:人など)
        eid (int): 外界照応詞のエンティティID
    """

    def __init__(self, exophor: str, eid: int):
        super().__init__(ArgumentType.EXOPHOR)
        self.exophor: str = exophor
        self.eid: int = eid

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(exophor={repr(self.exophor)}, eid={repr(self.eid)})"

    def __str__(self) -> str:
        return self.exophor

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SpecialArgument) and self.exophor == other.exophor
