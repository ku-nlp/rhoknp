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


def test_to_fstring():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    sentence = Sentence.from_knp(knp_text)
    assert sentence.clauses[0].discourse_relations[0].to_fstring() == "<談話関係:1/4/条件>"


def test_discourse_relation_1():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:2
        * 1D
        + 1D
        服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0
        も も も 助詞 9 副助詞 2 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 2
    discourse_relation_0 = document.clauses[0].discourse_relations[0]
    assert discourse_relation_0 != "foo"
    assert discourse_relation_0.sid == "1"
    assert discourse_relation_0.base_phrase_index == 4
    assert discourse_relation_0.label == DiscourseRelationLabel.CONDITION
    assert discourse_relation_0.modifier == document.clauses[0]
    assert discourse_relation_0.head == document.clauses[1]
    discourse_relation_1 = document.clauses[0].discourse_relations[1]
    assert discourse_relation_1 != "bar"
    assert discourse_relation_1.sid == "2"
    assert discourse_relation_1.base_phrase_index == 1
    assert discourse_relation_1.label == DiscourseRelationLabel.CONDITION
    assert discourse_relation_1.modifier == document.clauses[0]
    assert discourse_relation_1.head == document.clauses[2]


def test_discourse_relation_2():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.clauses[0].discourse_relations) == 1


def test_discourse_relation_3():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * -1D
        + -1D <節-区切><節-主辞>
        耐えろ たえろ 耐える 動詞 2 * 0 母音動詞 1 命令形 6
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:2
        * 1D
        + 1D <節-主辞>
        幸せに しあわせに 幸せだ 形容詞 3 * 0 ナ形容詞 21 ダ列基本連用形 7
        なる なる なる 接尾辞 14 動詞性接尾辞 7 子音動詞ラ行 10 基本形 2
        * -1D
        + -1D <談話関係:1/0/条件(逆方向)><節-区切>
        ため ため ため 名詞 6 副詞的名詞 9 * 0 * 0
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 1
    assert len(document.clauses[1].discourse_relations) == 0
    assert document.clauses[0].discourse_relations[0].label == DiscourseRelationLabel.CONDITION
    assert document.clauses[0].discourse_relations[0].modifier == document.clauses[0]
    assert document.clauses[0].discourse_relations[0].head == document.clauses[1]


def test_invalid_discourse_relation():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * 3D
        + 4D <節-区切><節-主辞><談話関係:1/3/条件;1/5/条件;2/1/条件;2/1/条;4>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
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
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * 3D
        + 4D <節-区切><節-主辞><節-機能-条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
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
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * 3D
        + 4D <節-区切><節-主辞><節-主辞><節-機能-条><節-機能->
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞><節-主辞><節-機能-条件>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
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
        辛い からい 辛い 形容詞 3 * 0 イ形容詞アウオ段 18 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:2
        * 1D
        + 1D <節-前向き機能-逆接>
        しかし しかし しかし 接続詞 10 * 0 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        美味い 美味い 美味い 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
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
        耐えろ たえろ 耐える 動詞 2 * 0 母音動詞 1 命令形 6
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:2
        * 1D
        + 1D <節-主辞>
        幸せに しあわせに 幸せだ 形容詞 3 * 0 ナ形容詞 21 ダ列基本連用形 7
        なる なる なる 接尾辞 14 動詞性接尾辞 7 子音動詞ラ行 10 基本形 2
        * -1D
        + -1D <節-前向き機能-目的><節-区切>
        ため ため ため 名詞 6 副詞的名詞 9 * 0 * 0
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
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
        厳しい きびしい 厳しい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:2
        * 5D
        + 5D <節-前向き機能-逆接>
        しかし しかし しかし 接続詞 10 * 0 * 0 * 0
        * 5D
        + 5D
        彼 かれ 彼 名詞 6 普通名詞 1 * 0 * 0
        は は は 助詞 9 副助詞 2 * 0 * 0
        * 4D
        + 4D
        いつも いつも いつも 副詞 8 * 0 * 0 * 0
        * 4D
        + 4D
        苦難 くなん 苦難 名詞 6 普通名詞 1 * 0 * 0
        を を を 助詞 9 格助詞 1 * 0 * 0
        * 5D
        + 5D <節-機能-原因・理由><節-区切><節-主辞><談話関係:202212161839-0-1/5/原因・理由>
        乗り越えて のりこえて 乗り越える 動詞 2 * 0 母音動詞 1 タ系連用テ形 14
        きた きた くる 接尾辞 14 動詞性接尾辞 7 カ変動詞 14 タ形 10
        から から から 助詞 9 接続助詞 3 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        大丈夫だ だいじょうぶだ 大丈夫だ 形容詞 3 * 0 ナ形容詞 21 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
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
        厳しい きびしい 厳しい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        # S-ID:2
        * 1D
        + 1D <節-前向き機能-原因・理由-逆>
        なぜなら なぜなら なぜなら 接続詞 10 * 0 * 0 * 0
        * -1D
        + -1D <節-前向き機能-原因・理由-逆><節-区切><節-主辞>
        雨 あめ 雨 名詞 6 普通名詞 1 * 0 * 0
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2
        から から から 助詞 9 接続助詞 3 * 0 * 0
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 0
    assert len(document.clauses[1].discourse_relations) == 1
    assert document.clauses[1].discourse_relations[0].head == document.clauses[0]


def test_invalid_backward_clause_function():
    knp_text = textwrap.dedent(
        """\
        # S-ID:2
        * 1D
        + 1D <節-前向き機能-原因・理由><節-前向き機能-原><節-前向き機能->
        なぜなら なぜなら なぜなら 接続詞 10 * 0 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        雨 あめ 雨 名詞 6 普通名詞 1 * 0 * 0
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2
        から から から 助詞 9 接続助詞 3 * 0 * 0
        だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 0
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.clauses[0].discourse_relations) == 0


def test_both():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D
        + 1D
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * 3D
        + 4D <節-区切><節-主辞><節-機能-条件><談話関係:1/4/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13
        * 3D
        + 3D
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0
        + 4D
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0
        が が が 助詞 9 格助詞 1 * 0 * 0
        * -1D
        + -1D <節-区切><節-主辞>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 1
    assert document.clauses[0].discourse_relations[0].is_explicit is True
