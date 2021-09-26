import pytest

from rhoknp.processors import Jumanpp
from rhoknp.units import Document

cases = [
    "外国人参政権",
    "望遠鏡で泳いでいる少女を見た。",
    "エネルギーを素敵にENEOS",  # EOS
    "Canon EOS 80D買った",  # EOS
    '"最高"の気分',  # double quotes
    "&lt;tag&gt;\\エス'ケープ",  # escape
    # "これは\rどう",  # carriage return  # TODO
]


@pytest.mark.parametrize("text", cases)
def test_jumanpp_apply(text: str):
    jumanpp = Jumanpp()
    document = jumanpp.apply(Document.from_sentence(text))
    assert document.text == text.replace(" ", "　").replace('"', "”")


def test_jumanpp_normal():
    jumanpp = Jumanpp()
    text = "この文を解析してください。"
    document = jumanpp.apply(Document.from_sentence(text))
    assert len(document.morphemes) == 7
    assert "".join(m.text for m in document.morphemes) == text


def test_jumanpp_nominalization():
    jumanpp = Jumanpp()
    text = "音の響きを感じる。"
    document = jumanpp.apply(Document.from_sentence(text))
    assert len(document.morphemes) == 6
    assert "".join(m.text for m in document.morphemes) == text
    assert document.morphemes[2].surf == "響き"
    assert document.morphemes[2].pos == "名詞"


def test_jumanpp_whitespace():
    jumanpp = Jumanpp()
    text = "半角 スペース"
    document = jumanpp.apply(Document.from_sentence(text))
    assert len(document.morphemes) == 3
    assert "".join(m.text for m in document.morphemes) == text.replace(" ", "　")
    assert document.morphemes[1].pos == "特殊"
    assert document.morphemes[1].subpos == "空白"
