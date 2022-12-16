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


def test_backward_clause_function_0():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * -1D
        + -1D <節-区切><節-主辞>
        辛い からい 辛い 形容詞 3 * 0 イ形容詞アウオ段 18 基本形 2 "代表表記:辛い/からい 反義:形容詞:甘い/あまい"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        # S-ID:2
        * 1D
        + 1D <節-前向き機能-逆接>
        しかし しかし しかし 接続詞 10 * 0 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        美味い 美味い 美味い 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 1
    assert len(document.clauses[1].discourse_relations) == 0
    assert document.clauses[0].discourse_relations[0].head == document.clauses[1]


def test_backward_clause_function_1():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * -1D
        + -1D <節-区切><節-主辞>
        耐えろ たえろ 耐える 動詞 2 * 0 母音動詞 1 命令形 6 "代表表記:耐える/たえる"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        # S-ID:2
        * 1D
        + 1D <節-主辞>
        幸せに しあわせに 幸せだ 形容詞 3 * 0 ナ形容詞 21 ダ列基本連用形 7 "代表表記:幸せだ/しあわせだ 反義:形容詞:不幸せだ/ふしあわせだ"
        なる なる なる 接尾辞 14 動詞性接尾辞 7 子音動詞ラ行 10 基本形 2 "代表表記:なる/なる"
        * -1D
        + -1D <節-前向き機能-目的><節-区切>
        ため ため ため 名詞 6 副詞的名詞 9 * 0 * 0 "代表表記:為/ため"
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 "代表表記:だ/だ"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 1
    assert len(document.clauses[1].discourse_relations) == 0
    assert document.clauses[0].discourse_relations[0].head == document.clauses[1]


def test_backward_clause_function_2():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * -1D
        + -1D <節-区切><節-主辞>
        厳しい きびしい 厳しい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:厳しい/きびしい"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        # S-ID:2
        * 5D
        + 5D <節-前向き機能-逆接>
        しかし しかし しかし 接続詞 10 * 0 * 0 * 0
        * 5D
        + 5D
        彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0 "代表表記:彼/かれ 漢字読み:訓 カテゴリ:人"
        は は は 助詞 9 副助詞 2 * 0 * 0 "代表表記:は/は"
        * 4D
        + 4D
        いつも いつも いつも 副詞 8 * 0 * 0 * 0
        * 4D
        + 4D
        苦難 くなん 苦難 名詞 6 普通名詞 1 * 0 * 0 "代表表記:苦難/くなん カテゴリ:抽象物"
        を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
        * 5D
        + 5D <節-機能-原因・理由><節-区切><節-主辞><談話関係:202212161839-0-1/5/原因・理由>
        乗り越えて のりこえて 乗り越える 動詞 2 * 0 母音動詞 1 タ系連用テ形 14 "代表表記:乗り越える/のりこえる"
        きた きた くる 接尾辞 14 動詞性接尾辞 7 カ変動詞 14 タ形 10 "代表表記:くる/くる"
        から から から 助詞 9 接続助詞 3 * 0 * 0 "代表表記:から/から"
        * -1D
        + -1D <節-区切><節-主辞>
        大丈夫だ だいじょうぶだ 大丈夫だ 形容詞 3 * 0 ナ形容詞 21 基本形 2 "代表表記:大丈夫だ/だいじょうぶだ"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 1
    assert len(document.clauses[1].discourse_relations) == 1
    assert len(document.clauses[2].discourse_relations) == 0
    assert document.clauses[0].discourse_relations[0].head == document.clauses[2]
    assert document.clauses[1].discourse_relations[0].head == document.clauses[2]


def test_backward_clause_function_3():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * -1D
        + -1D <節-区切><節-主辞>
        厳しい きびしい 厳しい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:厳しい/きびしい"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        # S-ID:2
        * 1D
        + 1D <節-前向き機能-原因・理由-逆>
        なぜなら なぜなら なぜなら 接続詞 10 * 0 * 0 * 0 "代表表記:なぜなら/なぜなら"
        * -1D
        + -1D <節-前向き機能-原因・理由-逆><節-区切><節-主辞>
        雨 あめ 雨 名詞 6 普通名詞 1 * 0 * 0 "代表表記:雨/あめ カテゴリ:抽象物 漢字読み:訓"
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 NIL
        から から から 助詞 9 接続助詞 3 * 0 * 0 NIL
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 NIL
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 0
    assert len(document.clauses[1].discourse_relations) == 1
    assert document.clauses[1].discourse_relations[0].head == document.clauses[0]


def test_both():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D
        + 4D <節-区切><節-主辞><節-機能-条件><談話関係:1/4/条件>
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
