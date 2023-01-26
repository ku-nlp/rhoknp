import multiprocessing
import textwrap
from pathlib import Path
from typing import Dict

import pytest

from rhoknp import Document, Sentence

CASES = [
    {
        "raw_text": "天気がいいので散歩した。",
        "sentences": ["天気がいいので散歩した。"],
        "line_by_line_text": textwrap.dedent(
            """\
            # S-ID:1
            天気がいいので散歩した。
            """
        ),
        "jumanpp": textwrap.dedent(
            """\
            # S-ID:1
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
        "knp_with_no_clause_tag": textwrap.dedent(
            """\
            # S-ID:1
            * 1D
            + 1D
            天気 てんき 天気 名詞 6 普通名詞 1 * 0 * 0 "代表表記:天気/てんき カテゴリ:抽象物"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            * 2D
            + 2D
            いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
            ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL
            * -1D
            + -1D
            散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物"
            した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
    },
    {
        "raw_text": "風が吹いたら桶屋が儲かる。服屋も儲かる。",
        "sentences": ["風が吹いたら桶屋が儲かる。", "服屋も儲かる。"],
        "line_by_line_text": textwrap.dedent(
            """\
            # S-ID:1
            風が吹いたら桶屋が儲かる。
            # S-ID:2
            服屋も儲かる。
            """
        ),
        "jumanpp": textwrap.dedent(
            """\
            # S-ID:1
            風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
            桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
            屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            # S-ID:2
            服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipediaページ内一覧:ドラゴンボールの登場人物 読み不明 疑似代表表記 代表表記:服屋/服屋"
            も も も 助詞 9 副助詞 2 * 0 * 0 NIL
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
        "knp": textwrap.dedent(
            """\
            # S-ID:1
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
            # S-ID:2
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
        ),
        "knp_with_no_clause_tag": textwrap.dedent(
            """\
            # S-ID:1
            * 1D
            + 1D
            風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            * 3D
            + 4D
            吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
            * 3D
            + 3D
            桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
            + 4D
            屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            * -1D
            + -1D
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            # S-ID:2
            * 1D
            + 1D
            服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipediaページ内一覧:ドラゴンボールの登場人物 読み不明 疑似代表表記 代表表記:服屋/服屋"
            も も も 助詞 9 副助詞 2 * 0 * 0 NIL
            * -1D
            + -1D
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
    },
]


@pytest.mark.parametrize("case", CASES)
def test_from_raw_text(case: Dict[str, str]) -> None:
    _ = Document.from_raw_text(case["raw_text"])


@pytest.mark.parametrize("case", CASES)
def test_from_raw_text_parallel(case: Dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        _ = pool.map(Document.from_raw_text, [case["raw_text"]])


@pytest.mark.parametrize("case", CASES)
def test_from_sentences(case: Dict[str, str]) -> None:
    doc1 = Document.from_sentences(case["sentences"])
    # from_sentences() allows Sentence objects as input.
    doc2 = Document.from_sentences(list(map(Sentence.from_raw_text, case["sentences"])))
    assert doc1 == doc2
    doc1.doc_id = "1"
    doc3 = Document.from_sentences(Document.from_jumanpp(case["jumanpp"]).sentences)
    assert doc1 == doc3
    doc4 = Document.from_sentences(Document.from_knp(case["knp"]).sentences)
    assert doc1 == doc4


@pytest.mark.parametrize("case", CASES)
def test_from_sentences_parallel(case: Dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        doc1 = pool.map(Document.from_sentences, [case["sentences"]])
        # from_sentences() allows Sentence objects as input.
        doc2 = pool.map(Document.from_sentences, [list(map(Sentence.from_raw_text, case["sentences"]))])
        assert doc1 == doc2


@pytest.mark.parametrize("case", CASES)
def test_from_line_by_line_text(case: Dict[str, str]) -> None:
    _ = Document.from_line_by_line_text(case["line_by_line_text"])


@pytest.mark.parametrize("case", CASES)
def test_from_line_by_line_text_parallel(case: Dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        _ = pool.map(Document.from_line_by_line_text, [case["line_by_line_text"]])


@pytest.mark.parametrize("case", CASES)
def test_from_jumanpp(case: Dict[str, str]) -> None:
    _ = Document.from_jumanpp(case["jumanpp"])


@pytest.mark.parametrize("case", CASES)
def test_from_jumanpp_parallel(case: Dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        _ = pool.map(Document.from_jumanpp, [case["jumanpp"]])


def test_from_jumanpp_error():
    invalid_jumanpp_text = textwrap.dedent(
        """\
        # S-ID:1
        天気 てんき 天気 名詞 6 普通名詞 1 * 0 *
        が が が 助詞 9 格助詞 1 * 0 * 0 NIL
        いい いい いい 形容詞 3 * 0 イ形容詞イ段 19 基本形 2 "代表表記:良い/よい 反義:形容詞:悪い/わるい"
        ので ので のだ 助動詞 5 * 0 ナ形容詞 21 ダ列タ系連用テ形 12 NIL
        散歩 さんぽ 散歩 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:散歩/さんぽ ドメイン:レクリエーション カテゴリ:抽象物"
        した した する 動詞 2 * 0 サ変動詞 16 タ形 10 "代表表記:する/する 自他動詞:自:成る/なる 付属動詞候補（基本）"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
    )
    with pytest.raises(ValueError):
        _ = Document.from_jumanpp(invalid_jumanpp_text)


def test_from_jumanpp_control_character() -> None:
    jumanpp = textwrap.dedent(
        """\
        # S-ID:0-1
        * あすたりすく * 特殊 1 記号 5 * 0 * 0
        + ぷらす + 未定義語 15 その他 1 * 0 * 0
        @ あっと @ 未定義語 15 その他 1 * 0 * 0
        EOS いーおーえす EOS 未定義語 15 アルファベット 3 * 0 * 0
        \u0020 すぺーす \u0020 特殊 1 空白 6 * 0 * 0
        < < < 特殊 1 括弧始 3 * 0 * 0
        > > > 特殊 1 括弧終 4 * 0 * 0
        " " " 特殊 1 括弧終 4 * 0 * 0
        : : : 未定義語 15 その他 1 * 0 * 0
        ; ; ; 未定義語 15 その他 1 * 0 * 0
        # # # 未定義語 15 その他 1 * 0 * 0
        EOS
        # S-ID:0-2
        * あすたりすく * 特殊 1 記号 5 * 0 * 0
        + ぷらす + 未定義語 15 その他 1 * 0 * 0
        @ あっと @ 未定義語 15 その他 1 * 0 * 0
        EOS いーおーえす EOS 未定義語 15 アルファベット 3 * 0 * 0
        \u0020 すぺーす \u0020 特殊 1 空白 6 * 0 * 0
        < < < 特殊 1 括弧始 3 * 0 * 0
        > > > 特殊 1 括弧終 4 * 0 * 0
        " " " 特殊 1 括弧終 4 * 0 * 0
        : : : 未定義語 15 その他 1 * 0 * 0
        ; ; ; 未定義語 15 その他 1 * 0 * 0
        # # # 未定義語 15 その他 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_jumanpp(jumanpp)
    assert document.to_jumanpp() == jumanpp
    assert len(document.sentences) == 2


@pytest.mark.parametrize("case", CASES)
def test_from_knp_with_no_clause_tag(case: Dict[str, str]) -> None:
    _ = Document.from_knp(case["knp_with_no_clause_tag"])


@pytest.mark.parametrize("case", CASES)
def test_from_knp_with_no_clause_tag_parallel(case: Dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        _ = pool.map(Document.from_knp, [case["knp_with_no_clause_tag"]])


@pytest.mark.parametrize("case", CASES)
def test_from_knp(case: Dict[str, str]) -> None:
    _ = Document.from_knp(case["knp"])


@pytest.mark.parametrize("case", CASES)
def test_from_knp_parallel(case: Dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        _ = pool.map(Document.from_knp, [case["knp"]])


def test_from_knp_error():
    invalid_knp_text = textwrap.dedent(
        """\
        # S-ID:1
        * 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき>
        + 1D <BGH:天気/てんき><文頭><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:天気/てんき><主辞代表表記:天気/てんき><解析格:ガ>
        天気 てんき 天気 名詞 6 普通名詞 1 * 0 *
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
    )
    with pytest.raises(ValueError):
        _ = Document.from_knp(invalid_knp_text)


@pytest.mark.parametrize("case", CASES)
def test_need_senter(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.need_senter is True
    doc = Document.from_sentences(case["sentences"])
    assert doc.need_senter is False
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    assert doc.need_senter is False
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.need_senter is False
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.need_senter is False
    doc = Document.from_knp(case["knp"])
    assert doc.need_senter is False


@pytest.mark.parametrize("case", CASES)
def test_need_jumanpp(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.need_jumanpp is True
    doc = Document.from_sentences(case["sentences"])
    assert doc.need_jumanpp is True
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    assert doc.need_jumanpp is True
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.need_jumanpp is False
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.need_jumanpp is False
    doc = Document.from_knp(case["knp"])
    assert doc.need_jumanpp is False


@pytest.mark.parametrize("case", CASES)
def test_need_knp(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.need_knp is True
    doc = Document.from_sentences(case["sentences"])
    assert doc.need_knp is True
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    assert doc.need_knp is True
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.need_knp is True
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.need_knp is False
    doc = Document.from_knp(case["knp"])
    assert doc.need_knp is False


@pytest.mark.parametrize("case", CASES)
def test_need_clause_tag(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.need_clause_tag is True
    doc = Document.from_sentences(case["sentences"])
    assert doc.need_clause_tag is True
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    assert doc.need_clause_tag is True
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.need_clause_tag is True
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.need_clause_tag is True
    doc = Document.from_knp(case["knp"])
    assert doc.need_clause_tag is False


@pytest.mark.parametrize("case", CASES)
def test_text(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.text == case["raw_text"]
    doc = Document.from_sentences(case["sentences"])
    assert doc.text == case["raw_text"]
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    assert doc.text == case["raw_text"]
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.text == case["raw_text"]
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.text == case["raw_text"]
    doc = Document.from_knp(case["knp"])
    assert doc.text == case["raw_text"]


@pytest.mark.parametrize("case", CASES)
def test_to_raw_text(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.to_raw_text() == case["raw_text"] + "\n"
    doc = Document.from_sentences(case["sentences"])
    assert doc.to_raw_text() == "\n".join(case["sentences"]) + "\n"
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    assert doc.to_raw_text() == case["line_by_line_text"]
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.to_raw_text() == case["line_by_line_text"]
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.to_raw_text() == case["line_by_line_text"]
    doc = Document.from_knp(case["knp"])
    assert doc.to_raw_text() == case["line_by_line_text"]


@pytest.mark.parametrize("case", CASES)
def test_to_jumanpp(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        assert doc.to_jumanpp() == case["jumanpp"]
    doc = Document.from_sentences(case["sentences"])
    with pytest.raises(AttributeError):
        assert doc.to_jumanpp() == case["jumanpp"]
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    with pytest.raises(AttributeError):
        assert doc.to_jumanpp() == case["jumanpp"]
    doc = Document.from_jumanpp(case["jumanpp"])
    assert doc.to_jumanpp() == case["jumanpp"]
    # NOTE: may not match because KNP sometimes rewrites morpheme information
    # doc = Document.from_knp(case["knp_with_no_clause_tag"])
    # assert doc.to_jumanpp() == case["jumanpp"]
    # NOTE: does not match because KNP appends features to morphemes
    # doc = Document.from_knp(case["knp"])
    # assert doc.to_jumanpp() == case["jumanpp"]


@pytest.mark.parametrize("case", CASES)
def test_to_knp(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        assert doc.to_knp() == case["knp"]
    doc = Document.from_sentences(case["sentences"])
    with pytest.raises(AttributeError):
        assert doc.to_knp() == case["knp"]
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    with pytest.raises(AttributeError):
        assert doc.to_knp() == case["knp"]
    doc = Document.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        assert doc.to_knp() == case["knp"]
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    assert doc.to_knp() == case["knp_with_no_clause_tag"]
    doc = Document.from_knp(case["knp"])
    assert doc.to_knp() == case["knp"]


@pytest.mark.parametrize("case", CASES)
def test_parent_unit(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    assert doc.parent_unit is None


@pytest.mark.parametrize("case", CASES)
def test_sentences(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        _ = doc.sentences
    doc = Document.from_sentences(case["sentences"])
    _ = doc.sentences
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    _ = doc.sentences
    doc = Document.from_jumanpp(case["jumanpp"])
    _ = doc.sentences
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    _ = doc.sentences
    doc = Document.from_knp(case["knp"])
    _ = doc.sentences


@pytest.mark.parametrize("case", CASES)
def test_clauses(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        _ = doc.clauses
    doc = Document.from_sentences(case["sentences"])
    with pytest.raises(AttributeError):
        _ = doc.clauses
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    with pytest.raises(AttributeError):
        _ = doc.clauses
    doc = Document.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        _ = doc.clauses
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    with pytest.raises(AttributeError):
        _ = doc.clauses
    doc = Document.from_knp(case["knp"])
    _ = doc.clauses


@pytest.mark.parametrize("case", CASES)
def test_phrases(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        _ = doc.phrases
    doc = Document.from_sentences(case["sentences"])
    with pytest.raises(AttributeError):
        _ = doc.phrases
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    with pytest.raises(AttributeError):
        _ = doc.phrases
    doc = Document.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        _ = doc.phrases
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    _ = doc.phrases
    doc = Document.from_knp(case["knp"])
    _ = doc.phrases


@pytest.mark.parametrize("case", CASES)
def test_base_phrases(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        _ = doc.base_phrases
    doc = Document.from_sentences(case["sentences"])
    with pytest.raises(AttributeError):
        _ = doc.base_phrases
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    with pytest.raises(AttributeError):
        _ = doc.base_phrases
    doc = Document.from_jumanpp(case["jumanpp"])
    with pytest.raises(AttributeError):
        _ = doc.base_phrases
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    _ = doc.base_phrases
    doc = Document.from_knp(case["knp"])
    _ = doc.base_phrases


@pytest.mark.parametrize("case", CASES)
def test_morphemes(case: Dict[str, str]) -> None:
    doc = Document.from_raw_text(case["raw_text"])
    with pytest.raises(AttributeError):
        _ = doc.morphemes
    doc = Document.from_sentences(case["sentences"])
    with pytest.raises(AttributeError):
        _ = doc.morphemes
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    with pytest.raises(AttributeError):
        _ = doc.morphemes
    doc = Document.from_jumanpp(case["jumanpp"])
    _ = doc.morphemes
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    _ = doc.morphemes
    doc = Document.from_knp(case["knp"])
    _ = doc.morphemes


@pytest.mark.parametrize("case", CASES)
def test_reference(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])
    for sentence in doc.sentences:
        assert sentence.document == doc
        assert sentence == sentence
        for clause in sentence.clauses:
            assert clause.document == doc
            assert clause.sentence == sentence
            assert clause == clause
            for phrase in clause.phrases:
                assert phrase.document == doc
                assert phrase.sentence == sentence
                assert phrase.clause == clause
                for base_phrase in phrase.base_phrases:
                    assert base_phrase.document == doc
                    assert base_phrase.sentence == sentence
                    assert base_phrase.phrase == phrase
                    assert base_phrase == base_phrase
                    for morpheme in base_phrase.morphemes:
                        assert morpheme.document == doc
                        assert morpheme.sentence == sentence
                        assert morpheme.clause == clause
                        assert morpheme.phrase == phrase
                        assert morpheme.base_phrase == base_phrase
                        assert morpheme == morpheme
                for morpheme in phrase.morphemes:
                    assert morpheme.phrase == phrase
            for base_phrase in clause.base_phrases:
                assert base_phrase.clause == clause
            for morpheme in clause.morphemes:
                assert morpheme.clause == clause
        for phrase in sentence.phrases:
            assert phrase.sentence == sentence
        for base_phrase in sentence.base_phrases:
            assert base_phrase.sentence == sentence
        for morpheme in sentence.morphemes:
            assert morpheme.sentence == sentence
    for clause in doc.clauses:
        assert clause.document == doc
    for phrase in doc.phrases:
        assert phrase.document == doc
    for base_phrase in doc.base_phrases:
        assert base_phrase.document == doc
    for morpheme in doc.morphemes:
        assert morpheme.document == doc


@pytest.mark.parametrize(
    "knp",
    [
        Path("tests/data/w201106-0000060050.knp").read_text(),
        Path("tests/data/wiki00100176.knp").read_text(),
    ],
)
def test_reference_with_no_clause_tag(knp: str) -> None:
    document = Document.from_knp(knp)
    for sentence in document.sentences:
        assert sentence.document == document
        assert sentence == sentence
        for phrase in sentence.phrases:
            assert phrase.document == document
            assert phrase.sentence == sentence
            for base_phrase in phrase.base_phrases:
                assert base_phrase.document == document
                assert base_phrase.sentence == sentence
                assert base_phrase.phrase == phrase
                assert base_phrase == base_phrase
                for morpheme in base_phrase.morphemes:
                    assert morpheme.document == document
                    assert morpheme.sentence == sentence
                    assert morpheme.phrase == phrase
                    assert morpheme.base_phrase == base_phrase
                    assert morpheme == morpheme
            for morpheme in phrase.morphemes:
                assert morpheme.phrase == phrase
        for phrase in sentence.phrases:
            assert phrase.sentence == sentence
        for base_phrase in sentence.base_phrases:
            assert base_phrase.sentence == sentence
        for morpheme in sentence.morphemes:
            assert morpheme.sentence == sentence
    for phrase in document.phrases:
        assert phrase.document == document
    for base_phrase in document.base_phrases:
        assert base_phrase.document == document
    for morpheme in document.morphemes:
        assert morpheme.document == document


@pytest.mark.parametrize("case", CASES)
def test_global_index(case: Dict[str, str]) -> None:
    def _test_global_index(doc: Document, attr: str) -> None:
        next_index = 0
        for unit in getattr(doc, attr):
            assert unit.global_index == next_index
            next_index += 1

    doc = Document.from_sentences(case["sentences"])
    for attr in ("sentences",):
        _test_global_index(doc, attr)
    doc = Document.from_line_by_line_text(case["line_by_line_text"])
    for attr in ("sentences",):
        _test_global_index(doc, attr)
    doc = Document.from_jumanpp(case["jumanpp"])
    for attr in ("sentences", "morphemes"):
        _test_global_index(doc, attr)
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    for attr in ("sentences", "phrases", "base_phrases", "morphemes"):
        _test_global_index(doc, attr)
    doc = Document.from_knp(case["knp"])
    for attr in ("sentences", "clauses", "phrases", "base_phrases", "morphemes"):
        _test_global_index(doc, attr)


@pytest.mark.parametrize("case", CASES)
def test_global_span(case: Dict[str, str]) -> None:
    def _test_global_span(doc: Document) -> None:
        prev_end = 0
        for morpheme in doc.morphemes:
            start, end = morpheme.global_span
            assert prev_end == start
            prev_end = end

    doc = Document.from_jumanpp(case["jumanpp"])
    _test_global_span(doc)
    doc = Document.from_knp(case["knp_with_no_clause_tag"])
    _test_global_span(doc)
    doc = Document.from_knp(case["knp"])
    _test_global_span(doc)


@pytest.mark.parametrize("case", CASES)
def test_cut_paste(case: Dict[str, str]) -> None:
    doc = Document.from_knp(case["knp"])

    # Split a document into sub-documents with a single sentence
    sub_docs = list(map(Document.from_sentences, [[sent] for sent in doc.sentences]))
    for sub_doc in sub_docs:
        assert len(sub_doc.sentences) == 1
        assert sub_doc.need_knp is False

    # Merge the sub-documents into a new document
    new_doc = Document.from_sentences([sent for sub_doc in sub_docs for sent in sub_doc.sentences])
    assert len(new_doc.sentences) == len(doc.sentences)
    assert new_doc.need_knp is False


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize(
    "key",
    ("raw_text", "sentences", "line_by_line_text", "jumanpp", "knp_with_no_clause_tag", "knp"),
)
def test_reparse(case: Dict[str, str], key: str) -> None:
    if key == "raw_text":
        doc = Document.from_raw_text(case[key])
    elif key == "sentences":
        doc = Document.from_sentences(case[key])
    elif key == "line_by_line_text":
        doc = Document.from_line_by_line_text(case[key])
    elif key == "jumanpp":
        doc = Document.from_jumanpp(case[key])
    elif key in ("knp_with_no_clause_tag", "knp"):
        doc = Document.from_knp(case[key])
    else:
        raise KeyError
    assert doc == doc.reparse()


def test_to_knp_kwdlc() -> None:
    doc_id = "w201106-0000060050"
    knp = Path(f"tests/data/{doc_id}.knp").read_text()
    doc = Document.from_knp(knp)
    assert doc.to_knp() == knp


def test_to_knp_wac() -> None:
    doc_id = "wiki00100176"
    knp = Path(f"tests/data/{doc_id}.knp").read_text()
    doc = Document.from_knp(knp)
    assert doc.to_knp() == knp


@pytest.mark.parametrize("doc_id", ("w201106-0000060050", "wiki00100176"))
def test_id(doc_id) -> None:
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    assert doc.doc_id == doc_id
    assert doc.did == doc_id


def test_update_id() -> None:
    doc_id = "w201106-0000060050"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    doc.doc_id = "test_doc_id"
    assert doc.doc_id == "test_doc_id"
    doc.did = "test_did"
    assert doc.did == "test_did"


def test_unset_id() -> None:
    doc = Document.from_raw_text("天気がいいので散歩した。")
    with pytest.raises(AttributeError):
        _ = doc.doc_id
    with pytest.raises(AttributeError):
        _ = doc.did


def test_eq() -> None:
    doc = Document.from_raw_text("天気がいいので散歩した。")
    assert doc != "天気がいいので散歩した。"


def test_eq_knp() -> None:
    doc_id = "w201106-0000060050"
    knp = Path(f"tests/data/{doc_id}.knp").read_text()
    doc1 = Document.from_knp(knp)
    doc2 = Document.from_knp(knp)
    assert doc1 == doc2


def test_eq_raw_text() -> None:
    doc1 = Document.from_raw_text("天気がいいので散歩した。")
    doc2 = Document.from_raw_text("天気がいいので散歩した。")
    assert doc1 == doc2


def test_text_error() -> None:
    doc = Document()
    with pytest.raises(AttributeError):
        _ = doc.text
