import logging
import re
from functools import cached_property
from typing import TYPE_CHECKING, Optional

from rhoknp.rel.coreference import Entity, EntityManager
from rhoknp.rel.exophora import ExophoraReferent
from rhoknp.rel.pas import CaseInfoFormat, Pas
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

logger = logging.getLogger(__name__)


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
            morpheme.base_phrase = self
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
        """nonidentical も含めた参照している全エンティティの集合．"""
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
        if self.rels or self.features:
            ret += f" {self.rels.to_fstring()}{self.features.to_fstring()}"
        ret += "\n"
        ret += "".join(morpheme.to_jumanpp() for morpheme in self.morphemes)
        return ret

    def get_coreferents(self, include_nonidentical: bool = False, include_self: bool = False) -> set["BasePhrase"]:
        """この基本句と共参照している基本句の集合を返却．

        Args:
            include_nonidentical: nonidentical なメンションを含めるなら True．
            include_self: 自身を含めるなら True．

        Returns:
            共参照している基本句の集合．
        """
        mentions: set["BasePhrase"] = set()
        for entity in self.entities:
            mentions.update(entity.mentions)
        if include_nonidentical is True:
            for entity in self.entities_nonidentical:
                mentions.update(entity.mentions)
        if include_self is False and self in mentions:
            mentions.remove(self)
        return mentions

    def is_nonidentical_to(self, entity: Entity) -> bool:
        """エンティティに対して自身が nonidentical な場合に True を返す．

        Raises:
            AssertionError: 自身が参照しないエンティティだった場合．
        """
        if entity in self.entities:
            return False
        else:
            assert entity in self.entities_nonidentical, f"non-referring entity: {entity}"
            return True

    def add_entity(self, entity: Entity, nonidentical: bool = False) -> None:
        """エンティティを追加．"""
        if nonidentical:
            self.entities_nonidentical.add(entity)
        else:
            self.entities.add(entity)
        entity.add_mention(self, nonidentical=nonidentical)

    def parse_rel(self) -> None:
        """関係タグ付きコーパスにおける <rel> タグをパース．"""
        if not self.rels:
            return
        self.pas = Pas(Predicate(self))
        for rel in self.rels:
            if rel.sid == "":
                logger.warning(f"empty sid found in {self.sentence.sid}; assume to be self")
                rel.sid = self.sentence.sid
            if rel.type in ALL_CASES:
                self._add_pas(rel)
            elif rel.type in ALL_COREFS:
                if rel.mode in (None, RelMode.AND):  # ignore "OR" and "?"
                    self._add_coreference(rel)
            else:
                logger.warning(f"unknown rel type: {rel.type}")

    def parse_knp_pas(self) -> None:
        """KNP 解析結果における <述語項構造> タグおよび <格解析結果> タグをパース．"""
        if "述語項構造" in self.features:
            pas_string = self.features["述語項構造"]
            assert isinstance(pas_string, str)
            pas = Pas.from_pas_string(self, pas_string, format_=CaseInfoFormat.PAS)
        elif "格解析結果" in self.features:
            pas_string = self.features["格解析結果"]
            assert isinstance(pas_string, str)
            pas = Pas.from_pas_string(self, pas_string, format_=CaseInfoFormat.CASE)
        else:
            pas = Pas(Predicate(self))
        self.pas = pas

    def reset_rels(self) -> None:
        """PAS と共参照関係をリセット．"""
        self.pas = None
        for entity in self.entities_all:
            entity.remove_mention(self)

    def _add_pas(self, rel: Rel) -> None:
        """述語項構造を追加．"""
        entity_manager: EntityManager = self.document.entity_manager
        assert self.pas is not None
        if rel.sid is not None:
            if (arg_base_phrase := self._get_target_base_phrase(rel)) is None:
                return
            if not arg_base_phrase.entities:
                arg_base_phrase.add_entity(entity_manager.get_or_create_entity())
            self.pas.add_argument(rel.type, arg_base_phrase, mode=rel.mode)
        else:
            if rel.target == "なし":
                self.pas.set_arguments_optional(rel.type)
                return
            # exophora
            entity = entity_manager.get_or_create_entity(ExophoraReferent(rel.target))
            self.pas.add_special_argument(rel.type, rel.target, eid=entity.eid, mode=rel.mode)

    def _add_coreference(self, rel: Rel) -> None:
        """共参照関係を追加．"""
        entity_manager: EntityManager = self.document.entity_manager
        # create source entity
        if not self.entities:
            self.add_entity(entity_manager.get_or_create_entity())

        nonidentical: bool = rel.type.endswith("≒")
        if rel.sid is not None:
            if (target_base_phrase := self._get_target_base_phrase(rel)) is None:
                return
            if target_base_phrase == self:
                logger.warning(f"{self.sentence.sid}: coreference with self found: {self}")
                return
            # create target entity
            if not target_base_phrase.entities:
                target_base_phrase.add_entity(entity_manager.get_or_create_entity())
            for source_entity in self.entities_all:
                for target_entity in target_base_phrase.entities_all:
                    entity_manager.merge_entities(self, target_base_phrase, source_entity, target_entity, nonidentical)
        else:
            # exophora
            for source_entity in self.entities_all:
                target_entity = entity_manager.get_or_create_entity(exophora_referent=ExophoraReferent(rel.target))
                entity_manager.merge_entities(self, None, source_entity, target_entity, nonidentical)

    def _get_target_base_phrase(self, rel: Rel) -> Optional["BasePhrase"]:
        sentence = next(sent for sent in self.document.sentences if sent.sid == rel.sid)
        assert rel.base_phrase_index is not None
        if rel.base_phrase_index >= len(sentence.base_phrases):
            logger.warning(f"index out of range in {self.sentence.sid}")
            return None
        target_base_phrase = sentence.base_phrases[rel.base_phrase_index]
        if not (set(rel.target) <= set(target_base_phrase.text)):
            logger.info(f"rel target mismatch; '{rel.target}' is not '{target_base_phrase.text}'")
        return target_base_phrase

    def __hash__(self) -> int:
        return hash((self.global_index, self.sentence.sid))
