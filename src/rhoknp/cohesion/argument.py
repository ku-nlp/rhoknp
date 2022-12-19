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

    CASE_EXPLICIT = "C"  #: 直接係り受けをもつ格要素（格は明示されている）．
    CASE_HIDDEN = "N"  #: 直接係り受けをもつ格要素（格は明示されていない）．
    OMISSION = "O"  #: 省略の指示対象．
    DEMONSTRATIVE = "D"  #: 指示詞の指示対象．
    EXOPHORA = "E"  #: 特殊（不特定：人など）．
    UNASSIGNED = "U"  #: 格要素の割り当てなし．


class BaseArgument(ABC):
    """項の基底クラス．"""

    def __init__(self, case: str, arg_type: ArgumentType) -> None:
        self.case: str = case
        self.type: ArgumentType = arg_type
        self.optional: bool = False
        self._pas: Optional["Pas"] = None

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        raise NotImplementedError

    @property
    def is_special(self) -> bool:
        """外界照応なら True．"""
        return self.type == ArgumentType.EXOPHORA

    @property
    def pas(self) -> "Pas":
        """述語項構造．"""
        assert self._pas is not None
        return self._pas

    @pas.setter
    def pas(self, pas: "Pas") -> None:
        """述語項構造．"""
        self._pas = pas


class EndophoraArgument(BaseArgument):
    """文脈中の句を指す項を表すクラス．

    Args:
        base_phrase: 照応詞が指す基本句．
        arg_type: 項のタイプ．
    """

    def __init__(self, case: str, base_phrase: "BasePhrase", arg_type: ArgumentType) -> None:
        super().__init__(case, arg_type)
        self.base_phrase = base_phrase  #: 項の核となる基本句．

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {repr(self.case)}, {repr(self.base_phrase.text)}>"

    def __str__(self) -> str:
        return self.base_phrase.text

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False:
            return False
        if self._pas is not None and other._pas is not None:
            if self.pas.predicate != other.pas.predicate:
                return False
        return self.case == other.case and self.base_phrase == other.base_phrase

    @property
    def document(self) -> "Document":
        """項の核となる基本句が属する文書．"""
        return self.base_phrase.document

    @property
    def sentence(self) -> "Sentence":
        """項の核となる基本句が属する文．"""
        return self.base_phrase.sentence

    @property
    def clause(self) -> "Clause":
        """項の核となる基本句が属する節．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.base_phrase.clause

    @property
    def phrase(self) -> "Phrase":
        """項の核となる基本句が属する文節．"""
        return self.base_phrase.phrase


class ExophoraArgument(BaseArgument):
    """外界を指す項を表すクラス．

    Args:
        exophora_referent: 外界照応における照応先（不特定:人など）．
        eid: エンティティID．
    """

    def __init__(self, case: str, exophora_referent: ExophoraReferent, eid: int) -> None:
        super().__init__(case, ArgumentType.EXOPHORA)
        self.exophora_referent = exophora_referent  #: 外界照応における照応先．
        self.eid = eid  #: エンティティID．

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(case={repr(self.case)}, exophora_referent={repr(self.exophora_referent)}, "
            f"eid={repr(self.eid)})"
        )

    def __str__(self) -> str:
        return str(self.exophora_referent)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False:
            return False
        if self._pas is not None and other._pas is not None:
            if self.pas.predicate != other.pas.predicate:
                return False
        return self.case == other.case and self.exophora_referent == other.exophora_referent


Argument = Union[EndophoraArgument, ExophoraArgument]
