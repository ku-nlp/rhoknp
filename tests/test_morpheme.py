from dataclasses import astuple, dataclass

import pytest

from rhoknp.units import Document


@dataclass
class MorphemeTestCase:
    jumanpp: str
    texts: list[str]


cases = [
    MorphemeTestCase(
        jumanpp="""外国 がいこく 外国 名詞 6 普通名詞 1 * 0 * 0 "代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"
人 じん 人 名詞 6 普通名詞 1 * 0 * 0 "代表表記:人/じん カテゴリ:人 漢字読み:音"
参政 さんせい 参政 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:参政/さんせい ドメイン:政治 カテゴリ:抽象物"
権 けん 権 名詞 6 普通名詞 1 * 0 * 0 "代表表記:権/けん カテゴリ:抽象物 漢字読み:音"
EOS""",
        texts=["外国", "人", "参政", "権"],
    )
]


@pytest.mark.parametrize("jumanpp,texts", [astuple(case) for case in cases])
def test_morpheme(jumanpp: str, texts: list[str]):
    document = Document.from_jumanpp(jumanpp)
    for i, morpheme in enumerate(document.morphemes):
        assert texts[i] == morpheme.text
