import logging
from typing import TYPE_CHECKING, Optional

from rhoknp.rel.argument import SpecialArgument
from rhoknp.rel.exophora import ExophoraReferent

if TYPE_CHECKING:
    from rhoknp.units.base_phrase import BasePhrase

logger = logging.getLogger(__name__)


class Entity:
    """共参照におけるエンティティ．

    Args:
        eid: エンティティ ID．
        exophora_referent: 自身が外界照応の照応先に対応するなら照応先の種類. 対応しないなら None.

    Attributes:
        eid: エンティティ ID
        exophora_referent: 外界照応の照応先．対応するものがなければ None.
        mentions: このエンティティを参照するメンションの集合．
        mentions_nonidentical: このエンティティを≒関係で参照するメンションの集合．
    """

    def __init__(self, eid: int, exophora_referent: Optional[ExophoraReferent] = None) -> None:
        self.eid: int = eid
        self.exophora_referent: Optional[ExophoraReferent] = exophora_referent
        self.mentions: set["BasePhrase"] = set()
        self.mentions_nonidentical: set["BasePhrase"] = set()

    @property
    def mentions_all(self) -> set["BasePhrase"]:
        """nonidentical を含めたこのエンティティを参照する全てのメンションの集合．"""
        return self.mentions | self.mentions_nonidentical

    def add_mention(self, mention: "BasePhrase", nonidentical: bool = False) -> None:
        """このエンティティを参照するメンションを追加．

        When an identical mention is added and the mention has already been registered as a nonidentical
        mention, it will be overwritten as identical.

        Args:
            mention: 追加対象のメンション．
            nonidentical: メンションが nonidentical ("≒" 付きでアノテーションされている) なら True．
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
        """このエンティティを参照するメンションを削除．"""
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
            return str(None)

    def __repr__(self) -> str:
        ret = f"{self.__class__.__name__}(eid={repr(self.eid)}"
        if self.mentions:
            ret += f", mentions={repr(self.mentions)}"
        if self.mentions_nonidentical:
            ret += f", mentions_nonidentical={repr(self.mentions_nonidentical)}"
        if self.exophora_referent:
            ret += f", exophora_referent={repr(self.exophora_referent)}"
        ret += ")"
        return ret

    def __hash__(self):
        return hash(self.eid)


class EntityManager:
    """文書全体のエンティティを管理．

    Attributes:
        entities: エンティティのリスト．
    """

    def __init__(self):
        self.entities: list[Entity] = []

    def get_or_create_entity(
        self, exophora_referent: Optional[ExophoraReferent] = None, eid: Optional[int] = None
    ) -> Entity:
        """自身が参照するエンティティを作成．

        exophora_referent が singleton entity だった場合を除き、新しく Entity のインスタンスを作成して返す．
        singleton entity とは、「著者」や「不特定:人１」などの文書中に必ず一つしか存在しないような entity．
        一方で、「不特定:人」や「不特定:物」は複数存在しうるので singleton entity ではない．
        eid を指定しない場合、最後に作成した entity の次の eid を選択．

        Args:
            exophora_referent: 外界照応における照応先．対応するものがなければ None．
            eid: エンティティ ID．None の場合自動で割り振る．

        Returns:
             Entity: 作成されたエンティティ．
        """
        if exophora_referent is not None and exophora_referent.is_singleton is True:
            entities = [e for e in self.entities if exophora_referent == e.exophora_referent]
            # すでに singleton entity が存在した場合、新しい entity は作らずにその entity を返す
            if entities:
                assert len(entities) == 1  # singleton entity が1つしかないことを保証
                return entities[0]
        eids: list[int] = [e.eid for e in self.entities]
        if eid in eids:
            _eid = eid
            eid = max(eids) + 1
            logger.warning(f"{_eid} is already used. use eid: {eid} instead.")
        elif eid is None or eid < 0:
            eid = max(eids) + 1 if eids else 0
        entity = Entity(eid, exophora_referent=exophora_referent)
        self.entities.append(entity)
        return entity

    def merge_entities(
        self,
        source_mention: "BasePhrase",
        target_mention: Optional["BasePhrase"],
        se: Entity,
        te: Entity,
        nonidentical: bool,
    ) -> None:
        """2つのエンティティをマージ．

        source_mention と se, target_mention と te の間には mention が張られているが、
        source と target 間には張られていないので、add_mention する．
        se と te が同一のエンティティであり、exophor も同じか片方が None ならば te の方を削除する．

        Args:
            source_mention: ソース側メンション．
            target_mention: ターゲット側メンション．メンションが存在しない場合は None．
            se: ソース側エンティティ．
            te: ターゲット側エンティティ．
            nonidentical: ソース側メンションとターゲット側メンションの関係が nonidentical なら True．
        """
        nonidentical_tgt = (target_mention is not None) and target_mention.is_nonidentical_to(te)
        if se not in source_mention.entities_all:
            return
        nonidentical_src = source_mention.is_nonidentical_to(se)
        if se is te:
            if not nonidentical:
                # se (te), source_mention, target_mention の三角形のうち2辺が identical ならもう1辺も identical
                if (not nonidentical_src) and nonidentical_tgt:
                    assert target_mention is not None
                    se.add_mention(target_mention, nonidentical=False)
                if nonidentical_src and (not nonidentical_tgt):
                    se.add_mention(source_mention, nonidentical=False)
            return
        if target_mention is not None:
            se.add_mention(target_mention, nonidentical=(nonidentical or nonidentical_src))
        te.add_mention(source_mention, nonidentical=(nonidentical or nonidentical_tgt))
        # se と te が同一でない可能性が捨てきれない場合、te は削除しない
        if nonidentical_src or nonidentical or nonidentical_tgt:
            return
        # se と te が同一でも exophor が異なれば te は削除しない
        if (
            se.exophora_referent is not None
            and te.exophora_referent is not None
            and se.exophora_referent != te.exophora_referent
        ):
            return
        # 以下 te を削除する準備
        if se.exophora_referent is None:
            se.exophora_referent = te.exophora_referent
        for tm in te.mentions_all:
            se.add_mention(tm, nonidentical=tm.is_nonidentical_to(te))
        # argument も eid を持っているので eid が変わった場合はこちらも更新
        pas_list = source_mention.document.pas_list()
        for arg in [arg for pas in pas_list for args in pas.get_all_arguments(relax=False).values() for arg in args]:
            if isinstance(arg, SpecialArgument) and arg.eid == te.eid:
                arg.eid = se.eid
        self.delete_entity(te)  # delete target entity

    def delete_entity(self, entity: Entity) -> None:
        """エンティティを削除．

        Remove the target entity from all the mentions of the entity as well as from self.entities.
        Note that entity IDs can have a missing number.

        Args:
            entity: 削除対象のエンティティ．
        """
        if entity not in self.entities:
            return
        for mention in entity.mentions_all:
            entity.remove_mention(mention)
        self.entities.remove(entity)

    def reset(self) -> None:
        """管理する全てのエンティティを削除．"""
        max_iteration = 100
        cnt = 0
        while self.entities:
            for entity in self.entities:
                self.delete_entity(entity)
            cnt += 1
            if cnt > max_iteration:
                raise RuntimeError("MAX_ITERATION exceeded")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(entities={repr(self.entities)})"

    def __getitem__(self, eid: int) -> Entity:
        es = [e for e in self.entities if e.eid == eid]
        if len(es) == 0:
            raise KeyError(f"entity ID: {eid} not found.")
        return es[0]
