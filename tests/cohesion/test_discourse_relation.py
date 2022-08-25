import textwrap
from typing import List

import pytest

from rhoknp import Document, Sentence
from rhoknp.cohesion.discourse_relation import DiscourseRelation, DiscourseRelationTag, DiscourseRelationTagValue


@pytest.mark.parametrize("sid, base_phrase_index, label, fstring", [("1", 0, "原因・理由", "1/0/原因・理由")])
def test_discourse_relation_tag_value(sid: str, base_phrase_index: int, label: str, fstring: str) -> None:
    v = DiscourseRelationTagValue(sid, base_phrase_index, label)
    assert v.sid == sid
    assert v.base_phrase_index == base_phrase_index
    assert v.label == label
    assert v.to_fstring() == fstring


@pytest.mark.parametrize(
    "fstring, values",
    [
        ("<談話関係:1/0/原因・理由>", [DiscourseRelationTagValue("1", 0, "原因・理由")]),
        (
            "<談話関係:1/0/原因・理由;2/1/原因・理由>",
            [DiscourseRelationTagValue("1", 0, "原因・理由"), DiscourseRelationTagValue("2", 1, "原因・理由")],
        ),
        (
            "<節-区切><談話関係:1/0/原因・理由;2/1/原因・理由>",
            [DiscourseRelationTagValue("1", 0, "原因・理由"), DiscourseRelationTagValue("2", 1, "原因・理由")],
        ),
        ("<節-区切>", []),
    ],
)
def test_discourse_relation_tag(fstring: str, values: List[DiscourseRelationTagValue]) -> None:
    discourse_relation_tag = DiscourseRelationTag.from_fstring(fstring)
    assert discourse_relation_tag.values == values


def test_document():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-2ad4f6df
        * 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ>
        + 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ><解析格:ガ>
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓" <代表表記:風/かぜ><カテゴリ:抽象物><漢字読み:訓><正規化代表表記:風/かぜ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく>
        + 4D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく><用言代表表記:吹く/ふく><節-区切><節-主辞><節-機能-条件><格関係0:ガ:風><格解析結果:吹く/ふく:動1:ガ/C/風/0/0/1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:吹く/ふく><談話関係:1/4/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト" <代表表記:吹く/ふく><補文ト><正規化代表表記:吹く/ふく><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 3D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:桶/おけ+屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や>
        + 3D <BGH:桶/おけ><文節内><係:文節内><体言><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:桶/おけ>
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他" <代表表記:桶/おけ><ドメイン:家庭・暮らし><カテゴリ:人工物-その他><正規化代表表記:桶/おけ><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始>
        + 4D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や><解析格:ガ>
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓" <代表表記:屋/や><カテゴリ:場所-施設><漢字読み:訓><正規化代表表記:屋/や><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
        + -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係3:ガ:屋><格解析結果:儲かる/もうかる:動2:ガ/C/屋/3/0/1><標準用言代表表記:儲かる/もうかる>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        # S-ID:2 KNP:5.0-2ad4f6df
        * 1D <文頭><モ><助詞><体言><係:未格><並キ:名:&ST:2.5&&モ><区切:1-4><並列タイプ:AND><格要素><連用要素><正規化代表表記:服屋/服屋><主辞代表表記:服屋/服屋><並列類似度:-100.000>
        + 1D <文頭><モ><助詞><体言><係:未格><並キ:名:&ST:2.5&&モ><区切:1-4><並列タイプ:AND><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:服屋/服屋><主辞代表表記:服屋/服屋><解析格:ガ>
        服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipediaページ内一覧:ドラゴンボールの登場人物 読み不明 疑似代表表記 代表表記:服屋/服屋" <自動獲得:Wikipedia><Wikipediaページ内一覧:ドラゴンボールの登場人物><読み不明><疑似代表表記><代表表記:服屋/服屋><正規化代表表記:服屋/服屋><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        も も も 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:儲かる/もうかる><文末><モ〜><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
        + -1D <BGH:儲かる/もうかる><文末><モ〜><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係0:ガ:服屋><格解析結果:儲かる/もうかる:動11:ガ/N/服屋/0/0/2;ニ/U/-/-/-/-;デ/U/-/-/-/-><標準用言代表表記:儲かる/もうかる>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 2
    discourse_relation_0 = document.clauses[0].discourse_relations[0]
    assert discourse_relation_0.sid == "1"
    assert discourse_relation_0.base_phrase_index == 4
    assert discourse_relation_0.label == "条件"
    assert discourse_relation_0.modifier == document.clauses[0]
    assert discourse_relation_0.head == document.clauses[1]
    discourse_relation_1 = document.clauses[0].discourse_relations[1]
    assert discourse_relation_1.sid == "2"
    assert discourse_relation_1.base_phrase_index == 1
    assert discourse_relation_1.label == "条件"
    assert discourse_relation_1.modifier == document.clauses[0]
    assert discourse_relation_1.head == document.clauses[2]


def test_document_out_of_range():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-2ad4f6df
        * 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ>
        + 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ><解析格:ガ>
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓" <代表表記:風/かぜ><カテゴリ:抽象物><漢字読み:訓><正規化代表表記:風/かぜ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく>
        + 4D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく><用言代表表記:吹く/ふく><節-区切><節-主辞><節-機能-条件><格関係0:ガ:風><格解析結果:吹く/ふく:動1:ガ/C/風/0/0/1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:吹く/ふく><談話関係:1/3/条件;1/5/条件;2/1/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト" <代表表記:吹く/ふく><補文ト><正規化代表表記:吹く/ふく><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 3D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:桶/おけ+屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や>
        + 3D <BGH:桶/おけ><文節内><係:文節内><体言><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:桶/おけ>
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他" <代表表記:桶/おけ><ドメイン:家庭・暮らし><カテゴリ:人工物-その他><正規化代表表記:桶/おけ><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始>
        + 4D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や><解析格:ガ>
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓" <代表表記:屋/や><カテゴリ:場所-施設><漢字読み:訓><正規化代表表記:屋/や><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
        + -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係3:ガ:屋><格解析結果:儲かる/もうかる:動2:ガ/C/屋/3/0/1><標準用言代表表記:儲かる/もうかる>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.clauses[0].discourse_relations) == 0


def test_sentence():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-2ad4f6df
        * 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ>
        + 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ><解析格:ガ>
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓" <代表表記:風/かぜ><カテゴリ:抽象物><漢字読み:訓><正規化代表表記:風/かぜ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく>
        + 4D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく><用言代表表記:吹く/ふく><節-区切><節-主辞><節-機能-条件><格関係0:ガ:風><格解析結果:吹く/ふく:動1:ガ/C/風/0/0/1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:吹く/ふく><談話関係:1/4/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト" <代表表記:吹く/ふく><補文ト><正規化代表表記:吹く/ふく><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 3D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:桶/おけ+屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や>
        + 3D <BGH:桶/おけ><文節内><係:文節内><体言><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:桶/おけ>
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他" <代表表記:桶/おけ><ドメイン:家庭・暮らし><カテゴリ:人工物-その他><正規化代表表記:桶/おけ><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始>
        + 4D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や><解析格:ガ>
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓" <代表表記:屋/や><カテゴリ:場所-施設><漢字読み:訓><正規化代表表記:屋/や><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
        + -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係3:ガ:屋><格解析結果:儲かる/もうかる:動2:ガ/C/屋/3/0/1><標準用言代表表記:儲かる/もうかる>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.clauses[0].discourse_relations) == 1


def test_modify_discourse_relations():
    knp_text = textwrap.dedent(
        """\
        # S-ID:1 KNP:5.0-2ad4f6df
        * 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ>
        + 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ><解析格:ガ>
        風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓" <代表表記:風/かぜ><カテゴリ:抽象物><漢字読み:訓><正規化代表表記:風/かぜ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * 3D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく>
        + 4D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく><用言代表表記:吹く/ふく><節-区切><節-主辞><節-機能-条件><格関係0:ガ:風><格解析結果:吹く/ふく:動1:ガ/C/風/0/0/1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:吹く/ふく><談話関係:1/4/条件>
        吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト" <代表表記:吹く/ふく><補文ト><正規化代表表記:吹く/ふく><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        * 3D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:桶/おけ+屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や>
        + 3D <BGH:桶/おけ><文節内><係:文節内><体言><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:桶/おけ>
        桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他" <代表表記:桶/おけ><ドメイン:家庭・暮らし><カテゴリ:人工物-その他><正規化代表表記:桶/おけ><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始>
        + 4D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や><解析格:ガ>
        屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓" <代表表記:屋/や><カテゴリ:場所-施設><漢字読み:訓><正規化代表表記:屋/や><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞>
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
        * -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
        + -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係3:ガ:屋><格解析結果:儲かる/もうかる:動2:ガ/C/屋/3/0/1><標準用言代表表記:儲かる/もうかる>
        儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
        EOS
        """
    )
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.clauses[0].discourse_relations) == 1
    assert len(sentence.clauses[0].end.discourse_relation_tag) == 1
    r = DiscourseRelation("1", 4, "原因・理由", sentence.clauses[0], sentence.clauses[1])
    sentence.clauses[0].discourse_relations.append(r)
    assert len(sentence.clauses[0].discourse_relations) == 2
    assert len(sentence.clauses[0].end.discourse_relation_tag) == 1  # not reflected
