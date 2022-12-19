import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, Optional

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
        """指定された値が存在すれば True．

        Args:
            value: 談話関係タグ．
        """
        return any(value == item.value for item in cls)

    @property
    def label(self) -> DiscourseRelationLabel:
        """タグに対応する談話関係のラベルを返却．"""
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

    @property
    def need_swap(self) -> bool:
        """談話関係が逆方向であれば True．"""
        return self in {
            DiscourseRelationTag.CAUSE_REASON_BACKWARD,
            DiscourseRelationTag.CAUSE_REASON_BACKWARD2,
            DiscourseRelationTag.PURPOSE_BACKWARD,
            DiscourseRelationTag.CONDITION_BACKWARD,
            DiscourseRelationTag.CONCESSION_BACKWARD,
            DiscourseRelationTag.EVIDENCE_BACKWARD,
        }


@dataclass
class DiscourseRelation:
    """談話関係クラス"""

    CLAUSE_FUNCTION_PAT: ClassVar[re.Pattern] = re.compile(r"節-機能-(?P<label>.+)")
    BACKWARD_CLAUSE_FUNCTION_PAT: ClassVar[re.Pattern] = re.compile(r"節-前向き機能-(?P<label>.+)")
    DISCOURSE_RELATION_PAT: ClassVar[re.Pattern] = re.compile(
        r"(?P<sid>[^/]+)/(?P<base_phrase_index>\d+)/(?P<tag>[^/]+)"
    )

    sid: str  #: 主辞の文ID．
    base_phrase_index: int  #: 主辞の基本句インデックス．
    label: DiscourseRelationLabel  #: 談話関係ラベル．
    tag: DiscourseRelationTag  #: 談話関係タグ．
    modifier: "Clause"  #: 修飾節．
    head: "Clause"  #: 主辞節．
    is_explicit: bool = False  #: 明示的な談話関係ならTrue．．

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.label == other.label and self.modifier == other.modifier and self.head == other.head

    @classmethod
    def from_clause_function_fstring(cls, fstring: str, modifier: "Clause") -> Optional["DiscourseRelation"]:
        """節機能を表す素性文字列から初期化．

        Args:
            fstring: 節機能を表す素性文字列．
            modifier: 修飾節．

        .. note::
            節機能由来で認定された談話関係は明示的 (explicit) とみなす．
        """
        match = cls.CLAUSE_FUNCTION_PAT.match(fstring)
        if match is None:
            return None
        label = match["label"]
        if not DiscourseRelationTag.has_value(label):
            return None
        tag = DiscourseRelationTag(label)
        label = tag.label
        head = modifier.parent
        if head is None:
            return None
        if tag.need_swap:
            # NOTE: Currently, no clause function requires swap.
            modifier, head = head, modifier  # pragma: no cover
        return cls(
            sid=modifier.sentence.sid,
            base_phrase_index=head.end.index,
            label=label,
            tag=tag,
            modifier=modifier,
            head=head,
            is_explicit=True,
        )

    @classmethod
    def from_backward_clause_function_fstring(cls, fstring: str, head: "Clause") -> Optional["DiscourseRelation"]:
        """前向き節機能を表す素性文字列から初期化．

        Args:
            fstring: 前向き節機能を表す素性文字列．
            head: 主節．

        .. note::
            前向き節機能由来で認定された談話関係は明示的 (explicit) とみなす．
        """
        match = cls.BACKWARD_CLAUSE_FUNCTION_PAT.match(fstring)
        if match is None:
            return None
        label = match["label"]
        if not DiscourseRelationTag.has_value(label):
            return None
        tag = DiscourseRelationTag(label)
        label = tag.label
        if head.sentence.has_document is False:
            return None  # cannot find modifier
        if head.sentence.index == 0:
            return None  # cannot find modifier
        modifier = head.sentence.document.sentences[head.sentence.index - 1].clauses[-1]
        if tag.need_swap:
            modifier, head = head, modifier
        return cls(
            sid=head.sentence.sid,
            base_phrase_index=head.end.index,
            label=label,
            tag=tag,
            modifier=modifier,
            head=head,
            is_explicit=True,
        )

    @classmethod
    def from_discourse_relation_fstring(cls, fstring: str, modifier: "Clause") -> Optional["DiscourseRelation"]:
        """談話関係を表す素性文字列から初期化．

        Args:
            fstring: 談話関係を表す素性文字列．
            modifier: 修飾節．
        """
        match = re.match(cls.DISCOURSE_RELATION_PAT, fstring)
        if match is None:
            logger.warning(f"'{fstring}' is not a valid discourse relation fstring")
            return None
        sid = match["sid"]
        base_phrase_index = int(match["base_phrase_index"])
        tag = match["tag"]
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
        if tag.need_swap:
            modifier, head = head, modifier
        return cls(sid, base_phrase_index, category, tag, modifier, head)

    def to_fstring(self) -> str:
        """談話関係を素性文字列に変換する．"""
        return f"<談話関係:{self.sid}/{self.base_phrase_index}/{self.label.value}>"
