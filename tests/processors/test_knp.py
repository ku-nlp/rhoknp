import pytest

from rhoknp.processors import KNP, Jumanpp
from rhoknp.units import Document


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        # "これは\rどう",  # carriage return  # TODO
    ],
)
def test_knp_apply(text: str):
    jumanpp = Jumanpp()
    knp = KNP()
    document = knp.apply(jumanpp.apply(Document.from_sentence(text)))
    assert document.text == text.replace(" ", "　").replace('"', "”")
