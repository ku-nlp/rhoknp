from dataclasses import astuple, dataclass

import pytest

from rhoknp.units import Morpheme


@dataclass
class MorphemeTestCase:
    jumanpp: str
    text: str


cases = [
    MorphemeTestCase(
        jumanpp='外国 がいこく 外国 名詞 6 普通名詞 1 * 0 * 0 "代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"',
        text="外国",
    ),
    MorphemeTestCase(
        jumanpp='人 じん 人 名詞 6 普通名詞 1 * 0 * 0 "代表表記:人/じん カテゴリ:人 漢字読み:音"',
        text="人",
    ),
    MorphemeTestCase(
        jumanpp='参政 さんせい 参政 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:参政/さんせい ドメイン:政治 カテゴリ:抽象物"',
        text="参政",
    ),
    MorphemeTestCase(
        jumanpp='権 けん 権 名詞 6 普通名詞 1 * 0 * 0 "代表表記:権/けん カテゴリ:抽象物 漢字読み:音"',
        text="権",
    ),
]


@pytest.mark.parametrize("jumanpp,text", [astuple(case) for case in cases])
def test_morpheme_from_jumanpp(jumanpp: str, text: str):
    morpheme = Morpheme.from_jumanpp(jumanpp)
    assert morpheme.text == text


@pytest.mark.parametrize("jumanpp,texts", [astuple(case) for case in cases])
def test_morpheme_to_jumanpp(jumanpp: str, texts: list[str]):
    morpheme = Morpheme.from_jumanpp(jumanpp)
    assert morpheme.to_jumanpp() == jumanpp


def test_morpheme_semantics():
    jumanpp = '解析 かいせき 解析 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:解析/かいせき カテゴリ:抽象物 ドメイン:教育・学習;科学・技術"'
    morpheme = Morpheme.from_jumanpp(jumanpp)
    assert morpheme.semantics == "代表表記:解析/かいせき カテゴリ:抽象物 ドメイン:教育・学習;科学・技術"


def test_morpheme_semantics_nil():
    jumanpp = "であり であり だ 判定詞 4 * 0 判定詞 25 デアル列基本連用形 18 NIL"
    morpheme = Morpheme.from_jumanpp(jumanpp)
    assert morpheme.semantics == "NIL"


def test_morpheme_at():
    jumanpp = "@ @ @ 未定義語 15 その他 1 * 0 * 0"
    morpheme = Morpheme.from_jumanpp(jumanpp)
    assert morpheme.text == "@"
