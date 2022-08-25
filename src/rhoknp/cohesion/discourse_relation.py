import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Optional

if TYPE_CHECKING:
    from rhoknp import Clause, Sentence

logger = logging.getLogger(__name__)


@dataclass
class DiscourseRelation:
    """談話関係クラス"""

    PAT: ClassVar[re.Pattern] = re.compile(r"(?P<sid>[^/]+)/(?P<base_phrase_index>\d+)/(?P<label>[^/]+)")

    sid: str
    base_phrase_index: int
    label: str
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
        return cls(sid, base_phrase_index, label, modifier, head)

    def to_fstring(self) -> str:
        return f"{self.sid}/{self.base_phrase_index}/{self.label}"
