from subprocess import PIPE, Popen

import pytest

# from rhoknp import parse, load_jumanpp

JMN = ["jumanpp"]


@pytest.mark.parametrize("text", ["外国人参政権"])
def test_jumanpp_parse(text: str):
    with Popen(JMN, stdout=PIPE, stdin=PIPE, encoding="utf-8") as p:
        out, _ = p.communicate(input=text)
    # doc = parse(text)
    # assert out == doc.to_jumanpp()


@pytest.mark.parametrize(
    "analysis",
    [
        """外国 がいこく 外国 名詞 6 普通名詞 1 * 0 * 0 "代表表記:外国/がいこく ドメイン:政治 カテゴリ:場所-その他"
人 じん 人 名詞 6 普通名詞 1 * 0 * 0 "代表表記:人/じん カテゴリ:人 漢字読み:音"
参政 さんせい 参政 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:参政/さんせい ドメイン:政治 カテゴリ:抽象物"
権 けん 権 名詞 6 普通名詞 1 * 0 * 0 "代表表記:権/けん カテゴリ:抽象物 漢字読み:音"
EOS"""
    ],
)
def test_jumanpp_load(analysis: str):
    pass
    # doc = load_jumanpp(analysis)
    # assert analysis == doc.to_jumanpp()
