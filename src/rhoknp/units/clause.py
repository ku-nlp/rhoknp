import logging
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional

from rhoknp.cohesion.discourse import DiscourseRelation
from rhoknp.units.base_phrase import BasePhrase
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.phrase import Phrase
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.document import Document
    from rhoknp.units.sentence import Sentence

logger = logging.getLogger(__name__)


class Clause(Unit):
    """節クラス．"""

    count = 0

    def __init__(self) -> None:
        super().__init__()

        # parent unit
        self._sentence: Optional["Sentence"] = None

        # child units
        self._phrases: Optional[List[Phrase]] = None

        self.discourse_relations: List[DiscourseRelation] = []  #: 談話関係のリスト．

        self.index = self.count  #: 文内におけるインデックス．
        Clause.count += 1

    def __post_init__(self) -> None:
        super().__post_init__()

        # Find discourse relations.
        for key in self.end.features:
            if key.startswith("節-機能"):
                if relation := DiscourseRelation.from_clause_function_fstring(key, modifier=self):
                    if relation not in relation.modifier.discourse_relations:
                        relation.modifier.discourse_relations.append(relation)
        for base_phrase in self.base_phrases:
            for key in base_phrase.features:
                if key.startswith("節-前向き機能"):
                    if base_phrase.parent is None or base_phrase.parent in self.base_phrases:
                        head = self
                    else:
                        head = base_phrase.parent.clause
                    if relation := DiscourseRelation.from_backward_clause_function_fstring(key, head=head):
                        if relation not in relation.modifier.discourse_relations:
                            relation.modifier.discourse_relations.append(relation)
        if values := self.end.features.get("談話関係", None):
            assert isinstance(values, str)
            for value in values.split(";"):
                if relation := DiscourseRelation.from_discourse_relation_fstring(value, modifier=self):
                    if relation not in relation.modifier.discourse_relations:
                        relation.modifier.discourse_relations.append(relation)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)) is False:
            return False
        if self.parent_unit != other.parent_unit:
            return False
        return self.index == other.index

    @cached_property
    def global_index(self) -> int:
        """文書全体におけるインデックス．"""
        if self.index > 0:
            return self.sentence.clauses[self.index - 1].global_index + 1
        if self.sentence.index == 0:
            return self.index
        return self.document.sentences[self.sentence.index - 1].clauses[-1].global_index + 1

    @property
    def parent_unit(self) -> Optional["Sentence"]:
        """上位の言語単位（文）．未登録なら None．"""
        return self._sentence

    @property
    def child_units(self) -> Optional[List[Phrase]]:
        """下位の言語単位（文節）．解析結果にアクセスできないなら None．"""
        return self._phrases

    @property
    def document(self) -> "Document":
        """文書．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.sentence.document

    @property
    def sentence(self) -> "Sentence":
        """文．"""
        assert self._sentence is not None
        return self._sentence

    @sentence.setter
    def sentence(self, sentence: "Sentence") -> None:
        """文．

        Args:
            sentence: 文．
        """
        self._sentence = sentence

    @property
    def phrases(self) -> List[Phrase]:
        """文節のリスト．"""
        assert self._phrases is not None
        return self._phrases

    @phrases.setter
    def phrases(self, phrases: List[Phrase]) -> None:
        """文節のリスト．

        Args:
            phrases: 文節のリスト．
        """
        for phrase in phrases:
            phrase.clause = self
        self._phrases = phrases

    @property
    def base_phrases(self) -> List[BasePhrase]:
        """基本句のリスト．"""
        return [base_phrase for phrase in self.phrases for base_phrase in phrase.base_phrases]

    @property
    def morphemes(self) -> List[Morpheme]:
        """形態素のリスト．"""
        return [morpheme for base_phrase in self.base_phrases for morpheme in base_phrase.morphemes]

    @cached_property
    def head(self) -> BasePhrase:
        """節主辞の基本句．"""
        heads: List[BasePhrase] = []
        for base_phrase in self.base_phrases:
            if "節-主辞" in base_phrase.features:
                heads.append(base_phrase)
        if len(heads) == 1:
            return heads[0]
        elif len(heads) > 1:
            logger.warning("found multiple heads in a clause; use the last base phrase as the head")
            return heads[-1]
        else:
            logger.warning("found no head in a clause; use the last base phrase as the head")
            return self.base_phrases[-1]

    @property
    def end(self) -> BasePhrase:
        """節区切の基本句．"""
        return self.base_phrases[-1]

    @cached_property
    def parent(self) -> Optional["Clause"]:
        """係り先の節．ないなら None．"""
        head_parent = self.head.parent
        while head_parent in self.base_phrases:
            head_parent = head_parent.parent
        for clause in self.sentence.clauses:
            if head_parent in clause.base_phrases:
                return clause
        return None

    @cached_property
    def children(self) -> List["Clause"]:
        """この節に係っている節のリスト．"""
        return [clause for clause in self.sentence.clauses if clause.parent == self]

    @cached_property
    def is_adnominal(self) -> bool:
        """連体修飾節なら True．"""
        return self.end.features.get("節-区切", "") == "連体修飾"

    @cached_property
    def is_sentential_complement(self) -> bool:
        """補文節なら True．"""
        return self.end.features.get("節-区切", "") == "補文"

    @classmethod
    def from_knp(cls, knp_text: str) -> "Clause":
        """節クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
        """
        clause = cls()
        phrases = []
        phrase_lines: List[str] = []
        for line in knp_text.split("\n"):
            if not line.strip():
                continue
            if Phrase.is_phrase_line(line) and phrase_lines:
                phrases.append(Phrase.from_knp("\n".join(phrase_lines)))
                phrase_lines = []
            phrase_lines.append(line)
        else:
            phrase = Phrase.from_knp("\n".join(phrase_lines))
            phrases.append(phrase)
        clause.phrases = phrases
        return clause

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        return "".join(phrase.to_knp() for phrase in self.phrases)
