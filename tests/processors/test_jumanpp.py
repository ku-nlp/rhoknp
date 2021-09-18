import pytest

from rhoknp.processors import Jumanpp
from rhoknp.units import Document


@pytest.mark.parametrize("text", ["外国人参政権", "望遠鏡で泳いでいる少女を見た。"])
def test_jumanpp_apply(text: str):
    jumanpp = Jumanpp()
    document = jumanpp.apply(Document.from_sentence(text))
    assert document.text == text
