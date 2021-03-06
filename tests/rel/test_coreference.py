from pathlib import Path

import pytest

from rhoknp.rel import Entity, ExophoraReferent
from rhoknp.units import BasePhrase, Document


def test_coref1() -> None:
    doc_id = "w201106-0000060050"
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())

    entities: list[Entity] = sorted(document.entity_manager.entities, key=lambda e: e.eid)
    assert len(entities) == 19

    entity = entities[0]
    assert entity.exophora_referent == ExophoraReferent("不特定:人")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 0

    entity = entities[1]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("コイン", 0)
    assert len(mentions[0].entities) == 1

    entity = entities[2]
    assert entity.exophora_referent == ExophoraReferent("不特定:人")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 0

    entity = entities[3]
    assert entity.exophora_referent == ExophoraReferent("読者")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("自分", 15)
    assert len(mentions[0].entities) == 1
    assert len(mentions[0].entities_nonidentical) == 3

    entity = entities[4]
    assert entity.exophora_referent == ExophoraReferent("著者")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("自分", 15)
    assert len(mentions[0].entities) == 1
    assert len(mentions[0].entities_nonidentical) == 3

    entity = entities[5]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("トス", 1)
    assert len(mentions[0].entities) == 1

    entity = entities[6]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("表", 4)
    assert len(mentions[0].entities) == 1

    entity = entities[7]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("数", 6)
    assert len(mentions[0].entities) == 1

    entity = entities[8]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("出た", 5)
    assert len(mentions[0].entities) == 1

    entity = entities[9]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("フィールド", 7)
    assert len(mentions[0].entities) == 1

    entity = entities[10]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("モンスター", 8)
    assert len(mentions[0].entities) == 1

    entity = entities[11]
    assert entity.exophora_referent == ExophoraReferent("不特定:状況")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 0

    entity = entities[12]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("破壊", 9)
    assert len(mentions[0].entities) == 1

    entity = entities[13]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("ターン", 13)
    assert len(mentions[0].entities) == 1

    entity = entities[14]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("自分", 15)
    assert len(mentions[0].entities) == 1

    entity = entities[15]
    assert entity.exophora_referent == ExophoraReferent("不特定:人")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("自分", 15)
    assert len(mentions[0].entities) == 1

    entity = entities[16]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("フェイズ", 17)
    assert len(mentions[0].entities) == 1

    entity = entities[17]
    assert entity.exophora_referent == ExophoraReferent("不特定:人")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 0

    entity = entities[18]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("効果", 11)
    assert len(mentions[0].entities) == 1


def test_coref2() -> None:
    doc_id = "w201106-0000060560"
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    entities: list[Entity] = sorted(document.entity_manager.entities, key=lambda e: e.eid)
    assert len(entities) == 15

    entity: Entity = entities[12]
    assert entity.exophora_referent is None
    mentions: list[BasePhrase] = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 4
    assert (mentions[0].text, mentions[0].global_index, {e.eid for e in mentions[0].entities}) == ("ドクターを", 7, {4})
    assert (mentions[1].text, mentions[1].global_index, {e.eid for e in mentions[1].entities}) == ("ドクターを", 11, {14})
    assert (mentions[2].text, mentions[2].global_index, {e.eid for e in mentions[2].entities}) == ("ドクターの", 16, {14})
    assert (mentions[3].text, mentions[3].global_index, {e.eid for e in mentions[3].entities}) == ("皆様", 17, {14})


@pytest.mark.parametrize("doc_id", ["w201106-0000060560", "w201106-0000060560", "w201106-0000060877"])
def test_coref_link(doc_id: str) -> None:
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    entities: list[Entity] = sorted(document.entity_manager.entities, key=lambda e: e.eid)

    for entity in entities:
        for mention in entity.mentions:
            assert entity in mention.entities
        for mention in entity.mentions_nonidentical:
            assert entity in mention.entities_nonidentical
    for mention in document.base_phrases:
        for entity in mention.entities:
            assert mention in entity.mentions
        for entity in mention.entities_nonidentical:
            assert mention in entity.mentions_nonidentical


def test_coreferents() -> None:
    doc_id = "w201106-0000060560"
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    mention = document.base_phrases[11]  # ドクター
    coreferents = sorted(mention.get_coreferents(include_nonidentical=False), key=lambda m: m.global_index)
    assert len(coreferents) == 2
    assert (coreferents[0].text, coreferents[0].global_index) == ("ドクターの", 16)
    assert (coreferents[1].text, coreferents[1].global_index) == ("皆様", 17)


def test_coreferents_nonidentical() -> None:
    doc_id = "w201106-0000060560"
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    mention = document.base_phrases[11]  # ドクター
    coreferents = sorted(mention.get_coreferents(include_nonidentical=True), key=lambda m: m.global_index)
    assert len(coreferents) == 3
    assert (coreferents[0].text, coreferents[0].global_index) == ("ドクターを", 7)
    assert (coreferents[1].text, coreferents[1].global_index) == ("ドクターの", 16)
    assert (coreferents[2].text, coreferents[2].global_index) == ("皆様", 17)


@pytest.mark.parametrize("doc_id", ["w201106-0000060560", "w201106-0000060560", "w201106-0000060877"])
def test_reset_entities(doc_id: str) -> None:
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    document.entity_manager.reset()
    assert len(document.entity_manager.entities) == 0
