from typing import Any, Dict

import pytest

from rhoknp.props import SemanticsDict

CASES = [
    {
        "sstring": '"代表表記:天気/てんき カテゴリ:抽象物"',
        "dict_": {"代表表記": "天気/てんき", "カテゴリ": "抽象物"},
    },
    {
        "sstring": '"代表表記:新/しん 内容語 NE:ORGANIZATION:head"',
        "dict_": {"代表表記": "新/しん", "内容語": True, "NE": "ORGANIZATION:head"},
    },
    {
        "sstring": "NIL",
        "dict_": {},
    },
]


@pytest.mark.parametrize("case", CASES)
def test_from_fstring(case: Dict[str, Any]) -> None:
    semantics = SemanticsDict.from_sstring(case["sstring"])
    assert dict(semantics) == case["dict_"]


@pytest.mark.parametrize("case", CASES)
def test_to_fstring(case: Dict[str, Any]) -> None:
    semantics = SemanticsDict(case["dict_"], is_nil=True)
    assert semantics.to_sstring() == case["sstring"]


def test_false():
    assert SemanticsDict._item_to_sstring("sem", False) == ""


def test_empty_dict():
    semantics = SemanticsDict({})
    assert semantics.to_sstring() == ""


def test_void():
    semantics = SemanticsDict()
    assert semantics.to_sstring() == ""


def test_empty_string():
    semantics = SemanticsDict.from_sstring("")
    assert semantics.to_sstring() == ""


def test_modification():
    features = SemanticsDict.from_sstring('"代表表記:天気/てんき カテゴリ:抽象物"')
    assert features.to_sstring() == '"代表表記:天気/てんき カテゴリ:抽象物"'
    # Update
    features["代表表記"] = "転機/てんき"
    assert features.to_sstring() == '"代表表記:転機/てんき カテゴリ:抽象物"'
    # Insert
    features["内容語"] = True
    assert features.to_sstring() == '"代表表記:転機/てんき カテゴリ:抽象物 内容語"'
    # Delete
    del features["カテゴリ"]
    assert features.to_sstring() == '"代表表記:転機/てんき 内容語"'
