from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional, Union

from rhoknp.cohesion.exophora import ExophoraReferent

if TYPE_CHECKING:
    from rhoknp.cohesion.pas import Pas
    from rhoknp.units.base_phrase import BasePhrase
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.phrase import Phrase
    from rhoknp.units.sentence import Sentence


class ArgumentType(Enum):
    """項のタイプ．"""

    CASE_EXPLICIT = "C"  #: 直接係り受けをもつ格要素 (格は明示されている)
    CASE_HIDDEN = "N"  #: 直接係り受けをもつ格要素（格は明示されていない）
    OMISSION = "O"  #: 省略の指示対象
    DEMONSTRATIVE = "D"  #: 指示詞の指示対象
    EXOPHORA = "E"  #: 特殊（不特定：人など）
    UNASSIGNED = "U"  #: 格要素の割り当てなし


class BaseArgument(ABC):
    """A base class for all kinds of arguments"""

    def __init__(self, arg_type: ArgumentType):
        self.type = arg_type
        self.optional = False
        self._pas: Optional["Pas"] = None

    @property
    def is_special(self) -> bool:
        return self.type == ArgumentType.EXOPHORA

    @property
    def pas(self) -> "Pas":
        if self._pas is None:
            raise AttributeError("pas has not been set")
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        self._pas = pas

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError


class EndophoraArgument(BaseArgument):
    """文脈中の句を指す項を表すクラス．

    Args:
        base_phrase: 文脈照応詞．
        arg_type: 項のタイプ．
    """

    def __init__(self, base_phrase: "BasePhrase", arg_type: ArgumentType):
        super().__init__(arg_type)
        self.base_phrase = base_phrase  #: 文脈照応詞．

    @property
    def unit(self) -> "BasePhrase":
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
        return f"<{self.__module__}.{self.__class__.__name__}: {repr(self.base_phrase.text)}>"

    def __str__(self) -> str:
        return self.base_phrase.text

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, EndophoraArgument) and self.base_phrase == other.base_phrase


class ExophoraArgument(BaseArgument):
    """外界を指す項を表すクラス．

    Args:
        exophora_referent: 外界照応詞 (不特定:人など)
        eid: 外界照応詞のエンティティID
    """

    def __init__(self, exophora_referent: ExophoraReferent, eid: int):
        super().__init__(ArgumentType.EXOPHORA)
        self.exophora_referent = exophora_referent  #: 外界照応詞．
        self.eid = eid

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(exophora_referent={repr(self.exophora_referent)}, eid={repr(self.eid)})"

    def __str__(self) -> str:
        return str(self.exophora_referent)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ExophoraArgument) and self.exophora_referent == other.exophora_referent


Argument = Union[EndophoraArgument, ExophoraArgument]
