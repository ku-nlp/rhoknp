import io
import textwrap

from rhoknp.cli.show import draw_tree
from rhoknp.units import Sentence

knp = textwrap.dedent(
    """\
    # S-ID:000-0-0 kwja:1.2.2
    * 3D
    + 1D <体言>
    望遠 ぼうえん 望遠 名詞 6 普通名詞 1 * 0 * 0 "代表表記:望遠/ぼうえん カテゴリ:抽象物" <基本句-主辞>
    + 4D <体言>
    鏡 きょう 鏡 名詞 6 普通名詞 1 * 0 * 0 "代表表記:鏡/きょう 漢字読み:音 カテゴリ:人工物-その他" <基本句-主辞>
    で で で 助詞 9 格助詞 1 * 0 * 0 "代表表記:で/で"
    * 2D
    + 3D <rel type="ガ" target="少女" sid="202212172122-0-0" id="3"/><用言:動><時制:非過去><レベル:B><動態述語><節-区切:連体修飾><節-主辞>
    泳いで およいで 泳ぐ 動詞 2 * 0 子音動詞ガ行 4 タ系連用テ形 14 "代表表記:泳ぐ/およぐ" <基本句-主辞><用言表記先頭>
    いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 "代表表記:いる/いる" <用言表記末尾>
    * 3D
    + 4D <体言><SM-主体>
    少女 しょうじょ 少女 名詞 6 普通名詞 1 * 0 * 0 "代表表記:少女/しょうじょ カテゴリ:人" <基本句-主辞>
    を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
    * -1D
    + -1D <rel type="ガ" target="著者"/><rel type="ヲ" target="少女" sid="202212172122-0-0" id="3"/><用言:動><時制:過去><レベル:C><動態述語><節-区切><節-主辞>
    見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 補文ト 自他動詞:自:見える/みえる" <基本句-主辞><用言表記先頭><用言表記末尾>
    。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
    EOS
    """
)
sentence = Sentence.from_knp(knp)


def test_draw_phrase_tree() -> None:
    out = textwrap.dedent(
        """\
        望遠n鏡nでp─────┐
         泳いでvいるs─┐ │
               少女nをp─┤
                 見たv。*
        """
    )
    with io.StringIO() as f:
        draw_tree(sentence.phrases, f, show_pos=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]


def test_draw_base_phrase_tree() -> None:
    out = textwrap.dedent(
        """\
           望遠n─┐
            鏡nでp─────┐
        泳いでvいるs─┐ │  ガ:少女
              少女nをp─┤
                見たv。*  ガ:著者 ヲ:少女
        """
    )
    with io.StringIO() as f:
        draw_tree(sentence.base_phrases, f, show_pos=True, show_rel=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]
