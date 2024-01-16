import textwrap
from pathlib import Path
from typing import List

import pytest

from rhoknp import Sentence
from rhoknp.cohesion import Entity, EntityManager, ExophoraArgument, ExophoraReferent
from rhoknp.units import BasePhrase, Document


def test_entity() -> None:
    document = Document.from_knp(
        textwrap.dedent(
            """\
            # S-ID:1
            * 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
            + 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><正規化代表表記:良い/よい><主辞代表表記:良い/よい>
            + 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            * -1D <BGH:散歩/さんぽ+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ>
            + -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            """
        )
    )
    eid = 0
    entity = Entity(eid, exophora_referent=None)
    assert str(entity) == ""
    base_phrase_0 = document.base_phrases[0]
    entity.add_mention(base_phrase_0)
    assert entity.eid == eid
    assert entity.exophora_referent is None
    assert entity.mentions_all == [base_phrase_0]
    assert str(entity) == "天気が"
    assert repr(entity) == "<rhoknp.cohesion.coreference.Entity: 0, '天気が'>"

    entity.add_mention(base_phrase_0, is_nonidentical=True)
    assert entity.mentions_all == [base_phrase_0]
    assert str(entity) == "天気が"
    assert repr(entity) == "<rhoknp.cohesion.coreference.Entity: 0, '天気が'>"

    base_phrase_1 = document.base_phrases[1]
    entity.add_mention(base_phrase_1, is_nonidentical=True)
    assert entity.mentions_all == [base_phrase_0, base_phrase_1]
    assert str(entity) == "天気が"
    assert repr(entity) == "<rhoknp.cohesion.coreference.Entity: 0, '天気が', 'いいので'>"

    entity.remove_mention(base_phrase_0)
    assert entity.mentions_all == [base_phrase_1]
    assert str(entity) == "いいので"
    assert repr(entity) == "<rhoknp.cohesion.coreference.Entity: 0, 'いいので'>"


def test_exophora_entity() -> None:
    exophora_referent = ExophoraReferent(text="不特定:物１")
    eid = 3
    entity = Entity(eid, exophora_referent=exophora_referent)
    assert entity.eid == eid
    assert entity.exophora_referent == exophora_referent
    assert entity.mentions_all == []
    assert str(entity) == "不特定:物1"


def test_coref_sentence() -> None:
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 2D
            + 2D <用言:判><体言><時制:非過去><状態述語>
            あれ あれ あれ 指示詞 7 名詞形態指示詞 1 * 0 * 0 "代表表記:あれ/あれ" <基本句-主辞><用言表記先頭><用言表記末尾>
            だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 "代表表記:だ/だ"
            よ よ よ 助詞 9 終助詞 4 * 0 * 0 "代表表記:よ/よ"
            * 2P
            + 2P <rel type="=" target="あれ" sid="000-0-0" id="0"/><修飾>
            あれ あれ あれ 指示詞 7 名詞形態指示詞 1 * 0 * 0 "代表表記:あれ/あれ" <基本句-主辞>
            、 、 、 特殊 1 読点 2 * 0 * 0 "代表表記:、/、"
            * -1D
            + -1D <rel type="=" target="不特定:物１"/><用言:判><体言><時制:非過去><否定表現><レベル:C><状態述語><節-区切><節-主辞>
            それ それ それ 指示詞 7 名詞形態指示詞 1 * 0 * 0 "代表表記:それ/それ" <基本句-主辞><用言表記先頭><用言表記末尾>
            じゃ じゃ じゃ 判定詞 4 * 0 判定詞 25 ダ列タ系連用テ形 12 "代表表記:だ/だ"
            なくて なくて ない 接尾辞 14 形容詞性述語接尾辞 5 イ形容詞アウオ段 18 タ系連用テ形 12 "代表表記:ない/ない"
            EOS
            """
        )
    )

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 2

    entity = entities[0]
    assert entity.exophora_referent is None
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 2
    assert (mentions[0].head.surf, mentions[0].global_index) == ("あれ", 0)
    assert len(mentions[0].entities) == 1
    assert (mentions[1].head.surf, mentions[1].global_index) == ("あれ", 1)
    assert len(mentions[1].entities) == 1

    entity = entities[1]
    assert entity.exophora_referent == ExophoraReferent("不特定:物１")
    mentions = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 1
    assert (mentions[0].head.surf, mentions[0].global_index) == ("それ", 2)
    assert len(mentions[0].entities) == 1


def test_coref1() -> None:
    doc_id = "w201106-0000060050"
    _ = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
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
    _ = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 15

    entity: Entity = entities[12]
    assert entity.exophora_referent is None
    mentions: List[BasePhrase] = sorted(entity.mentions_all, key=lambda x: x.global_index)
    assert len(mentions) == 4
    assert (mentions[0].text, mentions[0].global_index, {e.eid for e in mentions[0].entities}) == ("ドクターを", 7, {4})
    assert (mentions[1].text, mentions[1].global_index, {e.eid for e in mentions[1].entities}) == (
        "ドクターを",
        11,
        {14},
    )
    assert (mentions[2].text, mentions[2].global_index, {e.eid for e in mentions[2].entities}) == (
        "ドクターの",
        16,
        {14},
    )
    assert (mentions[3].text, mentions[3].global_index, {e.eid for e in mentions[3].entities}) == ("皆様", 17, {14})


@pytest.mark.parametrize("doc_id", ["w201106-0000060050", "w201106-0000060560", "w201106-0000060877"])
def test_coref_link(doc_id: str) -> None:
    document = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)

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


def test_coref_with_self() -> None:
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * -1D
            + -1D <rel type="=" target="わたし" sid="000-0-0" id="0"/>
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 1
    entity = entities[0]
    assert entity.exophora_referent is None
    assert len(entity.mentions) == 1
    mention = next(iter(entity.mentions))
    assert (mention.text, mention.global_index, {e.eid for e in mention.entities}) == ("わたし", 0, {0})
    assert len(entities[0].mentions_all) == 1


def test_coref_include_self() -> None:
    sentence = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * -1D
            + -1D
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )

    mention = sentence.base_phrases[0]
    coreferents = mention.get_coreferents(include_self=True)
    assert len(coreferents) == 1
    assert (coreferents[0].text, coreferents[0].global_index) == ("わたし", 0)


def test_merge_entity_0() -> None:
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D <rel type="=" target="著者"/>
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            * 2D
            + 2D <rel type="=" target="著者"/><rel type="=≒" target="わたし" sid="000-0-0" id="0"/>
            私 わたし 私 名詞 6 普通名詞 1 * 0 * 0
            * -1D
            + -1D <rel type="=≒" target="わたし" sid="000-0-0" id="0"/>
            自分 じぶん 自分 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 2

    entity = entities[0]
    assert entity.exophora_referent == ExophoraReferent("著者")
    assert len(entity.mentions_all) == 3
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 2
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("わたし", 0)
    assert len(mentions_identical[0].entities) == 1
    assert (mentions_identical[1].head.surf, mentions_identical[1].global_index) == ("私", 1)
    assert len(mentions_identical[1].entities) == 1
    mentions_nonidentical = sorted(entity.mentions_nonidentical, key=lambda x: x.global_index)
    assert len(mentions_nonidentical) == 1
    assert (mentions_nonidentical[0].head.surf, mentions_nonidentical[0].global_index) == ("自分", 2)
    assert len(mentions_nonidentical[0].entities) == 1

    entity = entities[1]
    assert entity.exophora_referent is None
    assert len(entity.mentions_all) == 2
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 1
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("自分", 2)
    assert len(mentions_identical[0].entities) == 1
    mentions_nonidentical = sorted(entity.mentions_nonidentical, key=lambda x: x.global_index)
    assert len(mentions_nonidentical) == 1
    assert (mentions_nonidentical[0].head.surf, mentions_nonidentical[0].global_index) == ("わたし", 0)
    assert len(mentions_nonidentical[0].entities) == 1


def test_merge_entity_1() -> None:
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D <rel type="=" target="著者"/>
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            * -1D
            + -1D <rel type="=≒" target="著者"/><rel type="=" target="わたし" sid="000-0-0" id="0"/>
            私 わたし 私 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 1

    entity = entities[0]
    assert entity.exophora_referent == ExophoraReferent("著者")
    assert len(entity.mentions_all) == 2
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 2
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("わたし", 0)
    assert len(mentions_identical[0].entities) == 1
    assert (mentions_identical[1].head.surf, mentions_identical[1].global_index) == ("私", 1)
    assert len(mentions_identical[1].entities) == 1
    assert len(entity.mentions_nonidentical) == 0


def test_merge_entity_2() -> None:
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D <rel type="=≒" target="著者"/>
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            * -1D
            + -1D <rel type="=" target="著者"/><rel type="=" target="わたし" sid="000-0-0" id="0"/>
            私 わたし 私 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 1

    entity = entities[0]
    assert entity.exophora_referent == ExophoraReferent("著者")
    assert len(entity.mentions_all) == 2
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 2
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("わたし", 0)
    assert len(mentions_identical[0].entities) == 1
    assert (mentions_identical[1].head.surf, mentions_identical[1].global_index) == ("私", 1)
    assert len(mentions_identical[1].entities) == 1
    assert len(entity.mentions_nonidentical) == 0


def test_merge_entity_3() -> None:
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D <rel type="=" target="著者"/>
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            * -1D
            + -1D <rel type="=" target="読者"/><rel type="=" target="わたし" sid="000-0-0" id="0"/>
            自分 じぶん 自分 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )

    entities: List[Entity] = sorted(EntityManager.entities.values(), key=lambda e: e.eid)
    assert len(entities) == 2

    entity = entities[0]
    assert entity.exophora_referent == ExophoraReferent("著者")
    assert len(entity.mentions_all) == 2
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 2
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("わたし", 0)
    assert len(mentions_identical[0].entities) == 2
    assert (mentions_identical[1].head.surf, mentions_identical[1].global_index) == ("自分", 1)
    assert len(mentions_identical[1].entities) == 2
    assert len(entity.mentions_nonidentical) == 0

    entity = entities[1]
    assert entity.exophora_referent == ExophoraReferent("読者")
    assert len(entity.mentions_all) == 2
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 2
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("わたし", 0)
    assert len(mentions_identical[0].entities) == 2
    assert (mentions_identical[1].head.surf, mentions_identical[1].global_index) == ("自分", 1)
    assert len(mentions_identical[1].entities) == 2
    assert len(entity.mentions_nonidentical) == 0


def test_merge_entity_4() -> None:
    sentence = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D
            わたし わたし わたし 名詞 6 普通名詞 1 * 0 * 0
            * -1D
            + -1D
            わたくし わたくし わたくし 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )
    EntityManager.reset()
    target_mention = sentence.base_phrases[0]
    entity = EntityManager.get_or_create_entity()
    entity.add_mention(target_mention, is_nonidentical=True)
    source_mention = sentence.base_phrases[1]
    entity.add_mention(source_mention, is_nonidentical=False)
    EntityManager.merge_entities(source_mention, target_mention, entity, entity, is_nonidentical=False)

    assert len(EntityManager.entities) == 1
    assert entity.exophora_referent is None
    assert len(entity.mentions_all) == 2
    mentions_identical = sorted(entity.mentions, key=lambda x: x.global_index)
    assert len(mentions_identical) == 2
    assert (mentions_identical[0].head.surf, mentions_identical[0].global_index) == ("わたし", 0)
    assert len(mentions_identical[0].entities) == 1
    assert (mentions_identical[1].head.surf, mentions_identical[1].global_index) == ("わたくし", 1)
    assert len(mentions_identical[1].entities) == 1
    assert len(entity.mentions_nonidentical) == 0


def test_update_argument_eid() -> None:
    doc = Document.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D <rel type="=" target="著者"/>
            私 わたし 私 名詞 6 普通名詞 1 * 0 * 0
            は は は 助詞 9 副助詞 2 * 0 * 0
            * -1D
            + -1D <rel type="ガ" target="私" sid="000-0-0" id="0"/><rel type="ヲ" target="不特定:人１"/>
            見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10
            。 。 。 特殊 1 句点 1 * 0 * 0
            EOS
            # S-ID:000-0-1
            * -1D
            + -1D <rel type="=" target="不特定:人１"/>
            彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0
            を を を 助詞 9 格助詞 1 * 0 * 0
            EOS
            """
        )
    )
    pas = doc.base_phrases[1].pas
    exophora_arguments = [arg for arg in pas.get_arguments("ヲ") if isinstance(arg, ExophoraArgument)]
    assert len(exophora_arguments) == 1
    assert exophora_arguments[0].eid == 2
    assert len(EntityManager.entities) == 2
