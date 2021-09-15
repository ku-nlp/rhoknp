import pytest

from rhoknp.processors import Jumanpp
from rhoknp.units import Document


@pytest.mark.parametrize("text", ["外国人参政権", "望遠鏡で泳いでいる少女を見た。"])
def test_jumanpp_apply(text: str):
    jumanpp = Jumanpp()
    document = jumanpp.apply(Document.from_sentence(text))
    assert document.text == text


@pytest.mark.parametrize(
    "jumanpp",
    [
        """外国 がいこく 外国 名詞 6 普通名詞 1 * 0 * 0 "代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"
人 じん 人 名詞 6 普通名詞 1 * 0 * 0 "代表表記:人/じん カテゴリ:人 漢字読み:音"
参政 さんせい 参政 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:参政/さんせい ドメイン:政治 カテゴリ:抽象物"
権 けん 権 名詞 6 普通名詞 1 * 0 * 0 "代表表記:権/けん カテゴリ:抽象物 漢字読み:音"
EOS""",
        """望遠 ぼうえん 望遠 名詞 6 普通名詞 1 * 0 * 0 "代表表記:望遠/ぼうえん カテゴリ:抽象物"
鏡 きょう 鏡 名詞 6 普通名詞 1 * 0 * 0 "代表表記:鏡/きょう カテゴリ:人工物-その他 漢字読み:音"
で で で 助詞 9 格助詞 1 * 0 * 0 NIL
泳いで およいで 泳ぐ 動詞 2 * 0 子音動詞ガ行 4 タ系連用テ形 14 "代表表記:泳ぐ/およぐ"
いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 "代表表記:いる/いる"
少女 しょうじょ 少女 名詞 6 普通名詞 1 * 0 * 0 "代表表記:少女/しょうじょ カテゴリ:人"
を を を 助詞 9 格助詞 1 * 0 * 0 NIL
見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 自他動詞:自:見える/みえる 補文ト"
。 。 。 特殊 1 句点 1 * 0 * 0 NIL
EOS""",
    ],
)
def test_jumanpp_load(jumanpp: str):
    doc = Document.from_jumanpp(jumanpp)
    assert jumanpp == doc.to_jumanpp()
