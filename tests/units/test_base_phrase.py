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
    {
        "knp": textwrap.dedent(
            """\
            # S-ID:202209271752-05054-00 kwja:1.0.0
            * 1D
            + 1D
            > ＞ > 特殊 1 括弧終 4 * 0 * 0
                  特殊 1 記号 5 * 0 * 0
                  特殊 1 記号 5 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * 2D
            + 2D <rel type="ガ" target=">" sid="202209271752-05054-00" id="0"/><rel type="ニ" target="不特定:人"/><用言:動><時制:非過去><レベル:C><動態述語><節-区切:補文><節-主辞>
            論じ ろんじ 論じる 動詞 2 * 0 母音動詞 1 未然形 3 <基本句-主辞><用言表記先頭>
            られる られる られる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 <用言表記末尾>
            と と と 助詞 9 格助詞 1 * 0 * 0
            * 3D
            + 3D <用言:動><時制:非過去><レベル:A-><動態述語>
            いう いう いう 動詞 2 * 0 子音動詞ワ行 12 基本形 2 <基本句-主辞>
            * 4D
            + 4D <体言>
            こと こと こと 名詞 6 形式名詞 8 * 0 * 0 <基本句-主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0
            * -1D
            + -1D <rel type="ガ" target="こと" sid="202209271752-05054-00" id="3"/><用言:形><時制:非過去><節-区切><レベル:C><状態述語><敬語:丁寧表現><節-主辞>
            少ない すくない 少ない 形容詞 3 * 0 イ形容詞アウオ段 18 基本形 2 <基本句-主辞><用言表記先頭><用言表記末尾>
            です です です 助動詞 5 * 0 無活用型 26 基本形 2
            ね ね ね 助詞 9 終助詞 4 * 0 * 0
            。 。 。 特殊 1 句点 1 * 0 * 0
            EOS
            """
        ),
        "num": 5,
        "parent_ids": [1, 2, 3, 4, -1],
        "children_ids": [[], [0], [1], [2], [3]],
    },
    {
        "knp": textwrap.dedent(
            """\
            # S-ID:202211041803-0-0 kwja:1.2.0
            * 2D
            + 2D <体言>
            ” ” ” 特殊 1 記号 5 * 0 * 0 <基本句-主辞>
            は は は 助詞 9 副助詞 2 * 0 * 0 "代表表記:は/は" <代表表記:は/は>
            * 2D
            + 2D <体言><係:ノ格>
            記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物" <代表表記:記号/きごう><カテゴリ:抽象物><基本句-主辞>
            の の の 助詞 9 接続助詞 3 * 0 * 0 "代表表記:の/の" <代表表記:の/の>
            * -1D
            + -1D <rel type="ガ" target="”" sid="202211041803-0-0" id="0"/><rel type="ノ" target="記号" sid="202211041803-0-0" id="1"/><用言:判><体言><時制:非過去><節-区切><レベル:C><状態述語><節-主辞>
            一種 いっしゅ 一種 名詞 6 普通名詞 1 * 0 * 0 <基本句-主辞><用言表記先頭><用言表記末尾>
            だ だ だ 判定詞 4 * 0 判定詞 25 基本形 2 "代表表記:だ/だ" <代表表記:だ/だ>
            EOS
            """
        ),
        "num": 3,
        "parent_ids": [2, 2, -1],
        "children_ids": [[], [], [0, 1]],
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


@pytest.mark.parametrize("case", CASES)
def test_index_sentence(case: dict[str, str]) -> None:
    sent = Sentence.from_knp(case["knp"])
    for index, base_phrase in enumerate(sent.base_phrases):
        assert base_phrase.index == index
        assert base_phrase.global_index == index


@pytest.mark.parametrize("case", CASES)
def test_index_document(case: dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    for index, base_phrase in enumerate(doc.base_phrases):
        assert base_phrase.global_index == index


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_from_knp(case: dict[str, str]) -> None:
    _ = BasePhrase.from_knp(case["knp"])


def test_from_knp_error() -> None:
    with pytest.raises(ValueError, match="malformed base phrase line: MALFORMED LINE"):
        _ = BasePhrase.from_knp("MALFORMED LINE")


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_to_knp(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert base_phrase.to_knp() == case["knp"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_text(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert base_phrase.text == case["text"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_morpheme_num(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert len(base_phrase.morphemes) == case["morpheme_num"]


@pytest.mark.parametrize("case", KNP_SNIPPETS)
def test_head_text(case: dict[str, str]) -> None:
    base_phrase = BasePhrase.from_knp(case["knp"])
    assert base_phrase.head.text == case["head_text"]


def test_empty_sid() -> None:
    document = Document.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * -1D
            + -1D <rel type="ガ" target="天気" sid="" id="0"/>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
            EOS
            """
        )
    )
    assert document.base_phrases[1].rel_tags[0].sid == ""
    arguments = document.base_phrases[1].pas.get_arguments("ガ")
    assert len(arguments) == 1
    assert str(arguments[0]) == "天気が"


def test_out_of_range_id() -> None:
    document = Document.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * -1D
            + -1D <rel type="ガ" target="天気" sid="000-0-0" id="10"/>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
            EOS
            """
        )
    )
    assert document.base_phrases[1].pas.get_all_arguments() == {}


def test_rel_target_mismatch() -> None:
    document = Document.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 1D
            + 1D
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * -1D
            + -1D <rel type="ガ" target="転機" sid="000-0-0" id="0"/>
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2
            EOS
            """
        )
    )
    arguments = document.base_phrases[1].pas.get_arguments("ガ")
    assert len(arguments) == 1
    assert str(arguments[0]) == "天気が"


def test_unknown_rel_type() -> None:
    document = Document.from_knp(
        textwrap.dedent(
            """\
            # S-ID:000-0-0
            * 3D
            + 3D
            日本 にほん 日本 名詞 6 地名 4 * 0 * 0
            は は は 助詞 9 副助詞 2 * 0 * 0
            * 3D
            + 3D
            京都 きょうと 京都 名詞 6 地名 4 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * 3D
            + 3D
            冬 ふゆ 冬 名詞 6 時相名詞 10 * 0 * 0
            が が が 助詞 9 格助詞 1 * 0 * 0
            * -1D
            + -1D <rel type="ガ" target="冬" sid="000-0-0" id="2"/><rel type="ガ２" target="京都" sid="000-0-0" id="1"/><rel type="ガ３" target="日本" sid="000-0-0" id="0"/>
            寒い さむい 寒い 形容詞 3 * 0 イ形容詞アウオ段 18 基本形 2
            EOS
            """
        )
    )
    arguments = document.base_phrases[3].pas.get_arguments("ガ３")
    assert len(arguments) == 1
    assert str(arguments[0]) == "日本は"
