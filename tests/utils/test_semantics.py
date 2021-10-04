import pytest

from rhoknp.units.utils import Semantics


@pytest.mark.parametrize("sstring", ['"代表表記:天気/てんき カテゴリ:抽象物"', "NIL"])
def test_features_from_fstring(sstring: str):
    semantics = Semantics.from_sstring(sstring)
    assert semantics.to_sstring() == sstring
