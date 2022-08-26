import textwrap

import pytest

from rhoknp import BasePhrase, Document, Sentence

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
        "num": 3,
        "parent_ids": [1, 2, -1],
        "children_ids": [[], [0], [1]],
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
        "num": 3,
        "parent_ids": [2, 2, -1],
        "children_ids": [[], [], [0, 1]],
    },
    {
        "knp": textwrap.dedent(
            """\
            # S-ID:1
            *
            +
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            *
            +
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL
            *
            +
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物"
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
        "num": 3,
        "parent_ids": None,
        "children_ids": None,
    },
]


KNP_SNIPPETS = [
    {
        "knp": textwrap.dedent(
            """\
            + 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            """
        ),
        "text": "天気が",
        "morpheme_num": 2,
        "head_text": "天気",
    },
    {
        "knp": textwrap.dedent(
            """\
            + 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去><格関係0:ガ:天気><格解析結果:良い/よい:形5:ガ/C/天気/0/0/1;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:良い/よい>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
            """
        ),
        "text": "いいので",
        "morpheme_num": 2,
        "head_text": "いい",
    },
    {
        "knp": textwrap.dedent(
            """\
            + -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位><格解析結果:散歩/さんぽ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:散歩/さんぽ>
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            """
        ),
        "text": "散歩した。",
        "morpheme_num": 3,
        "head_text": "散歩",
    },
    {
        "knp": textwrap.dedent(
            """\
            + 2D <文頭><組織名疑><ハ><助詞><体言><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:EOS/EOS><主辞代表表記:EOS/EOS><解析格:ガ>
            EOS EOS EOS 名詞 6 組織名 6 * 0 * 0 "未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS 品詞変更:EOS-EOS-EOS-15-3-0-0" <未知語><品詞推定:名詞><疑似代表表記><代表表記:EOS/EOS><正規化代表表記:EOS/EOS><品詞変更:EOS-EOS-EOS-15-3-0-0-"未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS"><品曖><品曖-アルファベット><品曖-組織名><記英数カ><英記号><記号><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            """
        ),
        "text": "EOSは",
        "morpheme_num": 2,
        "head_text": "EOS",
    },
    {
        "knp": textwrap.dedent(
            """\
            + 2D <BGH:特殊だ/とくしゅだ><文節内><係:文節内><名詞的形容詞語幹><体言><名詞項候補><先行詞候補><非用言格解析:形><正規化代表表記:特殊/とくしゅa>
            特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1 "代表表記:特殊/とくしゅa 代表表記変更:特殊だ/とくしゅだ 反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん" <代表表記:特殊/とくしゅa><反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん><正規化代表表記:特殊/とくしゅa><漢字><かな漢字><名詞的形容詞語幹><代表表記変更:特殊だ/とくしゅだ><名詞相当語><自立><内容語><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
            """
        ),
        "text": "特殊",
        "morpheme_num": 1,
        "head_text": "特殊",
    },
    {
        "knp": textwrap.dedent(
            """\
            + -1D <BGH:記号/きごう><文末><句点><体言><判定詞><用言:判><レベル:C><区切:5-5><ID:（文末）><裸名詞><係:文末><提題受:30><主節><格要素><連用要素><状態述語><敬語:丁寧表現><判定詞句><名詞項候補><先行詞候補><正規化代表表記:記号/きごう><主辞代表表記:記号/きごう><用言代表表記:記号/きごう><節-区切><節-主辞><時制:非過去><格関係0:ガ:EOS><格解析結果:記号/きごう:判3:ガ/N/EOS/0/0/1><標準用言代表表記:記号/きごう>
            記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物" <代表表記:記号/きごう><カテゴリ:抽象物><正規化代表表記:記号/きごう><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27 NIL <かな漢字><ひらがな><活用語><表現文末><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            """
        ),
        "text": "記号です。",
        "morpheme_num": 3,
        "head_text": "記号",
    },
    {
        "knp": textwrap.dedent(
            """\
            + -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
            """
        ),
        "text": "。",
        "morpheme_num": 1,
        "head_text": "。",
    },
    {
        "knp": textwrap.dedent(
            """\
            + -1D <BGH:円/えん><文頭><文末><カウンタ:円><数量><体言><用言:判><体言止><一文字漢字><レベル:C><区切:5-5><ID:（文末）><修飾><提題受:30><主節><状態述語><判定詞句><正規化代表表記:三/さん+円/えん><主辞代表表記:三/さん+円/えん><用言代表表記:円/えん><節-区切><節-主辞><時制:非過去><格解析結果:円/えん:判0:ガ/U/-/-/-/-;ニ/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-;ノ/U/-/-/-/-;ノ/U/-/-/-/-;ニツク/U/-/-/-/-><標準用言代表表記:円/えん>
            三 さん 三 名詞 6 数詞 7 * 0 * 0 "カテゴリ:数量 疑似代表表記 代表表記:三/さん" <カテゴリ:数量><疑似代表表記><代表表記:三/さん><正規化代表表記:三/さん><漢字><かな漢字><数字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始>
            円 えん 円 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0 "代表表記:円/えん 準内容語" <代表表記:円/えん><準内容語><正規化代表表記:円/えん><カウンタ><漢字><かな漢字><文末><表現文末><付属><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            """
        ),
        "text": "三円",
        "morpheme_num": 2,
        "head_text": "円",
    },
]


@pytest.mark.parametrize("case", CASES)
def test_document(case: dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    for base_phrase in doc.base_phrases:
        assert base_phrase.document == doc


@pytest.mark.parametrize("case", CASES)
def test_sentence(case: dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    for base_phrase in sent.base_phrases:
        assert base_phrase.sentence == sent


@pytest.mark.parametrize("case", CASES)
def test_num_document(case: dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    assert len(doc.base_phrases) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_num_sentence(case: dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    assert len(sent.base_phrases) == case["num"]


@pytest.mark.parametrize("case", CASES)
def test_parent_document(case: dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    if case["parent_ids"] is not None:
        assert [bp.parent.index if bp.parent else -1 for bp in doc.base_phrases] == case["parent_ids"]
    else:
        with pytest.raises(AttributeError):
            _ = [bp.parent for bp in doc.base_phrases]


@pytest.mark.parametrize("case", CASES)
def test_parent_sentence(case: dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    if case["parent_ids"] is not None:
        assert [bp.parent.index if bp.parent else -1 for bp in sent.base_phrases] == case["parent_ids"]
    else:
        with pytest.raises(AttributeError):
            _ = [bp.parent for bp in sent.base_phrases]


@pytest.mark.parametrize("case", CASES)
def test_children_document(case: dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    if case["children_ids"] is not None:
        assert [[child.index for child in bp.children] for bp in doc.base_phrases] == case["children_ids"]
    else:
        with pytest.raises(AttributeError):
            _ = [bp.children for bp in doc.base_phrases]


@pytest.mark.parametrize("case", CASES)
def test_children_sentence(case: dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    if case["children_ids"] is not None:
        assert [[child.index for child in bp.children] for bp in sent.base_phrases] == case["children_ids"]
    else:
        with pytest.raises(AttributeError):
            _ = [bp.children for bp in sent.base_phrases]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_from_knp(case: dict[str, str]) -> None:
    _ = BasePhrase.from_knp(case["knp"])


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_to_knp(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert base_phrase.to_knp() == case["knp"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_text(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert base_phrase.text == case["text"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_document_error(case: dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        base_phrase = BasePhrase.from_knp(case["knp"])
        _ = base_phrase.document


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_sentence_error(case: dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        base_phrase = BasePhrase.from_knp(case["knp"])
        _ = base_phrase.sentence


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_clause_error(case: dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        base_phrase = BasePhrase.from_knp(case["knp"])
        _ = base_phrase.clause


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_phrase_error(case: dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        base_phrase = BasePhrase.from_knp(case["knp"])
        _ = base_phrase.phrase


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_morpheme_num(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert len(base_phrase.morphemes) == case["morpheme_num"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_head_text(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert base_phrase.head.text == case["head_text"]


def test_no_pas():
    base_phrase = BasePhrase.from_knp(
        textwrap.dedent(
            """\
            + -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
            """
        )
    )
    assert base_phrase.pas is None


def test_discourse_relation_tag():
    base_phrase = BasePhrase.from_knp(
        textwrap.dedent(
            """\
            + -1D <節-主辞><節-区切><談話関係:1/1/原因・理由>
            吹く ふく 吹く 動詞 2 * 0 子音動詞カ行 2 基本形 2 "代表表記:吹く/ふく 補文ト" <代表表記:吹く/ふく>
            """
        )
    )
    assert base_phrase.discourse_relation_tag.to_fstring() == "<談話関係:1/1/原因・理由>"
