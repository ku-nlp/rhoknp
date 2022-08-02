import pytest

from rhoknp.props import SemanticsDict


@pytest.mark.parametrize("sstring", ['"代表表記:天気/てんき カテゴリ:抽象物"', "NIL"])
def test_from_fstring(sstring: str) -> None:
    semantics = SemanticsDict.from_sstring(sstring)
    assert semantics.to_sstring() == sstring


def test_false():
    assert SemanticsDict._item2sem_string("sem", False) == ""


def test_empty_dict():
    semantics = SemanticsDict()
    assert semantics.to_sstring() == ""


def test_void():
    semantics = SemanticsDict()
    assert semantics.to_sstring() == ""


def test_empty_string():
    semantics = SemanticsDict.from_sstring("")
    assert semantics.to_sstring() == ""
