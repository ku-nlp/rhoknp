import textwrap
from typing import Dict

import pytest

from rhoknp import Document, Morpheme, Sentence

CASES = [
    {
        "knp": textwrap.dedent(
            """\
            # S-ID:1
            * 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
            + 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><正規化代表表記:良い/よい><主辞代表表記:良い/よい>
            + 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去><格関係0:ガ:天気><格解析結果:良い/よい:形5:ガ/C/天気/0/0/1;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:良い/よい>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            * -1D <BGH:散歩/さんぽ+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ>
            + -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位><格解析結果:散歩/さんぽ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:散歩/さんぽ>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            """
        ),
        "jumanpp": textwrap.dedent(
            """\
            # S-ID:1
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            """
        ),
        "num": 7,
        "parent_ids": [2, 0, 4, 2, -1, 4, 4],
        "children_ids": [[1], [], [0, 3], [], [2, 5, 6], [], []],
    },
    {
        "knp": textwrap.dedent(
            textwrap.dedent(
                """\
                # S-ID:1
                * 1D <文頭><組織名疑><ハ><助詞><体言><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><正規化代表表記:EOS/EOS><主辞代表表記:EOS/EOS>
                + 2D <文頭><組織名疑><ハ><助詞><体言><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:EOS/EOS><主辞代表表記:EOS/EOS><解析格:ガ>
                EOS EOS EOS 名詞 6 組織名 6 * 0 * 0 "未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS 品詞変更:EOS-EOS-EOS-15-3-0-0" <未知語><品詞推定:名詞><疑似代表表記><代表表記:EOS/EOS><正規化代表表記:EOS/EOS><品詞変更:EOS-EOS-EOS-15-3-0-0-"未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS"><品曖><品曖-アルファベット><品曖-組織名><記英数カ><英記号><記号><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
                は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
                * -1D <BGH:記号/きごう><文末><句点><体言><判定詞><用言:判><レベル:C><区切:5-5><ID:（文末）><裸名詞><係:文末><提題受:30><主節><格要素><連用要素><状態述語><敬語:丁寧表現><正規化代表表記:特殊/とくしゅa+記号/きごう><主辞代表表記:記号/きごう>
                + 2D <BGH:特殊だ/とくしゅだ><文節内><係:文節内><名詞的形容詞語幹><体言><名詞項候補><先行詞候補><非用言格解析:形><正規化代表表記:特殊/とくしゅa>
                特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1 "代表表記:特殊/とくしゅa 代表表記変更:特殊だ/とくしゅだ 反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん" <代表表記:特殊/とくしゅa><反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん><正規化代表表記:特殊/とくしゅa><漢字><かな漢字><名詞的形容詞語幹><代表表記変更:特殊だ/とくしゅだ><名詞相当語><自立><内容語><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
                + -1D <BGH:記号/きごう><文末><句点><体言><判定詞><用言:判><レベル:C><区切:5-5><ID:（文末）><裸名詞><係:文末><提題受:30><主節><格要素><連用要素><状態述語><敬語:丁寧表現><判定詞句><名詞項候補><先行詞候補><正規化代表表記:記号/きごう><主辞代表表記:記号/きごう><用言代表表記:記号/きごう><節-区切><節-主辞><時制:非過去><格関係0:ガ:EOS><格解析結果:記号/きごう:判3:ガ/N/EOS/0/0/1><標準用言代表表記:記号/きごう>
                記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物" <代表表記:記号/きごう><カテゴリ:抽象物><正規化代表表記:記号/きごう><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
                です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27 NIL <かな漢字><ひらがな><活用語><表現文末><付属>
                。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
                EOS
                """
            )
        ),
        "jumanpp": textwrap.dedent(
            textwrap.dedent(
                """\
                # S-ID:1
                EOS EOS EOS 名詞 6 組織名 6 * 0 * 0 "未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS 品詞変更:EOS-EOS-EOS-15-3-0-0" <未知語><品詞推定:名詞><疑似代表表記><代表表記:EOS/EOS><正規化代表表記:EOS/EOS><品詞変更:EOS-EOS-EOS-15-3-0-0-"未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS"><品曖><品曖-アルファベット><品曖-組織名><記英数カ><英記号><記号><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
                は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
                特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1 "代表表記:特殊/とくしゅa 代表表記変更:特殊だ/とくしゅだ 反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん" <代表表記:特殊/とくしゅa><反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん><正規化代表表記:特殊/とくしゅa><漢字><かな漢字><名詞的形容詞語幹><代表表記変更:特殊だ/とくしゅだ><名詞相当語><自立><内容語><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
                記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物" <代表表記:記号/きごう><カテゴリ:抽象物><正規化代表表記:記号/きごう><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
                です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27 NIL <かな漢字><ひらがな><活用語><表現文末><付属>
                。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
                EOS
                """
            )
        ),
        "num": 6,
        "parent_ids": [3, 0, 3, -1, 3, 3],
        "children_ids": [[1], [], [], [0, 2, 4, 5], [], []],
    },
    {
        "knp": textwrap.dedent(
            """\
            # S-ID:1
            * 1D
            + 1D
            天気
            が
            * 2D
            + 2D
            いい
            ので
            * -1D
            + -1D
            散歩
            した
            。
            EOS
            """
        ),
        "jumanpp": textwrap.dedent(
            """\
            # S-ID:1
            天気
            が
            いい
            ので
            散歩
            した
            。
            EOS
            """
        ),
        "num": 7,
        "parent_ids": [2, 0, 4, 2, -1, 4, 4],
        "children_ids": [[1], [], [0, 3], [], [2, 5, 6], [], []],
    },
]


JUMANPP_SNIPPETS = [
    {
        "jumanpp": '外国 がいこく 外国 名詞 6 普通名詞 1 * 0 * 0 "代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"\n',
        "text": "外国",
        "surf": "外国",
        "reading": "がいこく",
        "lemma": "外国",
        "pos": "名詞",
        "subpos": "普通名詞",
        "conjtype": "*",
        "conjform": "*",
        "sstring": '"代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"',
        "fstring": "",
        "canon": "外国/がいこく",
    },
    {
        "jumanpp": '人 じん 人 名詞 6 普通名詞 1 * 0 * 0 "代表表記:人/じん カテゴリ:人 漢字読み:音"\n',
        "text": "人",
        "surf": "人",
        "reading": "じん",
        "lemma": "人",
        "pos": "名詞",
        "subpos": "普通名詞",
        "conjtype": "*",
        "conjform": "*",
        "sstring": '"代表表記:人/じん カテゴリ:人 漢字読み:音"',
        "fstring": "",
        "canon": "人/じん",
    },
    {
        "jumanpp": '参政 さんせい 参政 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:参政/さんせい ドメイン:政治 カテゴリ:抽象物"\n',
        "text": "参政",
        "surf": "参政",
        "reading": "さんせい",
        "lemma": "参政",
        "pos": "名詞",
        "subpos": "サ変名詞",
        "conjtype": "*",
        "conjform": "*",
        "sstring": '"代表表記:参政/さんせい ドメイン:政治 カテゴリ:抽象物"',
        "fstring": "",
        "canon": "参政/さんせい",
    },
    {
        "jumanpp": '権 けん 権 名詞 6 普通名詞 1 * 0 * 0 "代表表記:権/けん カテゴリ:抽象物 漢字読み:音"\n',
        "text": "権",
        "surf": "権",
        "reading": "けん",
        "lemma": "権",
        "pos": "名詞",
        "subpos": "普通名詞",
        "conjtype": "*",
        "conjform": "*",
        "sstring": '"代表表記:権/けん カテゴリ:抽象物 漢字読み:音"',
        "fstring": "",
        "canon": "権/けん",
    },
    {
        "jumanpp": textwrap.dedent(
            """\
            母 はは 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/はは 漢字読み:訓 カテゴリ:人 ドメイン:家庭・暮らし"
            @ 母 ぼ 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/ぼ 漢字読み:音 カテゴリ:人"
            """
        ),
        "text": "母",
        "surf": "母",
        "reading": "はは",
        "lemma": "母",
        "pos": "名詞",
        "subpos": "普通名詞",
        "conjtype": "*",
        "conjform": "*",
        "sstring": '"代表表記:母/はは 漢字読み:訓 カテゴリ:人 ドメイン:家庭・暮らし"',
        "fstring": "",
        "canon": "母/はは",
    },
    {
        "jumanpp": "@ @ @ 未定義語 15 その他 1 * 0 * 0\n",
        "text": "@",
        "surf": "@",
        "reading": "@",
        "lemma": "@",
        "pos": "未定義語",
        "subpos": "その他",
        "conjtype": "*",
        "conjform": "*",
        "sstring": "",
        "fstring": "",
        "canon": None,
    },
    {
        "jumanpp": "@ @ @ 未定義語 15 その他 1 * 0 * 0\n",
        "text": "@",
        "surf": "@",
        "reading": "@",
        "lemma": "@",
        "pos": "未定義語",
        "subpos": "その他",
        "conjtype": "*",
        "conjform": "*",
        "sstring": "",
        "fstring": "",
        "canon": None,
    },
    {
        "jumanpp": '走った はしった 走る 動詞 2 * 0 子音動詞ラ行 10 タ形 10 "代表表記:走る/はしる" <代表表記:走る/はしる><正規化代表表記:走る/はしる><かな漢字><活用語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>\n',
        "text": "走った",
        "surf": "走った",
        "reading": "はしった",
        "lemma": "走る",
        "pos": "動詞",
        "subpos": "*",
        "conjtype": "子音動詞ラ行",
        "conjform": "タ形",
        "sstring": '"代表表記:走る/はしる"',
        "fstring": "<代表表記:走る/はしる><正規化代表表記:走る/はしる><かな漢字><活用語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>",
        "canon": "走る/はしる",
    },
    {
        "jumanpp": "であり であり だ 判定詞 4 * 0 判定詞 25 デアル列基本連用形 18 NIL\n",
        "text": "であり",
        "surf": "であり",
        "reading": "であり",
        "lemma": "だ",
        "pos": "判定詞",
        "subpos": "*",
        "conjtype": "判定詞",
        "conjform": "デアル列基本連用形",
        "sstring": "NIL",
        "fstring": "",
        "canon": None,
    },
]


@pytest.mark.parametrize("case", CASES)
def test_document_knp(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    for morpheme in doc.morphemes:
        assert morpheme.document == doc


@pytest.mark.parametrize("case", CASES)
def test_document_jumanpp(case: Dict[str, str]) -> None:
    doc = Document.from_jumanpp(case["jumanpp"])
    for morpheme in doc.morphemes:
        assert morpheme.document == doc


@pytest.mark.parametrize("case", CASES)
def test_sentence_knp(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    for morpheme in sent.morphemes:
        assert morpheme.sentence == sent


@pytest.mark.parametrize("case", CASES)
def test_sentence_jumanpp(case: Dict[str, str]) -> None:
    sent = Sentence.from_jumanpp(case["jumanpp"])
    for morpheme in sent.morphemes:
        assert morpheme.sentence == sent


@pytest.mark.parametrize("case", CASES)
def test_num_document_knp(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert len(doc.morphemes) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_num_document_jumanpp(case: Dict[str, str]) -> None:
    doc = Document.from_jumanpp(case["jumanpp"])
    assert len(doc.morphemes) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_num_sentence_knp(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert len(sent.morphemes) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_num_sentence_jumanpp(case: Dict[str, str]) -> None:
    sent = Sentence.from_jumanpp(case["jumanpp"])
    assert len(sent.morphemes) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_parent_document_knp(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert [morpheme.parent.index if morpheme.parent else -1 for morpheme in doc.morphemes] == case["parent_ids"]


@pytest.mark.parametrize("case", CASES)
def test_parent_document_jumanpp(case: Dict[str, str]) -> None:
    doc = Document.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        assert [morpheme.parent.index if morpheme.parent else -1 for morpheme in doc.morphemes] == case["parent_ids"]


@pytest.mark.parametrize("case", CASES)
def test_parent_sentence_knp(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert [morpheme.parent.index if morpheme.parent else -1 for morpheme in sent.morphemes] == case["parent_ids"]


@pytest.mark.parametrize("case", CASES)
def test_parent_sentence_jumanpp(case: Dict[str, str]) -> None:
    sent = Sentence.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        assert [morpheme.parent.index if morpheme.parent else -1 for morpheme in sent.morphemes] == case["parent_ids"]


@pytest.mark.parametrize("case", CASES)
def test_children_document_knp(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert [[child.index for child in morpheme.children] for morpheme in doc.morphemes] == case["children_ids"]


@pytest.mark.parametrize("case", CASES)
def test_children_document_jumanpp(case: Dict[str, str]) -> None:
    doc = Document.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        assert [[child.index for child in morpheme.children] for morpheme in doc.morphemes] == case["children_ids"]


@pytest.mark.parametrize("case", CASES)
def test_children_sentence_knp(case: Dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert [[child.index for child in morpheme.children] for morpheme in sent.morphemes] == case["children_ids"]


@pytest.mark.parametrize("case", CASES)
def test_children_sentence_jumanpp(case: Dict[str, str]) -> None:
    sent = Sentence.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        assert [[child.index for child in morpheme.children] for morpheme in sent.morphemes] == case["children_ids"]


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_from_jumanpp(case: Dict[str, str]) -> None:
    _ = Morpheme.from_jumanpp(case["jumanpp"])


def test_from_jumanpp_error() -> None:
    jumanpp = "であり であり だ 判定詞 4 * 0 判定詞 25 デアル列基本連用形 18 MALFORMED_STRING\n"
    with pytest.raises(ValueError):
        _ = Morpheme.from_jumanpp(jumanpp)


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_to_jumanpp(case: Dict[str, str]) -> None:
    morpheme = Morpheme.from_jumanpp(case["jumanpp"])
    assert morpheme.to_jumanpp() == case["jumanpp"]


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
@pytest.mark.parametrize(
    "attr",
    ["text", "surf", "reading", "lemma", "pos", "subpos", "conjtype", "conjform", "sstring", "fstring", "canon"],
)
def test_attr(case: Dict[str, str], attr: str) -> None:
    morpheme = Morpheme.from_jumanpp(case["jumanpp"])
    assert getattr(morpheme, attr) == case[attr]


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
@pytest.mark.parametrize(
    "attr",
    ["reading", "lemma", "pos", "subpos", "conjtype", "conjform"],
)
def test_attr_error(case: Dict[str, str], attr: str) -> None:
    morpheme = Morpheme(case["text"])
    with pytest.raises(AttributeError):
        _ = getattr(morpheme, attr)


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_semantics(case: Dict[str, str]) -> None:
    morpheme = Morpheme.from_jumanpp(case["jumanpp"])
    assert morpheme.semantics.to_sstring() == case["sstring"]


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_document_error(case: Dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        morpheme = Morpheme.from_jumanpp(case["jumanpp"])
        _ = morpheme.document


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_sentence_error(case: Dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        morpheme = Morpheme.from_jumanpp(case["jumanpp"])
        _ = morpheme.sentence


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_phrase_error(case: Dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        morpheme = Morpheme.from_jumanpp(case["jumanpp"])
        _ = morpheme.phrase


@pytest.mark.parametrize("case", JUMANPP_SNIPPETS)
def test_base_phrase_error(case: Dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        morpheme = Morpheme.from_jumanpp(case["jumanpp"])
        _ = morpheme.base_phrase


def test_span() -> None:
    jumanpp = textwrap.dedent(
        """\
        天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物"
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
        ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL
        散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物"
        した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    sentence = Sentence.from_jumanpp(jumanpp)
    assert sentence.morphemes[0].span == (0, 2)
    assert sentence.morphemes[1].span == (2, 3)
    assert sentence.morphemes[2].span == (3, 5)
    assert sentence.morphemes[3].span == (5, 7)
    assert sentence.morphemes[4].span == (7, 9)
    assert sentence.morphemes[5].span == (9, 11)
    assert sentence.morphemes[6].span == (11, 12)


def test_span_error() -> None:
    jumanpp = '外国 がいこく 外国 名詞 6 普通名詞 1 * 0 * 0 "代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"\n'
    morpheme = Morpheme.from_jumanpp(jumanpp)
    with pytest.raises(AttributeError):
        _ = morpheme.span


def test_morpheme_homograph() -> None:
    jumanpp = textwrap.dedent(
        """\
        母 はは 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/はは 漢字読み:訓 カテゴリ:人 ドメイン:家庭・暮らし"
        @ 母 ぼ 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/ぼ 漢字読み:音 カテゴリ:人"
        """
    )
    morpheme = Morpheme.from_jumanpp(jumanpp)
    assert len(morpheme.homographs) == 1
    homograph = morpheme.homographs[0]
    assert homograph.surf == "母"
    assert homograph.reading == "ぼ"
    assert homograph.lemma == "母"
    assert homograph.pos == "名詞"
    assert homograph.subpos == "普通名詞"
    assert homograph.conjtype == "*"
    assert homograph.conjform == "*"
    assert homograph.sstring == '"代表表記:母/ぼ 漢字読み:音 カテゴリ:人"'
    assert homograph.fstring == ""


def test_morpheme_homograph_to_knp() -> None:
    knp = textwrap.dedent(
        """\
        # S-ID:1
        * -1D <体言><用言:判>
        + -1D <体言><用言:判>
        母 はは 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/はは ドメイン:家庭・暮らし カテゴリ:人 漢字読み:訓"
        EOS
        """
    )
    jumanpp_homograph = textwrap.dedent(
        """\
        母 はは 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/はは ドメイン:家庭・暮らし カテゴリ:人 漢字読み:訓"
        @ 母 ぼ 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/ぼ 漢字読み:音 カテゴリ:人"
        """
    )
    knp_homograph = textwrap.dedent(
        """\
        # S-ID:1
        * -1D <体言><用言:判>
        + -1D <体言><用言:判>
        母 はは 母 名詞 6 普通名詞 1 * 0 * 0 "代表表記:母/はは ドメイン:家庭・暮らし カテゴリ:人 漢字読み:訓" <ALT-母-ぼ-母-6-1-0-0-"代表表記:母/ぼ 漢字読み:音 カテゴリ:人">
        EOS
        """
    )
    sentence = Sentence.from_knp(knp)
    morpheme_homograph = Morpheme.from_jumanpp(jumanpp_homograph)
    assert len(sentence.morphemes) == 1
    sentence.morphemes[0].homographs = morpheme_homograph.homographs
    assert len(sentence.morphemes[0].homographs) == 1
    assert sentence.morphemes[0].to_jumanpp() == jumanpp_homograph
    assert sentence.to_knp() == knp_homograph


@pytest.mark.parametrize("char", ["#", "*", "+", "@", "EOS", "\u0020"])
def test_control_char(char: str) -> None:
    morpheme = Morpheme.from_jumanpp(char)
    assert morpheme.text == char
    assert morpheme.to_jumanpp() == char + "\n"
