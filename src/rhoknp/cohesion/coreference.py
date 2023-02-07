import logging
from typing import TYPE_CHECKING, Dict, Optional, Set

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

    def add_mention(self, mention: "BasePhrase", is_nonidentical: bool = False) -> None:
        """このエンティティを参照するメンションを追加．

        Args:
            mention: 追加対象のメンション．
            is_nonidentical: メンションが nonidentical（"≒" 付きでアノテーションされている）なら True．

        .. note::
            identical なメンションが追加されたとき，すでに nonidentical なメンションとして登録されていたら，
            identical なメンションとして上書きする．
        """
        if is_nonidentical:
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
            return str(list(self.mentions)[0])
        elif self.mentions_nonidentical:
            return str(list(self.mentions_nonidentical)[0])
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

    entities: Dict[int, Entity] = {}  #: ID をキーとするエンティティの辞書．

    @classmethod
    def get_or_create_entity(
        cls, exophora_referent: Optional[ExophoraReferent] = None, eid: Optional[int] = None
    ) -> Entity:
        """自身が参照するエンティティを作成．

        exophora_referent が singleton entity だった場合を除き，新しく Entity のインスタンスを作成して返す．
        singleton entity とは，「著者」や「不特定:人１」などの文書中に必ず一つしか存在しないような entity．
        一方で，「不特定:人」や「不特定:物」は複数存在しうるので singleton entity ではない．

        Args:
            exophora_referent: 外界照応における照応先．対応するものがなければ None．
            eid: エンティティ ID．None の場合自動で割り振る．

        Returns:
             Entity: 作成されたエンティティ．
        """
        if exophora_referent is not None and exophora_referent.is_singleton is True:
            entities = [e for e in cls.entities.values() if exophora_referent == e.exophora_referent]
            # If a singleton entity already exists, do not create a new entity, but return that entity.
            if entities:
                assert len(entities) == 1  # ensure that there is only one singleton entity
                return entities[0]
        if eid in cls.entities:
            return cls.entities[eid]
        elif eid is None:
            eid = max(cls.entities.keys()) + 1 if cls.entities else 0
        entity = Entity(eid, exophora_referent=exophora_referent)
        cls.entities[eid] = entity
        return entity

    @classmethod
    def merge_entities(
        cls,
        source_mention: "BasePhrase",
        target_mention: Optional["BasePhrase"],
        source_entity: Entity,
        target_entity: Entity,
        is_nonidentical: bool,
    ) -> None:
        """2つのエンティティをマージ．

        source_mention と source_entity, target_mention と target_entity の間には参照関係があるが，
        source と target 間には関係が作られていないので，add_mention する．
        source_entity と target_entity が同一のエンティティであり，exophor も同じか片方が None ならば target_entity の方を削除する．

        Args:
            source_mention: ソース側メンション．
            target_mention: ターゲット側メンション．メンションが存在しない場合は None．
            source_entity: ソース側エンティティ．
            target_entity: ターゲット側エンティティ．
            is_nonidentical: ソース側メンションとターゲット側メンションの関係が nonidentical なら True．
        """
        assert target_entity in target_mention.entities_all if target_mention else True
        assert source_entity in source_mention.entities_all
        is_tgt_nonidentical = target_mention is not None and target_entity in target_mention.entities_nonidentical
        is_src_nonidentical = source_entity in source_mention.entities_nonidentical
        if source_entity is target_entity:
            if is_nonidentical is False:
                # When two sides of a triangle formed by source_entity (=target_entity), source_mention, and
                # target_mention are identical, the other side is also identical.
                if is_src_nonidentical is False and is_tgt_nonidentical is True:
                    assert target_mention is not None
                    source_entity.add_mention(target_mention, is_nonidentical=False)
                if is_src_nonidentical is True and is_tgt_nonidentical is False:
                    source_entity.add_mention(source_mention, is_nonidentical=False)
            return
        if target_mention is not None:
            source_entity.add_mention(target_mention, is_nonidentical=(is_nonidentical or is_src_nonidentical))
        target_entity.add_mention(source_mention, is_nonidentical=(is_nonidentical or is_tgt_nonidentical))
        # When source_entity and target_entity may not be identical, do not delete target_entity.
        if is_nonidentical or is_tgt_nonidentical or is_src_nonidentical:
            return
        # When exophora_referent of source_entity and target_entity is different, target_entity is not deleted.
        if (
            source_entity.exophora_referent is not None
            and target_entity.exophora_referent is not None
            and source_entity.exophora_referent != target_entity.exophora_referent
        ):
            return
        # prepare to delete target_entity as follows
        if source_entity.exophora_referent is None:
            source_entity.exophora_referent = target_entity.exophora_referent
        for tm in target_entity.mentions_all:
            source_entity.add_mention(tm, is_nonidentical=target_entity in tm.entities_nonidentical)
        # Arguments also have entity ids and will be updated.
        source_sentence = source_mention.sentence
        pas_list = source_mention.document.pas_list if source_sentence.has_document else source_sentence.pas_list
        for arg in [arg for pas in pas_list for args in pas.get_all_arguments(relax=False).values() for arg in args]:
            if isinstance(arg, ExophoraArgument) and arg.eid == target_entity.eid:
                arg.eid = source_entity.eid
        cls.delete_entity(target_entity)

    @classmethod
    def delete_entity(cls, entity: Entity) -> None:
        """エンティティを削除．

        対象エンティティを `EntityManager` およびそのエンティティを参照するすべてのメンションから削除する．
        エンティティIDには欠番が生まれる可能性がある．

        Args:
            entity: 削除対象のエンティティ．
        """
        for mention in entity.mentions_all:
            entity.remove_mention(mention)
        cls.entities.pop(entity.eid)

    @classmethod
    def reset(cls) -> None:
        """管理しているエンティティを全て削除．"""
        cls.entities.clear()
