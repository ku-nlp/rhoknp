import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp import Clause, Sentence

logger = logging.getLogger(__name__)


@dataclass
class DiscourseRelation:
    PAT: ClassVar[re.Pattern[str]] = re.compile(r"(?P<sid>.+?)/(?P<base_phrase_index>\d+?)/(?P<label>[^;]+);?")
    sid: str
    base_phrase_index: int
    label: str
    modifier: Optional["Clause"] = None
    head: Optional["Clause"] = None

    def tie_units(self, clause: "Clause") -> None:
        """言語単位を紐付ける．"""
        modifier = clause
        head_sentence: Optional["Sentence"] = None
        if clause.sentence.has_document:
            sentences = clause.document.sentences
        else:
            sentences = [clause.sentence]
        for sentence in sentences:
            if sentence.sid == self.sid:
                head_sentence = sentence
                break
        if head_sentence is None:
            logger.warning(f"{self.sid} not found")
            return
        if self.base_phrase_index >= len(head_sentence.base_phrases):
            logger.warning(f"index out of range in {self.sid}")
            return
        head_base_phrase = head_sentence.base_phrases[self.base_phrase_index]
        head = head_base_phrase.clause
        if head.end != head_base_phrase:
            logger.warning(f"invalid clause tag in {self.sid}")
            return
        self.modifier = modifier
        self.head = head

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return f"{self.sid}/{self.base_phrase_index}/{self.label}"

    def __str__(self) -> str:
        return self.to_fstring()


class DiscourseRelationList(list[DiscourseRelation]):
    @classmethod
    def from_fstring(cls, fstring: str) -> "DiscourseRelationList":
        """素性文字列から初期化．

        Args:
            fstring: KNP 形式における素性文字列．

        Returns: DiscourseRelationList オブジェクト．

        """
        discourse_relations = cls()
        for match in DiscourseRelation.PAT.finditer(fstring):
            sid = match["sid"]
            base_phrase_index = int(match["base_phrase_index"])
            label = match["label"]
            discourse_relations.append(DiscourseRelation(sid, base_phrase_index, label))
        return discourse_relations

    def tie_units(self, clause: "Clause", drop_untied_relation: bool = True) -> None:
        """言語単位を紐付ける．"""
        for discourse_relation in reversed(self):  # To keep indexes
            discourse_relation.tie_units(clause)
            if drop_untied_relation and (discourse_relation.modifier is None or discourse_relation.head is None):
                self.remove(discourse_relation)

    def to_fstring(self) -> str:
        """素性文字列に変換．"""
        return ";".join(map(str, self))

    def __str__(self) -> str:
        return self.to_fstring()
