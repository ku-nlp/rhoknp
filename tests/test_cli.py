import tempfile
import textwrap

from typer.testing import CliRunner

from rhoknp import Document, __version__
from rhoknp.cli import app

runner = CliRunner()


knp = textwrap.dedent(
    """\
        # S-ID:1
        * 1D
        + 1D
        望遠 ぼうえん 望遠 名詞 6 普通名詞 1 * 0 * 0 "代表表記:望遠/ぼうえん カテゴリ:抽象物"
        + 2D
        鏡 きょう 鏡 名詞 6 普通名詞 1 * 0 * 0 "代表表記:鏡/きょう カテゴリ:人工物-その他 漢字読み:音"
        で で で 助詞 9 格助詞 1 * 0 * 0 NIL
        * 2D
        + 3D
        泳いで およいで 泳ぐ 動詞 2 * 0 子音動詞ガ行 4 タ系連用テ形 14 "代表表記:泳ぐ/およぐ"
        いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 "代表表記:いる/いる"
        * 3D
        + 4D
        少女 しょうじょ 少女 名詞 6 普通名詞 1 * 0 * 0 "代表表記:少女/しょうじょ カテゴリ:人"
        を を を 助詞 9 格助詞 1 * 0 * 0 NIL
        * -1D
        + -1D <節-区切><節-主辞>
        見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 自他動詞:自:見える/みえる 補文ト"
        。 。 。 特殊 1 句点 1 * 0 * 0 NIL
        EOS
        """
)


def test_version():
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert result.stdout.strip() == f"rhoknp version: {__version__}"


def test_show():
    doc = Document.from_knp(knp)
    with tempfile.NamedTemporaryFile("wt") as f:
        f.write(doc.to_knp())
        f.flush()
        result = runner.invoke(app, ["show", f.name])
        assert result.exit_code == 0


def test_show_error():
    result = runner.invoke(app, ["show", "foo.knp"])  # not exist
    assert result.exit_code == 2


def test_stats():
    doc = Document.from_knp(knp)
    with tempfile.NamedTemporaryFile("wt") as f:
        f.write(doc.to_knp())
        f.flush()
        result = runner.invoke(app, ["stats", f.name])
        assert result.exit_code == 0


def test_stats_json():
    doc = Document.from_knp(knp)
    with tempfile.NamedTemporaryFile("wt") as f:
        f.write(doc.to_knp())
        f.flush()
        result = runner.invoke(app, ["stats", f.name, "--json"])
        assert result.exit_code == 0


def test_stats_error():
    result = runner.invoke(app, ["stats", "foo.knp"])  # not exist
    assert result.exit_code == 2