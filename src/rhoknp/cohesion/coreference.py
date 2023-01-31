import logging
from typing import TYPE_CHECKING, List, Optional, Set

from rhoknp.cohesion.argument import ExophoraArgument
from rhoknp.cohesion.exophora import ExophoraReferent

if TYPE_CHECKING:
    from rhoknp.units.base_phrase import BasePhrase

logger = logging.getLogger(__name__)


class Entity:
    """共参照におけるエンティティ．

    Args:
        eid: エンティティ ID．
        exophora_referent: 自身が外界照応の照応先に対応するなら照応先の種類. 対応しないなら None.
    """

    def __init__(self, eid: int, exophora_referent: Optional[ExophoraReferent] = None) -> None:
        self.eid = eid  #: エンティティ ID．
        self.exophora_referent = exophora_referent  #: 外界照応の照応先．対応するものがなければ None．
        self.mentions: Set["BasePhrase"] = set()  #: このエンティティを参照するメンションの集合．
        self.mentions_nonidentical: Set["BasePhrase"] = set()  #: このエンティティを≒関係で参照するメンションの集合．

    @property
    def mentions_all(self) -> Set["BasePhrase"]:
        """nonidentical を含めたこのエンティティを参照する全てのメンションの集合．"""
        return self.mentions | self.mentions_nonidentical

    def add_mention(self, mention: "BasePhrase", nonidentical: bool = False) -> None:
        """このエンティティを参照するメンションを追加．

        Args:
            mention: 追加対象のメンション．
            nonidentical: メンションが nonidentical（"≒" 付きでアノテーションされている）なら True．

        .. note::
            identical なメンションが追加されたとき，すでに nonidentical なメンションとして登録されていたら，
            identical なメンションとして上書きする．
        """
        if nonidentical:
            if mention in self.mentions_all:
                return
            mention.entities_nonidentical.add(self)
            self.mentions_nonidentical.add(mention)
        else:
            if mention in self.mentions_nonidentical:
                self.remove_mention(mention)
            mention.entities.add(self)
            self.mentions.add(mention)

    def remove_mention(self, mention: "BasePhrase") -> None:
        """このエンティティを参照するメンションを削除．

        Args:
            mention: 削除対象のメンション．
        """
        if mention in self.mentions:
            self.mentions.remove(mention)
            mention.entities.remove(self)
        if mention in self.mentions_nonidentical:
            self.mentions_nonidentical.remove(mention)
            mention.entities_nonidentical.remove(self)

    def __str__(self) -> str:
        if self.exophora_referent:
            return str(self.exophora_referent)
        if self.mentions:
            return list(self.mentions)[0].__str__()
        elif self.mentions_nonidentical:
            return list(self.mentions_nonidentical)[0].__str__()
        else:
            return ""

    def __repr__(self) -> str:
        items = [repr(self.eid)]
        items += [repr(m.text) for m in self.mentions]
        items += [repr(m.text) for m in self.mentions_nonidentical]
        if self.exophora_referent:
            items.append(repr(self.exophora_referent))
        return f"<{self.__module__}.{self.__class__.__name__}: {', '.join(items)}>"

    def __hash__(self) -> int:
        return hash(self.eid)


class EntityManager:
    """文書全体のエンティティを管理．"""

    entities: List[Entity] = []  #: エンティティのリスト．

    @classmethod
    def get_or_create_entity(
        cls, exophora_referent: Optional[ExophoraReferent] = None, eid: Optional[int] = None
    ) -> Entity:
        """自身が参照するエンティティを作成．

        exophora_referent が singleton entity だった場合を除き，新しく Entity のインスタンスを作成して返す．
        singleton entity とは，「著者」や「不特定:人１」などの文書中に必ず一つしか存在しないような entity．
        一方で，「不特定:人」や「不特定:物」は複数存在しうるので singleton entity ではない．
        eid を指定しない場合，最後に作成した entity の次の eid を選択．

        Args:
            exophora_referent: 外界照応における照応先．対応するものがなければ None．
            eid: エンティティ ID．None の場合自動で割り振る．

        Returns:
             Entity: 作成されたエンティティ．
        """
        if exophora_referent is not None and exophora_referent.is_singleton is True:
            entities = [e for e in cls.entities if exophora_referent == e.exophora_referent]
            # すでに singleton entity が存在した場合，新しい entity は作らずにその entity を返す
            if entities:
                assert len(entities) == 1  # singleton entity が1つしかないことを保証
                return entities[0]
        eids: List[int] = [e.eid for e in cls.entities]
        if eid in eids:
            _eid = eid
            eid = max(eids) + 1
            logger.warning(f"{_eid} is already used. use eid: {eid} instead.")
        elif eid is None or eid < 0:
            eid = max(eids) + 1 if eids else 0
        entity = Entity(eid, exophora_referent=exophora_referent)
        cls.entities.append(entity)
        return entity

    @classmethod
    def merge_entities(
        cls,
        source_mention: "BasePhrase",
        target_mention: Optional["BasePhrase"],
        source_entity: Entity,
        target_entity: Entity,
        nonidentical: bool,
    ) -> None:
        """2つのエンティティをマージ．

        source_mention と source_entity, target_mention と target_entity の間には mention が張られているが，
        source と target 間には張られていないので，add_mention する．
        source_entity と target_entity が同一のエンティティであり，exophor も同じか片方が None ならば target_entity の方を削除する．

        Args:
            source_mention: ソース側メンション．
            target_mention: ターゲット側メンション．メンションが存在しない場合は None．
            source_entity: ソース側エンティティ．
            target_entity: ターゲット側エンティティ．
            nonidentical: ソース側メンションとターゲット側メンションの関係が nonidentical なら True．
        """
        nonidentical_tgt = (target_mention is not None) and target_mention.is_nonidentical_to(target_entity)
        if source_entity not in source_mention.entities_all:
            return
        nonidentical_src = source_mention.is_nonidentical_to(source_entity)
        if source_entity is target_entity:
            if not nonidentical:
                # source_entity (target_entity), source_mention, target_mention の三角形のうち2辺が identical ならもう1辺も identical
                if (not nonidentical_src) and nonidentical_tgt:
                    assert target_mention is not None
                    source_entity.add_mention(target_mention, nonidentical=False)
                if nonidentical_src and (not nonidentical_tgt):
                    source_entity.add_mention(source_mention, nonidentical=False)
            return
        if target_mention is not None:
            source_entity.add_mention(target_mention, nonidentical=(nonidentical or nonidentical_src))
        target_entity.add_mention(source_mention, nonidentical=(nonidentical or nonidentical_tgt))
        # source_entity と target_entity が同一でない可能性が捨てきれない場合，target_entity は削除しない
        if nonidentical_src or nonidentical or nonidentical_tgt:
            return
        # source_entity と target_entity が同一でも exophor が異なれば target_entity は削除しない
        if (
            source_entity.exophora_referent is not None
            and target_entity.exophora_referent is not None
            and source_entity.exophora_referent != target_entity.exophora_referent
        ):
            return
        # 以下 target_entity を削除する準備
        if source_entity.exophora_referent is None:
            source_entity.exophora_referent = target_entity.exophora_referent
        for tm in target_entity.mentions_all:
            source_entity.add_mention(tm, nonidentical=tm.is_nonidentical_to(target_entity))
        # argument も eid を持っているので eid が変わった場合はこちらも更新
        source_sentence = source_mention.sentence
        pas_list = source_mention.document.pas_list if source_sentence.has_document else source_sentence.pas_list
        for arg in [arg for pas in pas_list for args in pas.get_all_arguments(relax=False).values() for arg in args]:
            if isinstance(arg, ExophoraArgument) and arg.eid == target_entity.eid:
                arg.eid = source_entity.eid
        cls.delete_entity(target_entity)  # delete target entity

    @classmethod
    def delete_entity(cls, entity: Entity) -> None:
        """エンティティを削除．

        対象エンティティを `EntityManager` およびそのエンティティを参照するすべてのメンションから削除する．
        エンティティIDには欠番が生まれる可能性がある．

        Args:
            entity: 削除対象のエンティティ．
        """
        if entity not in cls.entities:
            return
        for mention in entity.mentions_all:
            entity.remove_mention(mention)
        cls.entities.remove(entity)

    @classmethod
    def get_entity(cls, eid: int) -> Entity:
        """指定されたエンティティ ID に対応するエンティティを返却．

        Args:
            eid: エンティティ ID．

        Returns:
             Entity: 対応するエンティティ．
        """
        es = [e for e in cls.entities if e.eid == eid]
        if len(es) == 0:
            raise ValueError(f"entity ID: {eid} not found.")
        return es[0]

    @classmethod
    def reset(cls) -> None:
        """管理しているエンティティを全て削除．"""
        cls.entities.clear()
