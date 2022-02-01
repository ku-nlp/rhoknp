import textwrap

import pytest

from rhoknp import Phrase, Sentence

cases = [
    {
        "text": r"天気がいいので散歩した。",
        "jumanpp": textwrap.dedent(
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
        ),
        "knp": textwrap.dedent(
            """\
            # S-ID:1 KNP:5.0-2ad4f6df DATE:2021/08/05 SCORE:-10.73865
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
            EOS
            """
        ),
    },
    {
        "text": r"EOSは特殊記号です。",
        "jumanpp": textwrap.dedent(
            """\
            EOS EOS EOS 未定義語 15 アルファベット 3 * 0 * 0 "未知語:ローマ字 品詞推定:名詞"
            は は は 助詞 9 副助詞 2 * 0 * 0 NIL
            特殊 とくしゅ 特殊だ 形容詞 3 * 0 ナノ形容詞 22 語幹 1 "代表表記:特殊だ/とくしゅだ 反義:名詞-普通名詞:一般/いっぱん;名詞-普通名詞:普遍/ふへん"
            記号 きごう 記号 名詞 6 普通名詞 1 * 0 * 0 "代表表記:記号/きごう カテゴリ:抽象物"
            です です だ 判定詞 4 * 0 判定詞 25 デス列基本形 27 NIL
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
        "knp": textwrap.dedent(
            """\
            # S-ID:1 KNP:5.0-2ad4f6df DATE:2021/09/21 SCORE:-17.80638
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
    },
    {
        "text": r"。",
        "jumanpp": textwrap.dedent(
            """\
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
        "knp": textwrap.dedent(
            """\
            # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/24 SCORE:0.00000
            * -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語>
            + -1D <文頭><文末><句点><受けNONE><用言:判><体言止><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><状態述語><判定詞句><用言代表表記:。/。><節-区切><節-主辞><時制:非過去>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文頭><文末><付属><タグ単位始><文節始><用言表記先頭><用言表記末尾><用言意味表記末尾>
            EOS
            """
        ),
    },
    {
        "text": r"顔面を打ちつけ負傷した。",
        "jumanpp": textwrap.dedent(
            """\
            顔面 がんめん 顔面 名詞 6 普通名詞 1 * 0 * 0 "代表表記:顔面/がんめん カテゴリ:場所-その他"
            を を を 助詞 9 格助詞 1 * 0 * 0 NIL
            打ち うち 打つ 動詞 2 * 0 子音動詞タ行 6 基本連用形 8 "代表表記:打つ/うつ ドメイン:スポーツ"
            つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:付ける/つける 可能動詞:付く/つく 補文ト 付属動詞候補（基本）"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:付ける/つける 自他動詞:自:付く/つく 補文ト 付属動詞候補（基本）"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:就ける/つける ドメイン:ビジネス 自他動詞:自:就く/つく"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:就ける/つける 可能動詞:就く/つく ドメイン:ビジネス"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:搗ける/つける 可能動詞:搗く/つく ドメイン:料理・食事"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:浸ける/つける ドメイン:料理・食事 自他動詞:自:浸かる/つかる"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:点ける/つける 自他動詞:自:点く/つく"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:着ける/つける ドメイン:交通 自他動詞:自:着く/つく"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:着ける/つける 可能動詞:着く/つく ドメイン:交通"
            @ つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:突ける/つける 可能動詞:突く/つく"
            負傷 ふしょう 負傷 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:負傷/ふしょう ドメイン:健康・医学 カテゴリ:抽象物"
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
        "knp": textwrap.dedent(
            """\
            # S-ID:1 KNP:5.0-825c01b7 DATE:2021/10/24 SCORE:-14.81311
            * 1D <BGH:顔面/がんめん><文頭><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><正規化代表表記:顔面/がんめん><主辞代表表記:顔面/がんめん>
            + 1D <BGH:顔面/がんめん><文頭><ヲ><助詞><体言><係:ヲ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:顔面/がんめん><主辞代表表記:顔面/がんめん><解析格:ヲ>
            顔面 がんめん 顔面 名詞 6 普通名詞 1 * 0 * 0 "代表表記:顔面/がんめん カテゴリ:場所-その他" <代表表記:顔面/がんめん><カテゴリ:場所-その他><正規化代表表記:顔面/がんめん><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            を を を 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * 2P <BGH:打つ/うつ><補文ト><可能表現><用言:動><係:連用><レベル:B><並キ:述:&レベル:強><区切:3-5><ID:動詞連用><連用要素><連用節><動態述語><正規化代表表記:打つ/うつ><主辞代表表記:打つ/うつ><並列類似度:1.258><並結句数:2><並結文節数:1><提題受:30>
            + 2P <BGH:打つ/うつ><補文ト><可能表現><用言:動><係:連用><レベル:B><並キ:述:&レベル:強><区切:3-5><ID:動詞連用><連用要素><連用節><動態述語><正規化代表表記:打つ/うつ><主辞代表表記:打つ/うつ><用言代表表記:打つ/うつ+付ける/つける><提題受:30><節-区切><節-主辞><時制:非過去><格関係0:ヲ:顔面><格解析結果:打つ/うつ+付ける/つける:動1:ガ/U/-/-/-/-;ヲ/C/顔面/0/0/1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-><標準用言代表表記:打つ/うつ+付ける/つける>
            打ち うち 打つ 動詞 2 * 0 子音動詞タ行 6 基本連用形 8 "代表表記:打つ/うつ ドメイン:スポーツ" <代表表記:打つ/うつ><ドメイン:スポーツ><正規化代表表記:打つ/うつ><かな漢字><活用語><連用形名詞化疑><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭>
            つけ つけ つける 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:付ける/つける 可能動詞:付く/つく 補文ト 付属動詞候補（基本）" <代表表記:付ける/つける><可能動詞:付く/つく><補文ト><付属動詞候補（基本）><正規化代表表記:付ける/つける?就ける/つける?就ける/つける?搗ける/つける?浸ける/つける?点ける/つける?着ける/つける?着ける/つける?突ける/つける><品曖><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:付ける/つける 自他動詞:自:付く/つく 補文ト 付属動詞候補（基本）"><自他動詞:自:着く/つく><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:就ける/つける ドメイン:ビジネス 自他動詞:自:就く/つく"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:就ける/つける 可能動詞:就く/つく ドメイン:ビジネス"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:搗ける/つける 可能動詞:搗く/つく ドメイン:料理・食事"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:浸ける/つける ドメイン:料理・食事 自他動詞:自:浸かる/つかる"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:点ける/つける 自他動詞:自:点く/つく"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:着ける/つける ドメイン:交通 自他動詞:自:着く/つく"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:着ける/つける 可能動詞:着く/つく ドメイン:交通"><ALT-つけ-つけ-つける-2-0-1-8-"代表表記:突ける/つける 可能動詞:突く/つく"><品曖-動詞><原形曖昧><かな漢字><ひらがな><活用語><連用形名詞化疑><付属><用言表記末尾><用言意味表記末尾>
            * -1D <BGH:負傷/ふしょう+する/する><文末><サ変><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:負傷/ふしょう><主辞代表表記:負傷/ふしょう>
            + -1D <BGH:負傷/ふしょう+する/する><文末><サ変動詞><時制:過去><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><サ変><正規化代表表記:負傷/ふしょう><主辞代表表記:負傷/ふしょう><用言代表表記:負傷/ふしょう><節-区切><節-主辞><主題格:一人称優位><格解析結果:負傷/ふしょう:動0:ガ/U/-/-/-/-;ヲ/U/-/-/-/-;ニ/U/-/-/-/-;デ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:負傷/ふしょう>
            負傷 ふしょう 負傷 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:負傷/ふしょう ドメイン:健康・医学 カテゴリ:抽象物" <代表表記:負傷/ふしょう><ドメイン:健康・医学><カテゴリ:抽象物><正規化代表表記:負傷/ふしょう><漢字><かな漢字><名詞相当語><サ変><サ変動詞><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）" <代表表記:する/する><自他動詞:自:成る/なる><付属動詞候補（基本）><正規化代表表記:する/する><かな漢字><ひらがな><活用語><表現文末><とタ系連用テ形複合辞><付属>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            """
        ),
    },
]


@pytest.mark.parametrize("text", [case["text"] for case in cases])
def test_sentence_from_raw_text_0(text: str) -> None:
    sentence = Sentence.from_raw_text(text)
    assert sentence.text == text


@pytest.mark.parametrize("text", [case["text"] for case in cases])
def test_sentence_from_raw_text(text: str) -> None:
    sentence = Sentence(text)
    assert sentence.text == text


@pytest.mark.parametrize(
    "jumanpp, text", [(case["jumanpp"], case["text"]) for case in cases]
)
def test_sentence_from_jumanpp(jumanpp: str, text: str) -> None:
    sentence = Sentence.from_jumanpp(jumanpp)
    assert str(sentence) == text


def test_sentence_clauses() -> None:
    knp = cases[0]["knp"]
    sent = Sentence.from_knp(knp)
    assert len(sent.clauses) == 2


def test_sentence_clauses_error() -> None:
    text = cases[0]["text"]
    doc = Sentence.from_raw_text(text)
    with pytest.raises(AttributeError):
        _ = doc.clauses


def test_sentence_chunks() -> None:
    knp = cases[0]["knp"]
    sent = Sentence.from_knp(knp)
    assert len(sent.phrases) == 3


def test_sentence_chunks_error() -> None:
    text = cases[0]["text"]
    sent = Sentence.from_raw_text(text)
    with pytest.raises(AttributeError):
        _ = sent.phrases


def test_sentence_phrases() -> None:
    knp = cases[0]["knp"]
    sent = Sentence.from_knp(knp)
    assert len(sent.base_phrases) == 3


def test_sentence_phrases_error() -> None:
    text = cases[0]["text"]
    sent = Sentence.from_raw_text(text)
    with pytest.raises(AttributeError):
        _ = sent.base_phrases


def test_sentence_morphemes() -> None:
    knp = cases[0]["knp"]
    sent = Sentence.from_knp(knp)
    assert len(sent.morphemes) == 7


def test_sentence_morphemes_error() -> None:
    text = cases[0]["text"]
    sent = Sentence.from_raw_text(text)
    with pytest.raises(AttributeError):
        _ = sent.morphemes


@pytest.mark.parametrize("jumanpp", [case["jumanpp"] for case in cases])
def test_sentence_to_jumanpp(jumanpp: str) -> None:
    sentence = Sentence.from_jumanpp(jumanpp)
    assert sentence.to_jumanpp() == jumanpp


@pytest.mark.parametrize("knp, text", [(case["knp"], case["text"]) for case in cases])
def test_sentence_from_knp(knp: str, text: str) -> None:
    sentence = Sentence.from_knp(knp)
    assert str(sentence) == text


# TODO: support <ALT> tag
@pytest.mark.parametrize("knp", [case["knp"] for case in cases[:3]])
def test_sentence_to_knp(knp: str) -> None:
    sentence = Sentence.from_knp(knp)
    assert sentence.to_knp() == knp


def test_sentence_need_jumanpp() -> None:
    text = cases[0]["text"]
    sent = Sentence.from_raw_text(text)
    assert sent.need_jumanpp is True
    jumanpp = cases[0]["jumanpp"]
    sent = Sentence.from_jumanpp(jumanpp)
    assert sent.need_jumanpp is False


def test_sentence_need_knp() -> None:
    jumanpp = cases[0]["jumanpp"]
    sent = Sentence.from_jumanpp(jumanpp)
    assert sent.need_knp is True
    knp = cases[0]["knp"]
    sent = Sentence.from_knp(knp)
    assert sent.need_knp is False


@pytest.mark.parametrize("knp", [case["knp"] for case in cases])
def test_sentence_sid(knp: str) -> None:
    sentence = Sentence.from_knp(knp)
    assert sentence.sid == "1"


def test_child_units_kwdlc():
    sent = Sentence.from_knp(
        textwrap.dedent(
            """\
        # S-ID:w201106-0000060050-1 JUMAN:6.1-20101108 KNP:3.1-20101107 DATE:2011/06/21 SCORE:-44.94406 MOD:2017/10/15 MEMO:
        * 2D
        + 1D
        コイン こいん コイン 名詞 6 普通名詞 1 * 0 * 0
        + 3D <rel type="ガ" target="不特定:人"/><rel type="ヲ" target="コイン" sid="w201106-0000060050-1" id="0"/>
        トス とす トス 名詞 6 サ変名詞 2 * 0 * 0
        を を を 助詞 9 格助詞 1 * 0 * 0
        * 2D
        + 3D
        ３ さん ３ 名詞 6 数詞 7 * 0 * 0
        回 かい 回 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0
        * -1D
        + -1D <rel type="ガ" target="不特定:人"/><rel type="ガ" mode="？" target="読者"/><rel type="ガ" mode="？" target="著者"/><rel type="ヲ" target="トス" sid="w201106-0000060050-1" id="1"/>
        行う おこなう 行う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
        )
    )
    for child_unit in sent.child_units:
        assert isinstance(child_unit, Phrase)


def test_document():
    sent = Sentence("コイントスを３回行う。")
    try:
        _ = sent.document
    except AttributeError:
        pass
    except Exception as e:
        raise e


def test_from_jumanpp_empty_line():
    _ = Sentence.from_jumanpp(
        textwrap.dedent(
            """\


        # S-ID:w201106-0000060050-1 JUMAN:6.1-20101108 KNP:3.1-20101107 DATE:2011/06/21 SCORE:-44.94406 MOD:2017/10/15 MEMO:
        コイン こいん コイン 名詞 6 普通名詞 1 * 0 * 0
        トス とす トス 名詞 6 サ変名詞 2 * 0 * 0
        を を を 助詞 9 格助詞 1 * 0 * 0
        ３ さん ３ 名詞 6 数詞 7 * 0 * 0
        回 かい 回 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0
        行う おこなう 行う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
        )
    )


def test_from_knp_empty_line():
    _ = Sentence.from_knp(
        textwrap.dedent(
            """\


        # S-ID:w201106-0000060050-1 JUMAN:6.1-20101108 KNP:3.1-20101107 DATE:2011/06/21 SCORE:-44.94406 MOD:2017/10/15 MEMO:
        * 2D
        + 1D
        コイン こいん コイン 名詞 6 普通名詞 1 * 0 * 0
        + 3D <rel type="ガ" target="不特定:人"/><rel type="ヲ" target="コイン" sid="w201106-0000060050-1" id="0"/>
        トス とす トス 名詞 6 サ変名詞 2 * 0 * 0
        を を を 助詞 9 格助詞 1 * 0 * 0
        * 2D
        + 3D
        ３ さん ３ 名詞 6 数詞 7 * 0 * 0
        回 かい 回 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0
        * -1D
        + -1D <rel type="ガ" target="不特定:人"/><rel type="ガ" mode="？" target="読者"/><rel type="ガ" mode="？" target="著者"/><rel type="ヲ" target="トス" sid="w201106-0000060050-1" id="1"/>
        行う おこなう 行う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
        。 。 。 特殊 1 句点 1 * 0 * 0
        EOS
        """
        )
    )


def test_from_knp_invalid_input():
    with pytest.raises(Exception):
        _ = Sentence.from_knp(
            textwrap.dedent(
                """\
                ;; Invalid input
                EOS
                """
            )
        )
