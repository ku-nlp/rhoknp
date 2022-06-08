import re
from enum import Enum
from typing import ClassVar, Optional


class ExophoraReferentType(Enum):
    WRITER = "著者"
    READER = "読者"
    UNSPECIFIED_PERSON = "不特定:人"
    UNSPECIFIED_MATTER = "不特定:物"
    UNSPECIFIED_SITUATION = "不特定:状況"
    PREVIOUS_SENTENCE = "前文"
    NEXT_SENTENCE = "後文"


class ExophoraReferent:
    _HAN2ZEN: dict[str, str] = {
        "0": "０",
        "1": "１",
        "2": "２",
        "3": "３",
        "4": "４",
        "5": "５",
        "6": "６",
        "7": "７",
        "8": "８",
        "9": "９",
    }
    PAT: ClassVar[re.Pattern[str]] = re.compile(
        rf"^(?P<type>{'|'.join(t.value for t in ExophoraReferentType)})(?P<index>[0-9０-９]*)$"
    )

    def __init__(self, text: str) -> None:
        match: Optional[re.Match[str]] = self.PAT.match(text)
        if match is None:
            raise ValueError(f"invalid exophora referent: {text}")
        self.index: Optional[int] = (
            int(match.group("index")) if match.group("index") else None
        )
        self.type = ExophoraReferentType(match.group("type"))

    @property
    def text(self) -> str:
        return self.type.value + "".join(
            self._HAN2ZEN[s] for s in str(self.index or "")
        )

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(text={repr(self.text)})"
