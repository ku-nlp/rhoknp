import multiprocessing
import pickle
import textwrap
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from rhoknp import Document

CASES: list[dict[str, str | list[str]]] = [
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
    {
        "raw_text": "風が吹いたら桶屋が儲かる。服屋も儲かる。",
        "sentences": ["風が吹いたら桶屋が儲かる。", "服屋も儲かる。"],
        "line_by_line_text": textwrap.dedent(
            """\
            # S-ID:1-1
            風が吹いたら桶屋が儲かる。
            # S-ID:2-1
            服屋も儲かる。
            """
        ),
        "jumanpp": textwrap.dedent(
            """\
            # S-ID:1-1
            風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト"
            桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他"
            屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓"
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            # S-ID:2-1
            服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipediaページ内一覧:ドラゴンボールの登場人物 読み不明 疑似代表表記 代表表記:服屋/服屋"
            も も も 助詞 9 副助詞 2 * 0 * 0 NIL
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける"
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL
            EOS
            """
        ),
        # Inconsistent document IDs
        "knp": textwrap.dedent(
            """\
            # S-ID:1-1
            * 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ>
            + 1D <BGH:風/かぜ><文頭><ガ><助詞><体言><一文字漢字><係:ガ格><区切:0-0><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:風/かぜ><主辞代表表記:風/かぜ><解析格:ガ>
            風 かぜ 風 名詞 6 普通名詞 1 * 0 * 0 "代表表記:風/かぜ カテゴリ:抽象物 漢字読み:訓" <代表表記:風/かぜ><カテゴリ:抽象物><漢字読み:訓><正規化代表表記:風/かぜ><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * 3D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく>
            + 4D <BGH:吹く/ふく><補文ト><用言:動><係:連用><レベル:B><区切:3-5><ID:〜たら><連用要素><連用節><動態述語><正規化代表表記:吹く/ふく><主辞代表表記:吹く/ふく><用言代表表記:吹く/ふく><節-区切><節-主辞><節-機能-条件><格関係0:ガ:風><格解析結果:吹く/ふく:動1:ガ/C/風/0/0/1-1;ニ/U/-/-/-/-;ト/U/-/-/-/-;デ/U/-/-/-/-;カラ/U/-/-/-/-;時間/U/-/-/-/-><標準用言代表表記:吹く/ふく><談話関係:1-1/4/条件;2-1/1/条件>
            吹いたら ふいたら 吹く 動詞 2 * 0 子音動詞カ行 2 タ系条件形 13 "代表表記:吹く/ふく 補文ト" <代表表記:吹く/ふく><補文ト><正規化代表表記:吹く/ふく><かな漢字><活用語><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            * 3D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><正規化代表表記:桶/おけ+屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や>
            + 3D <BGH:桶/おけ><文節内><係:文節内><体言><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:桶/おけ>
            桶 おけ 桶 名詞 6 普通名詞 1 * 0 * 0 "代表表記:桶/おけ ドメイン:家庭・暮らし カテゴリ:人工物-その他" <代表表記:桶/おけ><ドメイン:家庭・暮らし><カテゴリ:人工物-その他><正規化代表表記:桶/おけ><漢字><かな漢字><名詞相当語><自立><内容語><タグ単位始><文節始>
            + 4D <SM-主体><SM-人><BGH:屋/や><ガ><助詞><体言><係:ガ格><区切:0-0><格要素><連用要素><一文字漢字><名詞項候補><先行詞候補><正規化代表表記:屋/や><主辞代表表記:屋/や><主辞’代表表記:桶/おけ+屋/や><解析格:ガ>
            屋 や 屋 名詞 6 普通名詞 1 * 0 * 0 "代表表記:屋/や カテゴリ:場所-施設 漢字読み:訓" <代表表記:屋/や><カテゴリ:場所-施設><漢字読み:訓><正規化代表表記:屋/や><漢字><かな漢字><名詞相当語><自立><複合←><内容語><タグ単位始><文節主辞>
            が が が 助詞 9 格助詞 1 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
            + -1D <BGH:儲かる/もうかる><文末><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係3:ガ:屋><格解析結果:儲かる/もうかる:動2:ガ/C/屋/3/0/1-1><標準用言代表表記:儲かる/もうかる>
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            # S-ID:2-1
            * 1D <文頭><モ><助詞><体言><係:未格><並キ:名:&ST:2.5&&モ><区切:1-4><並列タイプ:AND><格要素><連用要素><正規化代表表記:服屋/服屋><主辞代表表記:服屋/服屋><並列類似度:-100.000>
            + 1D <文頭><モ><助詞><体言><係:未格><並キ:名:&ST:2.5&&モ><区切:1-4><並列タイプ:AND><格要素><連用要素><名詞項候補><先行詞候補><正規化代表表記:服屋/服屋><主辞代表表記:服屋/服屋><解析格:ガ>
            服屋 服屋 服屋 名詞 6 普通名詞 1 * 0 * 0 "自動獲得:Wikipedia Wikipediaページ内一覧:ドラゴンボールの登場人物 読み不明 疑似代表表記 代表表記:服屋/服屋" <自動獲得:Wikipedia><Wikipediaページ内一覧:ドラゴンボールの登場人物><読み不明><疑似代表表記><代表表記:服屋/服屋><正規化代表表記:服屋/服屋><漢字><かな漢字><名詞相当語><文頭><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            も も も 助詞 9 副助詞 2 * 0 * 0 NIL <かな漢字><ひらがな><付属>
            * -1D <BGH:儲かる/もうかる><文末><モ〜><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる>
            + -1D <BGH:儲かる/もうかる><文末><モ〜><句点><用言:動><レベル:C><区切:5-5><ID:（文末）><係:文末><提題受:30><主節><格要素><連用要素><動態述語><正規化代表表記:儲かる/もうかる><主辞代表表記:儲かる/もうかる><用言代表表記:儲かる/もうかる><節-区切><節-主辞><時制:非過去><主題格:一人称優位><格関係0:ガ:服屋><格解析結果:儲かる/もうかる:動11:ガ/N/服屋/0/0/2-1;ニ/U/-/-/-/-;デ/U/-/-/-/-><標準用言代表表記:儲かる/もうかる>
            儲かる もうかる 儲かる 動詞 2 * 0 子音動詞ラ行 10 基本形 2 "代表表記:儲かる/もうかる ドメイン:ビジネス 自他動詞:他:儲ける/もうける" <代表表記:儲かる/もうかる><ドメイン:ビジネス><自他動詞:他:儲ける/もうける><正規化代表表記:儲かる/もうかる><かな漢字><活用語><表現文末><自立><内容語><タグ単位始><文節始><文節主辞><用言表記先頭><用言表記末尾><用言意味表記末尾>
            。 。 。 特殊 1 句点 1 * 0 * 0 NIL <英記号><記号><文末><付属>
            EOS
            """
        ),
        "knp_with_no_clause_tag": textwrap.dedent(
            """\
            # S-ID:1-1
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
            # S-ID:2-1
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


BUILDERS: dict[str, Callable[[Any], Document]] = {
    "raw_text": Document.from_raw_text,
    "sentences": Document.from_sentences,
    "line_by_line_text": Document.from_line_by_line_text,
    "jumanpp": Document.from_jumanpp,
    "knp_with_no_clause_tag": Document.from_knp,
    "knp": Document.from_knp,
}

# (is_senter_required, is_jumanpp_required, is_knp_required, is_clause_tag_required)
REQUIRED_STEPS: dict[str, tuple[bool, bool, bool, bool]] = {
    "raw_text": (True, True, True, True),
    "sentences": (False, True, True, True),
    "line_by_line_text": (False, True, True, True),
    "jumanpp": (False, False, True, True),
    "knp_with_no_clause_tag": (False, False, False, True),
    "knp": (False, False, False, False),
}

ACCESSIBLE_UNITS: dict[str, tuple[str, ...]] = {
    "raw_text": (),
    "sentences": ("sentences",),
    "line_by_line_text": ("sentences",),
    "jumanpp": ("sentences", "morphemes"),
    "knp_with_no_clause_tag": ("sentences", "phrases", "base_phrases", "morphemes"),
    "knp": ("sentences", "clauses", "phrases", "base_phrases", "morphemes"),
}


@pytest.mark.parametrize("case", CASES)
def test_parallel(case: dict[str, str]) -> None:
    with multiprocessing.Pool(processes=1) as pool:
        docs = [pool.apply(build, (case[key],)) for key, build in BUILDERS.items()]
    for doc in docs:
        assert doc.text == case["raw_text"]


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("key", ["line_by_line_text", "jumanpp", "knp"])
def test_from_sentences(case: dict[str, str], key: str) -> None:
    # from_sentences() also accepts Sentence objects and keeps their analysis results.
    doc = BUILDERS[key](case[key])
    new_doc = Document.from_sentences(doc.sentences)
    assert new_doc.text == doc.text
    assert len(new_doc.sentences) == len(doc.sentences)
    assert new_doc.is_jumanpp_required() is doc.is_jumanpp_required()
    assert new_doc.is_knp_required() is doc.is_knp_required()


@pytest.mark.parametrize("case", CASES)
def test_from_jumanpp_without_last_eos(case: dict[str, str]) -> None:
    jumanpp_lines = case["jumanpp"].rstrip().split("\n")
    assert jumanpp_lines[-1] == "EOS"
    doc = Document.from_jumanpp("\n".join(jumanpp_lines[:-1]) + "\n")
    assert doc.text == case["raw_text"]


def test_from_jumanpp_error() -> None:
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
    with pytest.raises(ValueError, match=r"malformed line: .*"):
        _ = Document.from_jumanpp(invalid_jumanpp_text)


def test_from_jumanpp_control_character() -> None:
    jumanpp = textwrap.dedent(
        """\
        # S-ID:0-1
        * あすたりすく * 特殊 1 記号 5 * 0 * 0
        + ぷらす + 未定義語 15 その他 1 * 0 * 0
        @ あっと @ 未定義語 15 その他 1 * 0 * 0
        EOS いーおーえす EOS 未定義語 15 アルファベット 3 * 0 * 0
        \\␣ すぺーす \\␣ 特殊 1 空白 6 * 0 * 0
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
        \\␣ すぺーす \\␣ 特殊 1 空白 6 * 0 * 0
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
def test_from_knp_without_last_eos(case: dict[str, str]) -> None:
    knp_lines = case["knp"].rstrip().split("\n")
    assert knp_lines[-1] == "EOS"
    doc = Document.from_knp("\n".join(knp_lines[:-1]) + "\n")
    assert doc.text == case["raw_text"]


def test_from_knp_error() -> None:
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
    with pytest.raises(ValueError, match=r"malformed line: .*"):
        _ = Document.from_knp(invalid_knp_text)


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("key", BUILDERS)
def test_required_steps(case: dict[str, str], key: str) -> None:
    doc = BUILDERS[key](case[key])
    assert (
        doc.is_senter_required(),
        doc.is_jumanpp_required(),
        doc.is_knp_required(),
        doc.is_clause_tag_required(),
    ) == REQUIRED_STEPS[key]


@pytest.mark.parametrize("case", CASES)
def test_text(case: dict[str, str]) -> None:
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


def test_text_error() -> None:
    doc = Document()
    with pytest.raises(AttributeError):
        _ = doc.text


@pytest.mark.parametrize("case", CASES)
def test_to_raw_text(case: dict[str, str]) -> None:
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
def test_to_jumanpp(case: dict[str, str]) -> None:
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
def test_to_knp(case: dict[str, str]) -> None:
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


def test_parent_unit() -> None:
    doc = Document.from_raw_text("天気がいいので散歩した。")
    assert doc.parent_unit is None


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("key", BUILDERS)
def test_unit_access(case: dict[str, str], key: str) -> None:
    doc = BUILDERS[key](case[key])
    for attr in ("sentences", "clauses", "phrases", "base_phrases", "morphemes"):
        if attr in ACCESSIBLE_UNITS[key]:
            assert len(getattr(doc, attr)) > 0
        else:
            with pytest.raises(AttributeError):
                _ = getattr(doc, attr)


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("key", ["jumanpp", "knp_with_no_clause_tag", "knp"])
def test_reference(case: dict[str, str], key: str) -> None:
    document = BUILDERS[key](case[key])
    for sentence in document.sentences:
        assert sentence.document == document
        for morpheme in sentence.morphemes:
            assert morpheme.document == document
            assert morpheme.sentence == sentence
        if sentence.is_knp_required():
            continue
        for phrase in sentence.phrases:
            assert phrase.document == document
            assert phrase.sentence == sentence
            for base_phrase in phrase.base_phrases:
                assert base_phrase.document == document
                assert base_phrase.sentence == sentence
                assert base_phrase.phrase == phrase
                for morpheme in base_phrase.morphemes:
                    assert morpheme.document == document
                    assert morpheme.sentence == sentence
                    assert morpheme.phrase == phrase
                    assert morpheme.base_phrase == base_phrase
            for morpheme in phrase.morphemes:
                assert morpheme.phrase == phrase
        for base_phrase in sentence.base_phrases:
            assert base_phrase.sentence == sentence
        if sentence.is_clause_tag_required():
            continue
        for clause in sentence.clauses:
            assert clause.document == document
            assert clause.sentence == sentence
            for phrase in clause.phrases:
                assert phrase.clause == clause
            for base_phrase in clause.base_phrases:
                assert base_phrase.clause == clause
            for morpheme in clause.morphemes:
                assert morpheme.clause == clause


@pytest.mark.parametrize("case", CASES)
def test_global_index(case: dict[str, str]) -> None:
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
def test_global_span(case: dict[str, str]) -> None:
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
@pytest.mark.parametrize("key", BUILDERS)
def test_reparse(case: dict[str, str], key: str) -> None:
    doc = BUILDERS[key](case[key])
    assert doc == doc.reparse()


def test_pas_list() -> None:
    doc_id = "w201106-0000060050"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text(encoding="utf-8"))
    assert len(doc.pas_list) == 12


@pytest.mark.parametrize("path", sorted(Path("tests/data").glob("*.knp")), ids=lambda path: path.stem)
def test_annotated_corpora(path: Path) -> None:
    knp = path.read_text(encoding="utf-8")
    doc = Document.from_knp(knp)
    assert doc.to_knp() == knp
    assert doc.doc_id == doc.did == path.stem
    assert pickle.loads(pickle.dumps(doc)).to_knp() == knp  # nosec pickle


def test_update_id() -> None:
    doc_id = "w201106-0000060050"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text(encoding="utf-8"))
    doc.doc_id = "test_doc_id"
    assert doc.doc_id == "test_doc_id"
    assert doc.did == "test_doc_id"
    doc.did = "test_did"
    assert doc.doc_id == "test_did"
    assert doc.did == "test_did"


def test_eq() -> None:
    doc0 = Document.from_raw_text("天気がいいので散歩した。")
    assert doc0 != "天気がいいので散歩した。"
    doc1 = Document.from_raw_text("天気がいいので散歩した。")
    assert doc0 == doc1
    assert hash(doc0) == hash(doc1)
    doc1.doc_id = "1"
    doc2 = Document.from_raw_text("天気がいいので散歩した。")
    doc2.doc_id = "2"
    assert doc0 != doc1
    assert hash(doc0) != hash(doc1)
    assert doc1 != doc2
    assert hash(doc1) != hash(doc2)


@pytest.mark.parametrize("case", CASES)
def test_pickle_unpickle(case: dict[str, str]) -> None:
    doc1 = Document.from_knp(case["knp"])
    doc2 = pickle.loads(pickle.dumps(doc1))  # nosec pickle
    assert doc1.to_knp() == doc2.to_knp()
