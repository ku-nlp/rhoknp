import logging
import re
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional, Set

from rhoknp.cohesion.coreference import Entity
from rhoknp.cohesion.exophora import ExophoraReferent
from rhoknp.cohesion.pas import CaseInfoFormat, Pas
from rhoknp.cohesion.predicate import Predicate
from rhoknp.cohesion.rel import CASE_TYPES, COREF_TYPES, RelMode, RelTag, RelTagList
from rhoknp.props.dependency import DepType
from rhoknp.props.feature import FeatureDict
from rhoknp.props.memo import MemoTag
from rhoknp.units.morpheme import Morpheme
from rhoknp.units.unit import Unit

if TYPE_CHECKING:
    from rhoknp.units.clause import Clause
    from rhoknp.units.document import Document
    from rhoknp.units.phrase import Phrase
    from rhoknp.units.sentence import Sentence

logger = logging.getLogger(__name__)


class BasePhrase(Unit):
    """基本句クラス．"""

    PAT = re.compile(
        rf"^\+( (?P<pid>-1|\d+)(?P<dtype>[{''.join(e.value for e in DepType)}]))?( {FeatureDict.PAT.pattern})?$"
    )
    count = 0

    def __init__(
        self,
        parent_index: Optional[int],
        dep_type: Optional[DepType],
        features: Optional[FeatureDict] = None,
        rel_tags: Optional[RelTagList] = None,
        memo_tag: Optional[MemoTag] = None,
    ) -> None:
        super().__init__()

        # parent unit
        self._phrase: Optional["Phrase"] = None

        # child units
        self._morphemes: Optional[List[Morpheme]] = None

        self.parent_index: Optional[int] = parent_index  #: 係り先の基本句の文内におけるインデックス．
        self.dep_type: Optional[DepType] = dep_type  #: 係り受けの種類．
        self.features: FeatureDict = features or FeatureDict()  #: 素性．
        self.rel_tags: RelTagList = rel_tags or RelTagList()  #: 基本句間関係．
        self.memo_tag: MemoTag = memo_tag or MemoTag()  #: タグ付けメモ．
        self.pas: Optional["Pas"] = None  #: 述語項構造．
        self.entities: Set[Entity] = set()  #: 参照しているエンティティ．
        self.entities_nonidentical: Set[Entity] = set()  #: ≒で参照しているエンティティ．

        self.index = self.count  #: 文内におけるインデックス．
        BasePhrase.count += 1

    def __post_init__(self) -> None:
        super().__post_init__()

        # Parse the PAS tag.
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

        # Parse the rel tag if this unit is a piece of a document.
        if self.sentence.has_document is False:
            logger.info("post-processing of rel tags was skipped because there is no document.")
            return
        for rel_tag in self.rel_tags:
            if rel_tag.sid == "":
                rel_tag = RelTag(
                    type=rel_tag.type,
                    target=rel_tag.target,
                    sid=self.sentence.sid,  # The target is considered to be in the same sentence.
                    base_phrase_index=rel_tag.base_phrase_index,
                    mode=rel_tag.mode,
                )
            if rel_tag.type in CASE_TYPES:
                self._add_pas(rel_tag)
            elif rel_tag.type in COREF_TYPES and rel_tag.mode in (None, RelMode.AND):  # ignore "OR" and "?"
                self._add_coreference(rel_tag)
            else:
                logger.warning(f"{rel_tag} is ignored.")

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
            return self.sentence.base_phrases[self.index - 1].global_index + 1
        if self.sentence.index == 0:
            return self.index
        return self.document.sentences[self.sentence.index - 1].base_phrases[-1].global_index + 1

    @property
    def parent_unit(self) -> Optional["Phrase"]:
        """上位の言語単位（文節）．未登録なら None．"""
        return self._phrase

    @property
    def child_units(self) -> Optional[List[Morpheme]]:
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
        """文．"""
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
        """文節．"""
        assert self._phrase is not None
        return self._phrase

    @phrase.setter
    def phrase(self, phrase: "Phrase") -> None:
        """文節．

        Args:
            phrase: 文節．
        """
        self._phrase = phrase

    @property
    def morphemes(self) -> List[Morpheme]:
        """形態素のリスト．"""
        assert self._morphemes is not None
        return self._morphemes

    @morphemes.setter
    def morphemes(self, morphemes: List[Morpheme]) -> None:
        """形態素のリスト．

        Args:
            morphemes: 形態素のリスト．
        """
        for morpheme in morphemes:
            morpheme.base_phrase = self
        self._morphemes = morphemes

    @property
    def head(self) -> Morpheme:
        """主辞の形態素．"""
        feature_to_priority = {"内容語": 0, "準内容語": 1, "基本句-主辞": 2}
        head = self.morphemes[0]
        current_priority = -1
        for morpheme in self.morphemes:
            if not morpheme.features:
                continue
            for feature, priority in feature_to_priority.items():
                if feature in morpheme.features and priority > current_priority:
                    head = morpheme
                    current_priority = priority
        return head

    @property
    def parent(self) -> Optional["BasePhrase"]:
        """係り先の基本句．ないなら None．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        if self.parent_index is None:
            raise AttributeError("parent_index has not been set")
        if self.parent_index == -1:
            return None
        return self.sentence.base_phrases[self.parent_index]

    @cached_property
    def children(self) -> List["BasePhrase"]:
        """この基本句に係っている基本句のリスト．

        Raises:
            AttributeError: 解析結果にアクセスできない場合．
        """
        return [base_phrase for base_phrase in self.sentence.base_phrases if base_phrase.parent == self]

    @property
    def entities_all(self) -> Set[Entity]:
        """nonidentical も含めた参照している全エンティティの集合．"""
        return self.entities | self.entities_nonidentical

    @classmethod
    def from_knp(cls, knp_text: str) -> "BasePhrase":
        """基本句クラスのインスタンスを KNP の解析結果から初期化．

        Args:
            knp_text: KNP の解析結果．
        """
        first_line, *lines = knp_text.split("\n")
        match = cls.PAT.match(first_line)
        if match is None:
            raise ValueError(f"malformed base phrase line: {first_line}")
        parent_index = int(match["pid"]) if match["pid"] is not None else None
        dep_type = DepType(match["dtype"]) if match["dtype"] is not None else None
        features = FeatureDict.from_fstring(match["feats"] or "")
        rel_tags = RelTagList.from_fstring(match["feats"] or "")
        memo_tag = MemoTag.from_fstring(match["feats"] or "")
        base_phrase = cls(parent_index, dep_type, features, rel_tags, memo_tag)

        morphemes: List[Morpheme] = []
        for line in lines:
            if line.strip() == "":
                continue
            morphemes.append(Morpheme.from_jumanpp(line))
        base_phrase.morphemes = morphemes
        return base_phrase

    def to_knp(self) -> str:
        """KNP フォーマットに変換．"""
        ret = "+"
        if self.parent_index is not None:
            assert self.dep_type is not None
            ret += f" {self.parent_index}{self.dep_type.value}"
        if self.rel_tags or self.memo_tag or self.features:
            ret += " "
            ret += self.rel_tags.to_fstring()
            if self.memo_tag:
                ret += self.memo_tag.to_fstring()
            ret += self.features.to_fstring()
        ret += "\n"
        ret += "".join(morpheme.to_knp() for morpheme in self.morphemes)
        return ret

    def get_coreferents(self, include_nonidentical: bool = False, include_self: bool = False) -> Set["BasePhrase"]:
        """この基本句と共参照している基本句の集合を返却．

        Args:
            include_nonidentical: nonidentical なメンションを含めるなら True．
            include_self: 自身を含めるなら True．

        Returns:
            共参照している基本句の集合．
        """
        mentions: Set["BasePhrase"] = set()
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

        Args:
            entity: エンティティ．
        """
        if entity in self.entities:
            return False
        else:
            assert entity in self.entities_nonidentical, f"non-referring entity: {entity}"
            return True

    def add_entity(self, entity: Entity, nonidentical: bool = False) -> None:
        """エンティティを追加．

        Args:
            entity: 追加するエンティティ．
            nonidentical: nonidentical なメンションなら True．
        """
        if nonidentical:
            self.entities_nonidentical.add(entity)
        else:
            self.entities.add(entity)
        entity.add_mention(self, nonidentical=nonidentical)

    def _add_pas(self, rel_tag: RelTag) -> None:
        """述語項構造を追加．"""
        entity_manager = self.document.entity_manager
        assert self.pas is not None
        if rel_tag.sid is not None:
            if (arg_base_phrase := self._get_target_base_phrase(rel_tag)) is None:
                return
            if not arg_base_phrase.entities:
                arg_base_phrase.add_entity(entity_manager.get_or_create_entity())
            self.pas.add_argument(rel_tag.type, arg_base_phrase, mode=rel_tag.mode)
        else:
            if rel_tag.target == "なし":
                self.pas.set_arguments_optional(rel_tag.type)
                return
            # exophora
            entity = entity_manager.get_or_create_entity(ExophoraReferent(rel_tag.target))
            self.pas.add_special_argument(rel_tag.type, rel_tag.target, eid=entity.eid, mode=rel_tag.mode)

    def _add_coreference(self, rel_tag: RelTag) -> None:
        """共参照関係を追加．"""
        entity_manager = self.document.entity_manager
        # create source entity
        if not self.entities:
            self.add_entity(entity_manager.get_or_create_entity())

        nonidentical: bool = rel_tag.type.endswith("≒")
        if rel_tag.sid is not None:
            if (target_base_phrase := self._get_target_base_phrase(rel_tag)) is None:
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
                target_entity = entity_manager.get_or_create_entity(exophora_referent=ExophoraReferent(rel_tag.target))
                entity_manager.merge_entities(self, None, source_entity, target_entity, nonidentical)

    def _get_target_base_phrase(self, rel_tag: RelTag) -> Optional["BasePhrase"]:
        """rel が指す基本句を取得．"""
        sentences = [sent for sent in self.document.sentences if sent.sid == rel_tag.sid]
        if not sentences:
            logger.warning(f"{self.sentence.sid}: relation with unknown sid found: {rel_tag.sid}")
            return None
        sentence = sentences[0]
        assert rel_tag.base_phrase_index is not None
        if rel_tag.base_phrase_index >= len(sentence.base_phrases):
            logger.warning(f"{self.sentence.sid}: index out of range")
            return None
        target_base_phrase = sentence.base_phrases[rel_tag.base_phrase_index]
        if not (set(rel_tag.target) & set(target_base_phrase.text)):
            logger.warning(
                f"{self.sentence.sid}: rel target mismatch; '{rel_tag.target}' vs '{target_base_phrase.text}'"
            )
        return target_base_phrase

    def __hash__(self) -> int:
        return hash((self.global_index, self.sentence.sid))

    @staticmethod
    def is_base_phrase_line(line: str) -> bool:
        """基本句行なら True を返す．"""
        return BasePhrase.PAT.match(line) is not None
