import re
import weakref
from functools import cached_property
from logging import getLogger
from typing import TYPE_CHECKING, Optional

from rhoknp.rel.coreference import Entity, EntityManager
from rhoknp.rel.exophora import ExophoraReferent
from rhoknp.rel.pas import Pas
from rhoknp.rel.predicate import Predicate
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.unit import Unit
from rhoknp.units.utils import DepType, Features, Rel, RelMode, Rels
from rhoknp.utils.constants import ALL_CASES, ALL_COREFS

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.phrase import Phrase
    from rhoknp.units.sentence import Sentence

logger = getLogger(__file__)


class BasePhrase(Unit):
    """基本句クラス．"""

    KNP_PAT = re.compile(
        rf"^\+ (?P<pid>-1|\d+)(?P<dtype>[{''.join(e.value for e in DepType)}])( (?P<tags>(<[^>]+>)*))?$"
    )
    count = 0

    def __init__(self, parent_index: int, dep_type: DepType, features: Features, rels: Rels):
        super().__init__()

        # parent unit
        self._phrase: Optional["Phrase"] = None

        # child units
        self._morphemes: Optional[list[Morpheme]] = None

        self.parent_index: int = parent_index  #: 係り先の基本句の文内におけるインデックス．
        self.dep_type: DepType = dep_type  #: 係り受けの種類．
        self.features: Features = features  #: 素性．
        self.rels: Rels = rels  #: 基本句間関係．
        self.pas: Optional["Pas"] = None  #: 述語項構造．
        self.entities: set[Entity] = set()  #: 参照しているエンティティ．
        self.entities_nonidentical: set[Entity] = set()  #: ≒で参照しているエンティティ．

        self.index = self.count
        BasePhrase.count += 1

    @property
    def global_index(self) -> int:
        """文書全体におけるインデックス．"""
        offset = 0
        for prev_sentence in self.document.sentences[: self.sentence.index]:
            offset += len(prev_sentence.base_phrases)
        return self.index + offset

    @property
    def parent_unit(self) -> Optional["Phrase"]:
        """上位の言語単位（文節）．未登録なら None．"""
        return self._phrase

    @property
    def child_units(self) -> Optional[list[Morpheme]]:
        """下位の言語単位（形態素）．解析結果にアクセスできないなら None．"""
        return self._morphemes

    @property
    def document(self) -> "Document":
        """文書．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.phrase.document

    @property
    def sentence(self) -> "Sentence":
        """文．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.phrase.sentence

    @property
    def clause(self) -> "Clause":
        """節．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return self.phrase.clause

    @property
    def phrase(self) -> "Phrase":
        """文節．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self._phrase is None:
            raise AttributeError("phrase has not been set")
        return self._phrase

    @phrase.setter
    def phrase(self, phrase: "Phrase") -> None:
        """文節．

        Args:
            phrase: 文節．
        """
        self._phrase = phrase

    @property
    def morphemes(self) -> list[Morpheme]:
        """形態素．"""
        if self._morphemes is None:
            raise AssertionError
        return self._morphemes

    @morphemes.setter
    def morphemes(self, morphemes: list[Morpheme]) -> None:
        """形態素．

        Args:
            morphemes: 形態素．
        """
        for morpheme in morphemes:
            morpheme.base_phrase = weakref.proxy(self)
        self._morphemes = morphemes

    @cached_property
    def head(self) -> Morpheme:
        """主辞の形態素．"""
        head = None
        for morpheme in self.morphemes:
            if morpheme.features is None:
                continue
            if "内容語" in morpheme.features and head is None:
                # Consider the first content word as the head
                head = morpheme
            if "準内容語" in morpheme.features:
                # Sub-content words overwrite the head
                head = morpheme
        if head:
            return head
        return self.morphemes[0]

    @property
    def parent(self) -> Optional["BasePhrase"]:
        """係り先の基本句．ないなら None．"""
        if self.parent_index == -1:
            return None
        return self.sentence.base_phrases[self.parent_index]

    @cached_property
    def children(self) -> list["BasePhrase"]:
        """この基本句に係っている基本句のリスト．"""
        return [base_phrase for base_phrase in self.sentence.base_phrases if base_phrase.parent == self]

    @property
    def entities_all(self) -> set[Entity]:
        return self.entities | self.entities_nonidentical

    @classmethod
    def from_knp(cls, knp_text: str) -> "BasePhrase":
        """基本句クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
        """
        first_line, *lines = knp_text.split("\n")
        match = cls.KNP_PAT.match(first_line)
        if match is None:
            raise ValueError(f"malformed line: {first_line}")
        parent_index = int(match.group("pid"))
        dep_type = DepType(match.group("dtype"))
        features = Features(match.group("tags") or "")
        rels = Rels.from_fstring(match.group("tags") or "")
        base_phrase = cls(parent_index, dep_type, features, rels)

        morphemes: list[Morpheme] = []
        for line in lines:
            if not line.strip():
                continue
            morphemes.append(Morpheme.from_jumanpp(line))
        base_phrase.morphemes = morphemes
        return base_phrase

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = f"+ {self.parent_index}{self.dep_type.value}"
        if self.features:
            ret += f" {self.features}"
        ret += "\n"
        ret += "".join(morpheme.to_jumanpp() for morpheme in self.morphemes)
        return ret

    def is_nonidentical_to(self, entity: Entity) -> bool:
        """Whether this mention has uncertain relation with a specified entity."""
        if entity in self.entities:
            return False
        else:
            assert entity in self.entities_nonidentical, f"non-referring entity: {entity}"
            return True

    def parse_rel(self) -> None:
        """関係タグ付きコーパスにおける <rel> タグをパース．"""
        entity_manager: EntityManager = self.document.entity_manager
        # extract PAS
        pas = Pas(Predicate(self))
        for rel in self.rels:
            if rel.type not in ALL_CASES:
                continue
            if rel.sid == "":
                logger.warning(f"empty sid found in {self.sentence.sid}; assume to be self")
                rel.sid = self.sentence.sid
            if rel.sid is not None:
                sentence = next(sent for sent in self.document.sentences if sent.sid == rel.sid)
                assert rel.base_phrase_index is not None
                if rel.base_phrase_index >= len(sentence.base_phrases):
                    logger.warning(f"index out of range in {self.sentence.sid}")
                    continue
                arg_base_phrase = sentence.base_phrases[rel.base_phrase_index]
                if not (set(rel.target) <= set(arg_base_phrase.text)):
                    logger.info(f"rel target mismatch; '{rel.target}' is not '{arg_base_phrase.text}'")
                if not arg_base_phrase.entities:
                    entity = entity_manager.create_entity()
                    entity.add_mention(arg_base_phrase)
                pas.add_argument(rel.type, arg_base_phrase, mode=rel.mode)
            else:
                if rel.target == "なし":
                    pas.set_arguments_optional(rel.type)
                    continue
                # exophora
                entity = entity_manager.create_entity(ExophoraReferent(rel.target))
                pas.add_special_argument(rel.type, rel.target, eid=entity.eid, mode=rel.mode)
        self.pas = pas

        # extract coreference
        for rel in self.rels:
            if rel.type not in ALL_COREFS:
                continue
            if rel.mode in (None, RelMode.AND):  # ignore "OR" and "?"
                self._add_coreference(rel)

    def _add_coreference(self, rel: Rel) -> None:
        """Add a coreference relation."""
        entity_manager: EntityManager = self.document.entity_manager
        target_base_phrase: Optional[BasePhrase]
        if rel.sid is not None:
            sentence = next(sent for sent in self.document.sentences if sent.sid == rel.sid)
            assert rel.base_phrase_index is not None
            if rel.base_phrase_index >= len(sentence.base_phrases):
                logger.warning(f"index out of range in {self.sentence.sid}")
                return
            target_base_phrase = sentence.base_phrases[rel.base_phrase_index]
            if target_base_phrase.global_index == self.global_index:
                logger.warning(f"{self.sentence.sid}: coreference with self found: {self}")
                return
            # create target entity
            if not target_base_phrase.entities:
                target_entity = entity_manager.create_entity()
                target_entity.add_mention(target_base_phrase)
                target_base_phrase.entities.add(target_entity)
        else:
            # exophora
            target_base_phrase = None

        # create source entity
        if not self.entities:
            source_entity = entity_manager.create_entity()
            source_entity.add_mention(self)
            self.entities.add(source_entity)

        nonidentical: bool = rel.type.endswith("≒")
        for source_entity in self.entities_all:
            if rel.sid is not None:
                assert target_base_phrase is not None
                for target_entity in target_base_phrase.entities_all:
                    entity_manager.merge_entities(self, target_base_phrase, source_entity, target_entity, nonidentical)
            else:
                target_entity = entity_manager.create_entity(exophora_referent=ExophoraReferent(rel.target))
                entity_manager.merge_entities(self, None, source_entity, target_entity, nonidentical)

    def __hash__(self):
        return hash((self.global_index, self.sentence.sid))
