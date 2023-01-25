import io
import textwrap

from rhoknp.cli.show import draw_tree
from rhoknp.units import Sentence

sentence1 = Sentence.from_knp(
    textwrap.dedent(
        """\
        # S-ID:000-0-0
        * 3D
        + 1D <体言>
        望遠 ぼうえん 望遠 名詞 6 普通名詞 1 * 0 * 0 "代表表記:望遠/ぼうえん カテゴリ:抽象物" <基本句-主辞>
        + 4D <体言>
        鏡 きょう 鏡 名詞 6 普通名詞 1 * 0 * 0 "代表表記:鏡/きょう 漢字読み:音 カテゴリ:人工物-その他" <基本句-主辞>
        で で で 助詞 9 格助詞 1 * 0 * 0 "代表表記:で/で"
        * 2D
        + 3D <rel type="ガ" target="少女" sid="000-0-0" id="3"/><用言:動><時制:非過去><レベル:B><動態述語><節-区切:連体修飾><節-主辞>
        泳いで およいで 泳ぐ 動詞 2 * 0 子音動詞ガ行 4 タ系連用テ形 14 "代表表記:泳ぐ/およぐ" <基本句-主辞><用言表記先頭>
        いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 "代表表記:いる/いる" <用言表記末尾>
        * 3D
        + 4D <体言><SM-主体>
        少女 しょうじょ 少女 名詞 6 普通名詞 1 * 0 * 0 "代表表記:少女/しょうじょ カテゴリ:人" <基本句-主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
        * -1D
        + -1D <rel type="ガ" target="著者"/><rel type="ヲ" target="少女" sid="000-0-0" id="3"/><用言:動><時制:過去><レベル:C><動態述語><節-区切><節-主辞>
        見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 補文ト 自他動詞:自:見える/みえる" <基本句-主辞><用言表記先頭><用言表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
)

sentence2 = Sentence.from_knp(
    textwrap.dedent(
        """\
        # S-ID:001-0-0
        * 1D
        + 1D <体言>
        クロール くろーる クロール 名詞 6 普通名詞 1 * 0 * 0 "代表表記:クロール/くろーる カテゴリ:抽象物 ドメイン:スポーツ" <基本句-主辞>
        で で で 助詞 9 格助詞 1 * 0 * 0 "代表表記:で/で"
        * 3D
        + 3D <rel type="ガ" target="次郎" sid="001-0-0" id="3"/><用言:動><時制:非過去><レベル:B><動態述語><節-区切:連体修飾><節-主辞>
        泳いで およいで 泳ぐ 動詞 2 * 0 子音動詞ガ行 4 タ系連用テ形 14 "代表表記:泳ぐ/およぐ" <基本句-主辞><用言表記先頭>
        いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 "代表表記:いる/いる" <用言表記末尾>
        * 3P
        + 3P <体言><SM-主体><NE:PERSON:太郎>
        太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0 "代表表記:太郎/たろう 人名:日本:名:45:0.00106" <基本句-主辞>
        と と と 助詞 9 格助詞 1 * 0 * 0 "代表表記:と/と"
        * 4D
        + 4D <体言><SM-主体><NE:PERSON:次郎>
        次郎 じろう 次郎 名詞 6 人名 5 * 0 * 0 "代表表記:次郎/じろう 人名:日本:名:135:0.00068" <基本句-主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
        * -1D
        + -1D <rel type="ガ" target="著者"/><rel type="ヲ" target="次郎" sid="001-0-0" id="3"/><用言:動><時制:過去><レベル:C><動態述語><節-区切><節-主辞>
        見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 補文ト 自他動詞:自:見える/みえる" <基本句-主辞><用言表記先頭><用言表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
)

sentence3 = Sentence.from_knp(
    textwrap.dedent(
        """\
        # S-ID:002-0-0
        * 3P
        + 3P <体言><SM-主体><NE:PERSON:太郎>
        太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0 <基本句-主辞>
        と と と 助詞 9 格助詞 1 * 0 * 0 "代表表記:と/と"
        * 2D
        + 2D <rel type="ガ" target="服" sid="002-0-0" id="2"/><用言:形><時制:非過去><レベル:B-><状態述語>
        白い しろい 白い 形容詞 3 * 0 イ形容詞アウオ段 18 基本形 2 "代表表記:白い/しろい 名詞派生:白/しろ" <基本句-主辞><用言表記先頭><用言表記末尾>
        * 3D
        + 3D <体言><係:ノ格>
        服 ふく 服 名詞 6 普通名詞 1 * 0 * 0 "代表表記:服/ふく 漢字読み:音 カテゴリ:人工物-衣類 ドメイン:家庭・暮らし" <基本句-主辞>
        の の の 助詞 9 接続助詞 3 * 0 * 0 "代表表記:の/の"
        * 4D
        + 4D <体言><SM-主体>
        花子 はなこ 花子 名詞 6 人名 5 * 0 * 0 "代表表記:花子/はなこ 人名:日本:名:912:0.00019" <基本句-主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
        * -1D
        + -1D <rel type="ガ" target="著者"/><rel type="ヲ" target="花子" sid="002-0-0" id="3"/><用言:動><時制:過去><レベル:C><動態述語><節-区切><節-主辞>
        見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 補文ト 自他動詞:自:見える/みえる" <基本句-主辞><用言表記先頭><用言表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
)

sentence4 = Sentence.from_knp(
    textwrap.dedent(
        """\
        # S-ID:003-0-0
        * 2P
        + 2P <体言>
        ウナギ うなぎ ウナギ 名詞 6 普通名詞 1 * 0 * 0 "代表表記:鰻/うなぎ カテゴリ:動物;人工物-食べ物 ドメイン:料理・食事" <基本句-主辞>
        と と と 助詞 9 格助詞 1 * 0 * 0 "代表表記:と/と"
        、 、 、 特殊 1 読点 2 * 0 * 0 "代表表記:、/、"
        * 4D
        + 4D <体言><節-機能疑-目的><NE:LOCATION:浜松>
        浜松 はままつ 浜松 名詞 6 地名 4 * 0 * 0 "代表表記:浜松/はままつ 地名:日本:静岡県:市" <基本句-主辞>
        に に に 助詞 9 格助詞 1 * 0 * 0 "代表表記:に/に"
        * 3D
        + 3D <体言>
        鱧 つぼみ 鱧 名詞 6 普通名詞 1 * 0 * 0 <基本句-主辞>
        を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
        * 4D
        + 4D <rel type="ガ" target="著者"/><rel type="ヲ" target="鱧" sid="003-0-0" id="2"/><用言:動><レベル:A><動態述語><節-機能疑-目的>
        食べ たべ 食べる 動詞 2 * 0 母音動詞 1 基本連用形 8 "代表表記:食べる/たべる ドメイン:料理・食事" <基本句-主辞><用言表記先頭><用言表記末尾><ALT-食べ-たべ-食べる-2-0-1-8-"代表表記:食べる/たべる ドメイン:料理・食事">
        に に に 助詞 9 格助詞 1 * 0 * 0 "代表表記:に/に"
        * -1D
        + -1D <rel type="ガ" target="著者"/><rel type="ニ" target="浜松" sid="003-0-0" id="1"/><用言:動><時制:非過去><レベル:C><動態述語><節-区切><節-主辞>
        行く いく 行く 動詞 2 * 0 子音動詞カ行促音便形 3 基本形 2 "代表表記:行く/いく 付属動詞候補（タ系） ドメイン:交通 反義:動詞:帰る/かえる" <基本句-主辞><用言表記先頭><用言表記末尾>
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
)


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
        draw_tree(sentence1.phrases, f, show_pos=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]


def test_draw_base_phrase_tree_1() -> None:
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
        draw_tree(sentence1.base_phrases, f, show_pos=True, show_rel=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]


def test_draw_base_phrase_tree_2() -> None:
    out = textwrap.dedent(
        """\
        クロールnでp─┐
          泳いでvいるs───┐    ガ:次郎
                太郎Jとp━P
                  次郎Jをp─┐
                    見たv。*  ガ:著者 ヲ:次郎
        """
    )
    with io.StringIO() as f:
        draw_tree(sentence2.base_phrases, f, show_pos=True, show_rel=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]


def test_draw_base_phrase_tree_3() -> None:
    out = textwrap.dedent(
        """\
        太郎Jとp━━━━━P
             白いj─┐ ┃    ガ:服
              服nのp─┨
              花子Jをp─┐
                見たv。*  ガ:著者 ヲ:花子
        """
    )
    with io.StringIO() as f:
        draw_tree(sentence3.base_phrases, f, show_pos=True, show_rel=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]


def test_draw_base_phrase_tree_4() -> None:
    out = textwrap.dedent(
        """\
        ウナギnとp、*━━━P
               浜松Cにp─╂───┐
                   鱧nをp─┐ │
                   食べvにp─┤  ガ:著者 ヲ:鱧
                     行くv。*  ガ:著者 ニ:浜松
        """
    )
    with io.StringIO() as f:
        draw_tree(sentence4.base_phrases, f, show_pos=True, show_rel=True)
        assert [line.rstrip() for line in f.getvalue().splitlines()] == [line.rstrip() for line in out.splitlines()]
