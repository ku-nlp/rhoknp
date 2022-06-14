import re
from enum import Enum
from logging import getLogger
from typing import Any, ClassVar, Optional

logger = getLogger(__file__)


class ExophoraReferentType(Enum):
    WRITER = "著者"
    READER = "読者"
    UNSPECIFIED_PERSON = "不特定:人"
    UNSPECIFIED_MATTER = "不特定:物"
    UNSPECIFIED_SITUATION = "不特定:状況"
    PREVIOUS_SENTENCE = "前文"
    NEXT_SENTENCE = "後文"
    OTHER = "OTHER"


class ExophoraReferent:
    """外界照応における照応先を表すクラス．"""

    PAT: ClassVar[re.Pattern[str]] = re.compile(
        rf"^(?P<type>{'|'.join(t.value for t in ExophoraReferentType if t != ExophoraReferentType.OTHER)})"
        rf"(?P<index>[０-９\d]*)$"
    )

    def __init__(self, text: str) -> None:
        self.index: Optional[int] = None
        self._other_text: Optional[str] = None
        match: Optional[re.Match[str]] = self.PAT.match(text)
        if match is None:
            logger.warning(f"unknown exophora referent found: {text}")
            self.type = ExophoraReferentType.OTHER
            self._other_text = text
        else:
            if index := match.group("index"):
                self.index = int(index)
            self.type = ExophoraReferentType(match.group("type"))

    @property
    def text(self) -> str:
        """外界照応の照応先を表すテキスト表現．"""
        if self.type != ExophoraReferentType.OTHER:
            return self.type.value + str(self.index or "")
        else:
            assert self._other_text is not None
            return self._other_text

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text={repr(self.text)})"

    def __eq__(self, other: Any):
        return (
            isinstance(other, type(self))
            and self.type == other.type != ExophoraReferentType.OTHER
            and self.index == other.index
        )
