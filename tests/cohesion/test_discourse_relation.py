import textwrap

import pytest

from rhoknp import Document, Sentence
from rhoknp.cohesion import DiscourseRelationLabel, DiscourseRelationTag


@pytest.mark.parametrize(
    "tag, label",
    [
        (DiscourseRelationTag.NO_RELATION, DiscourseRelationLabel.NO_RELATION),
        (DiscourseRelationTag.CAUSE_REASON, DiscourseRelationLabel.CAUSE_REASON),
        (DiscourseRelationTag.CAUSE_REASON_FORWARD, DiscourseRelationLabel.CAUSE_REASON),
        (DiscourseRelationTag.CAUSE_REASON_BACKWARD, DiscourseRelationLabel.CAUSE_REASON),
        (DiscourseRelationTag.CAUSE_REASON_BACKWARD2, DiscourseRelationLabel.CAUSE_REASON),
        (DiscourseRelationTag.PURPOSE, DiscourseRelationLabel.PURPOSE),
        (DiscourseRelationTag.PURPOSE_FORWARD, DiscourseRelationLabel.PURPOSE),
        (DiscourseRelationTag.PURPOSE_BACKWARD, DiscourseRelationLabel.PURPOSE),
        (DiscourseRelationTag.CONDITION, DiscourseRelationLabel.CONDITION),
        (DiscourseRelationTag.CONDITION_FORWARD, DiscourseRelationLabel.CONDITION),
        (DiscourseRelationTag.CONDITION_BACKWARD, DiscourseRelationLabel.CONDITION),
        (DiscourseRelationTag.NEGATIVE_CONDITION, DiscourseRelationLabel.CONDITION),
        (DiscourseRelationTag.CONTRAST, DiscourseRelationLabel.CONTRAST),
        (DiscourseRelationTag.CONTRAST_NO_DIRECTION, DiscourseRelationLabel.CONTRAST),
        (DiscourseRelationTag.CONCESSION, DiscourseRelationLabel.CONCESSION),
        (DiscourseRelationTag.CONCESSION_FORWARD, DiscourseRelationLabel.CONCESSION),
        (DiscourseRelationTag.CONCESSION_BACKWARD, DiscourseRelationLabel.CONCESSION),
        (DiscourseRelationTag.CONCESSIVE_CONDITION, DiscourseRelationLabel.CONCESSION),
        (DiscourseRelationTag.EVIDENCE, DiscourseRelationLabel.EVIDENCE),
        (DiscourseRelationTag.EVIDENCE_FORWARD, DiscourseRelationLabel.EVIDENCE),
        (DiscourseRelationTag.EVIDENCE_BACKWARD, DiscourseRelationLabel.EVIDENCE),
    ],
)
def test_discourse_relation_tag_label(tag: DiscourseRelationTag, label: DiscourseRelationLabel):
    assert tag.label == label


def test_document():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        # S-ID:2
        * 1D
        + 1D
        服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipediaページ内一覧:ドラゴンボールの登場人物 読み不明 疑似代表表記 代表表記:服屋/服屋"
        も も も 助詞 9 副助詞 2 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 2
    discourse_relation_0 = document.clauses[0].discourse_relations[0]
    assert discourse_relation_0.sid == "1"
    assert discourse_relation_0.base_phrase_index == 4
    assert discourse_relation_0.label == DiscourseRelationLabel.CONDITION
    assert discourse_relation_0.modifier == document.clauses[0]
    assert discourse_relation_0.head == document.clauses[1]
    discourse_relation_1 = document.clauses[0].discourse_relations[1]
    assert discourse_relation_1.sid == "2"
    assert discourse_relation_1.base_phrase_index == 1
    assert discourse_relation_1.label == DiscourseRelationLabel.CONDITION
    assert discourse_relation_1.modifier == document.clauses[0]
    assert discourse_relation_1.head == document.clauses[2]


def test_sentence():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.clauses[0].discourse_relations) == 1


def test_to_fstring():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    sentence = Sentence.from_knp(knp_text)
    assert sentence.clauses[0].discourse_relations[0].to_fstring() == "<談話関係:1/4/条件>"


def test_invalid_discourse_relation():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/3/条件;1/5/条件;2/1/条件;2/1/条;4>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 0


def test_clause_function():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><節-機能-条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 1


def test_invalid_clause_function():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><節-主辞><節-機能-条><節-機能->
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞><節-主辞><節-機能-条件>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 0
    assert len(document.clauses[1].discourse_relations) == 0
