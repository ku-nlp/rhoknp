import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp import Clause, Sentence

logger = logging.getLogger(__name__)


class DiscourseRelationLabel(Enum):
    """談話関係ラベルを表す列挙体．"""

    NO_RELATION = "談話関係なし"
    CAUSE_REASON = "原因・理由"
    PURPOSE = "目的"
    CONDITION = "条件"
    EVIDENCE = "根拠"
    CONTRAST = "対比"
    CONCESSION = "逆接"


class DiscourseRelationTag(Enum):
    """談話関係タグを表す列挙体．"""

    NO_RELATION = "談話関係なし"
    CAUSE_REASON = "原因・理由"
    CAUSE_REASON_FORWARD = "原因・理由(順方向)"
    CAUSE_REASON_BACKWARD = "原因・理由(逆方向)"
    CAUSE_REASON_BACKWARD2 = "原因・理由-逆"
    PURPOSE = "目的"
    PURPOSE_FORWARD = "目的(順方向)"
    PURPOSE_BACKWARD = "目的(逆方向)"
    CONDITION = "条件"
    CONDITION_FORWARD = "条件(順方向)"
    CONDITION_BACKWARD = "条件(逆方向)"
    NEGATIVE_CONDITION = "否定条件"
    CONTRAST = "対比"
    CONTRAST_NO_DIRECTION = "対比(方向なし)"
    CONCESSION = "逆接"
    CONCESSION_FORWARD = "逆接・譲歩(順方向)"
    CONCESSION_BACKWARD = "逆接・譲歩(逆方向)"
    CONCESSIVE_CONDITION = "条件-逆条件"
    EVIDENCE = "根拠"
    EVIDENCE_FORWARD = "その他根拠(順方向)"
    EVIDENCE_BACKWARD = "その他根拠(逆方向)"

    @classmethod
    def has_value(cls, value: str) -> bool:
        return any(value == item.value for item in cls)

    @property
    def label(self) -> DiscourseRelationLabel:
        if self in {
            DiscourseRelationTag.NO_RELATION,
        }:
            return DiscourseRelationLabel.NO_RELATION
        elif self in {
            DiscourseRelationTag.CAUSE_REASON,
            DiscourseRelationTag.CAUSE_REASON_FORWARD,
            DiscourseRelationTag.CAUSE_REASON_BACKWARD,
            DiscourseRelationTag.CAUSE_REASON_BACKWARD2,
        }:
            return DiscourseRelationLabel.CAUSE_REASON
        elif self in {
            DiscourseRelationTag.PURPOSE,
            DiscourseRelationTag.PURPOSE_FORWARD,
            DiscourseRelationTag.PURPOSE_BACKWARD,
        }:
            return DiscourseRelationLabel.PURPOSE
        elif self in {
            DiscourseRelationTag.CONDITION,
            DiscourseRelationTag.CONDITION_FORWARD,
            DiscourseRelationTag.CONDITION_BACKWARD,
            DiscourseRelationTag.NEGATIVE_CONDITION,
        }:
            return DiscourseRelationLabel.CONDITION
        elif self in {
            DiscourseRelationTag.CONTRAST,
            DiscourseRelationTag.CONTRAST_NO_DIRECTION,
        }:
            return DiscourseRelationLabel.CONTRAST
        elif self in {
            DiscourseRelationTag.CONCESSION,
            DiscourseRelationTag.CONCESSION_FORWARD,
            DiscourseRelationTag.CONCESSION_BACKWARD,
            DiscourseRelationTag.CONCESSIVE_CONDITION,
        }:
            return DiscourseRelationLabel.CONCESSION
        elif self in {
            DiscourseRelationTag.EVIDENCE,
            DiscourseRelationTag.EVIDENCE_FORWARD,
            DiscourseRelationTag.EVIDENCE_BACKWARD,
        }:
            return DiscourseRelationLabel.EVIDENCE
        raise AssertionError  # unreachable


@dataclass
class DiscourseRelation:
    """談話関係クラス"""

    CLAUSE_FUNCTION_PAT: ClassVar[re.Pattern] = re.compile(r"節-機能-(?P<label>.+)")
    DISCOURSE_RELATION_PAT: ClassVar[re.Pattern] = re.compile(
        r"(?P<sid>[^/]+)/(?P<base_phrase_index>\d+)/(?P<tag>[^/]+)"
    )

    sid: str
    base_phrase_index: int
    label: DiscourseRelationLabel
    tag: DiscourseRelationTag
    modifier: "Clause"
    head: "Clause"
    explicit: bool = False

    @classmethod
    def from_clause_function_fstring(cls, fstring: str, modifier: "Clause") -> Optional["DiscourseRelation"]:
        match = cls.CLAUSE_FUNCTION_PAT.match(fstring)
        if match is None:
            return None
        label = match.group("label")
        if not DiscourseRelationTag.has_value(label):
            return None
        tag = DiscourseRelationTag(label)
        label = tag.label
        head = modifier.parent
        if head is None:
            return None
        return cls(
            sid=modifier.sentence.sid if modifier.sentence.sid is not None else str(modifier.sentence.index),
            base_phrase_index=head.end.index,
            label=label,
            tag=tag,
            modifier=modifier,
            head=modifier,
            explicit=True,
        )

    @classmethod
    def from_discourse_relation_fstring(cls, fstring: str, modifier: "Clause") -> Optional["DiscourseRelation"]:
        match = re.match(cls.DISCOURSE_RELATION_PAT, fstring)
        if match is None:
            logger.warning(f"'{fstring}' is not a valid discourse relation fstring")
            return None
        sid = match.group("sid")
        base_phrase_index = int(match.group("base_phrase_index"))
        tag = match.group("tag")
        if not DiscourseRelationTag.has_value(tag):
            logger.warning(f"unknown discourse relation label '{tag}' found")
            return None
        tag = DiscourseRelationTag(tag)
        category = tag.label
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
        return cls(sid, base_phrase_index, category, tag, modifier, head)

    def to_fstring(self) -> str:
        return f"<談話関係:{self.sid}/{self.base_phrase_index}/{self.label.value}>"
