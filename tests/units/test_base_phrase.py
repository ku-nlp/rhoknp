import textwrap

import pytest

from rhoknp import BasePhrase, Document, Sentence


@pytest.mark.parametrize(
    "knp, base_phrase_texts",
    [
        (
            """# S-ID:1 KNP:5.0-2ad4f6df DATE:2021/08/05 SCORE:-10.73865
* 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
+ 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
* 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><正規化代表表記:良い/よい><主辞代表表記:良い/よい>
+ 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去><格関係0:ガ:天気><格解析結果:良い/よい:形5:ガ/C/天気/0/0/2;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:良い/よい>
いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
* -1D <BGH:散歩/さんぽ+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ>
+ -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位><格解析結果:散歩/さんぽ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:散歩/さんぽ>
散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
EOS""",
            ["天気が", "いいので", "散歩した。"],
        ),
        (
            """# S-ID:1 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:-17.80638
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
""",
            ["EOSは", "特殊", "記号です。"],
        ),
        (
            """# S-ID:2 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:0.00000
* -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語>
+ -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
EOS
""",
            ["。"],
        ),
    ],
)
def test_document_from_knp(knp: str, base_phrase_texts: list[str]) -> None:
    doc = Document.from_knp(knp)
    assert [str(base_phrase) for base_phrase in doc.base_phrases] == base_phrase_texts


@pytest.mark.parametrize(
    "knp, parent_indexes",
    [
        (
            """# S-ID:1 KNP:5.0-2ad4f6df DATE:2021/08/05 SCORE:-10.73865
* 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
+ 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
* 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><正規化代表表記:良い/よい><主辞代表表記:良い/よい>
+ 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去><格関係0:ガ:天気><格解析結果:良い/よい:形5:ガ/C/天気/0/0/2;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:良い/よい>
いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
* -1D <BGH:散歩/さんぽ+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ>
+ -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位><格解析結果:散歩/さんぽ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:散歩/さんぽ>
散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
EOS""",
            [1, 2, -1],
        ),
        (
            """# S-ID:1 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:-17.80638
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
""",
            [2, 2, -1],
        ),
        (
            """# S-ID:2 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:0.00000
* -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語>
+ -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
EOS
""",
            [-1],
        ),
    ],
)
def test_parent(knp: str, parent_indexes: list[int]) -> None:
    sent = Sentence.from_knp(knp)
    for i, parent_index in enumerate(parent_indexes):
        if parent_index >= 0:
            assert sent.base_phrases[i].parent == sent.base_phrases[parent_index]
        else:
            assert sent.base_phrases[i].parent is None


@pytest.mark.parametrize(
    "knp, child_indexes",
    [
        (
            """# S-ID:1 KNP:5.0-2ad4f6df DATE:2021/08/05 SCORE:-10.73865
* 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
+ 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
* 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><正規化代表表記:良い/よい><主辞代表表記:良い/よい>
+ 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去><格関係0:ガ:天気><格解析結果:良い/よい:形5:ガ/C/天気/0/0/2;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:良い/よい>
いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
* -1D <BGH:散歩/さんぽ+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ>
+ -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位><格解析結果:散歩/さんぽ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:散歩/さんぽ>
散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
EOS""",
            [[], [0], [1]],
        ),
        (
            """# S-ID:1 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:-17.80638
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
""",
            [[], [], [0, 1]],
        ),
        (
            """# S-ID:2 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:0.00000
* -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語>
+ -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
EOS
""",
            [[]],
        ),
    ],
)
def test_children(knp: str, child_indexes: list[list[int]]) -> None:
    sent = Sentence.from_knp(knp)
    for i, child_index in enumerate(child_indexes):
        assert sent.base_phrases[i].children == [
            sent.base_phrases[j] for j in child_index
        ]


@pytest.mark.parametrize(
    "knp",
    [
        """+ 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物" <代表表記:天気/てんき><カテゴリ:抽象物><正規化代表表記:天気/てんき><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
""",
        """+ 2D <BGH:良い/よい><用言:形><係:連用><レベル:B+><区切:3-5><ID:〜ので><提題受:20><連用要素><連用節><状態述語><節-機能-原因・理由:ので><正規化代表表記:良い/よい><主辞代表表記:良い/よい><用言代表表記:良い/よい><節-区切><節-主辞><時制:非過去><格関係0:ガ:天気><格解析結果:良い/よい:形5:ガ/C/天気/0/0/2;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:良い/よい>
いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい" <代表表記:良い/よい><反義:形容詞:悪い/わるい><正規化代表表記:良い/よい><かな漢字><ひらがな><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL <かな漢字><ひらがな><活用語><付属>
""",
        """+ -1D <BGH:散歩/さんぽ+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:散歩/さんぽ><主辞代表表記:散歩/さんぽ><用言代表表記:散歩/さんぽ><節-区切><節-主辞><主題格:一人称優位><格解析結果:散歩/さんぽ:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;マデ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:散歩/さんぽ>
散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物" <代表表記:散歩/さんぽ><ドメイン:レクリエーション><カテゴリ:抽象物><正規化代表表記:散歩/さんぽ><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
""",
        """+ 2D <文頭><組織名疑><ハ><助詞><体言><係:未格><提題><区切:3-5><主題表現><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:EOS/EOS><主辞代表表記:EOS/EOS><解析格:ガ>
EOS EOS EOS 名詞 6 組織名 6 * 0 * 0 "未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS 品詞変更:EOS-EOS-EOS-15-3-0-0" <未知語><品詞推定:名詞><疑似代表表記><代表表記:EOS/EOS><正規化代表表記:EOS/EOS><品詞変更:EOS-EOS-EOS-15-3-0-0-"未知語:ローマ字 品詞推定:名詞 疑似代表表記 代表表記:EOS/EOS"><品曖><品曖-アルファベット><品曖-組織名><記英数カ><英記号><記号><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
は は は 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
""",
        """+ 2D <BGH:特殊だ/とくしゅだ><文節内><係:文節内><名詞的形容詞語幹><体言><名詞項候補><先行詞候補><非用言格解析:形><正規化代表表記:特殊/とくしゅa>
特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1 "代表表記:特殊/とくしゅa 代表表記変更:特殊だ/とくしゅだ 反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん" <代表表記:特殊/とくしゅa><反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん><正規化代表表記:特殊/とくしゅa><漢字><かな漢字><名詞的形容詞語幹><代表表記変更:特殊だ/とくしゅだ><名詞相当語><自立><内容語><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
""",
        """+ -1D <BGH:記号/きごう><文末><句点><体言><判定詞><用言:判><レベル:C><区切:5-5><ID:（文末）><裸名詞><係:文末><提題受:30><主節><格要素><連用要素><状態述語><敬語:丁寧表現><判定詞句><名詞項候補><先行詞候補><正規化代表表記:記号/きごう><主辞代表表記:記号/きごう><用言代表表記:記号/きごう><節-区切><節-主辞><時制:非過去><格関係0:ガ:EOS><格解析結果:記号/きごう:判3:ガ/N/EOS/0/0/1><標準用言代表表記:記号/きごう>
記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物" <代表表記:記号/きごう><カテゴリ:抽象物><正規化代表表記:記号/きごう><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27 NIL <かな漢字><ひらがな><活用語><表現文末><付属>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
""",
        """+ -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
""",
    ],
)
def test_base_phrase_to_knp(knp: str) -> None:
    base_phrase = BasePhrase.from_knp(knp)
    assert base_phrase.to_knp() == knp


def test_base_phrase_phrase():
    base_phrase = BasePhrase.from_knp(
        textwrap.dedent(
            """\
        + -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
        """
        )
    )
    with pytest.raises(AttributeError):
        _ = base_phrase.phrase