import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp import Clause, Sentence

logger = logging.getLogger(__name__)


class DiscourseRelationCategory(Enum):
    """談話関係カテゴリを表す列挙体．"""

    NO_RELATION = "談話関係なし"
    CAUSE_REASON = "原因・理由"
    CAUSE_REASON_FORWARD = "原因・理由(順方向)"
    CAUSE_REASON_BACKWARD = "原因・理由(逆方向)"
    PURPOSE = "目的"
    PURPOSE_FORWARD = "目的(順方向)"
    PURPOSE_BACKWARD = "目的(逆方向)"
    CONDITION = "条件"
    CONDITION_FORWARD = "条件(順方向)"
    CONDITION_BACKWARD = "条件(逆方向)"
    CONTRAST = "対比"
    CONTRAST_NO_DIRECTION = "対比(方向なし)"
    CONCESSION = "逆接"
    CONCESSION_FORWARD = "逆接・譲歩(順方向)"
    CONCESSION_BACKWARD = "逆接・譲歩(逆方向)"
    EVIDENCE = "根拠"
    EVIDENCE_FORWARD = "その他根拠(順方向)"
    EVIDENCE_BACKWARD = "その他根拠(逆方向)"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return any(value == item.value for item in cls)


@dataclass
class DiscourseRelation:
    """談話関係クラス"""

    PAT: ClassVar[re.Pattern] = re.compile(r"(?P<sid>[^/]+)/(?P<base_phrase_index>\d+)/(?P<label>[^/]+)")

    sid: str
    base_phrase_index: int
    label: DiscourseRelationCategory
    modifier: "Clause"
    head: "Clause"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.sid}, {self.base_phrase_index}, {self.label})"

    @classmethod
    def from_fstring(cls, fstring: str, modifier: "Clause") -> Optional["DiscourseRelation"]:
        match = re.match(cls.PAT, fstring)
        if match is None:
            logger.warning(f"'{fstring}' is not a valid discourse relation fstring")
            return None
        sid = match.group("sid")
        base_phrase_index = int(match.group("base_phrase_index"))
        label = match.group("label")
        if not DiscourseRelationCategory.has_value(label):
            logger.warning(f"unknown discourse relation label '{label}' found")
            return None
        head_sentence: Optional["Sentence"] = None
        if modifier.sentence.has_document:
            sentences = modifier.document.sentences
        else:
            sentences = [modifier.sentence]
        for sentence in sentences:
            if sentence.sid == sid:
                head_sentence = sentence
                break
        if head_sentence is None:
            logger.warning(f"{sid} not found")
            return None
        if base_phrase_index >= len(head_sentence.base_phrases):
            logger.warning(f"index out of range in {sid}")
            return None
        head_base_phrase = head_sentence.base_phrases[base_phrase_index]
        head = head_base_phrase.clause
        if head.end != head_base_phrase:
            logger.warning(f"invalid clause tag in {sid}")
            return None
        return cls(sid, base_phrase_index, DiscourseRelationCategory(label), modifier, head)

    def to_fstring(self) -> str:
        return f"<談話関係:{self.sid}/{self.base_phrase_index}/{self.label.value}>"
