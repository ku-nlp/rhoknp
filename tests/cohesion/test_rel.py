import pytest

from rhoknp.cohesion.rel import RelMode, RelTagList

FSTRINGS = [
    """<rel type="=≒" target="オフェンス" sid="w201106-0001519365-1" id="3"/><rel type="=≒" mode="AND" target="ディフェンス" sid="w201106-0001519365-1" id="4"/><rel type="ノ？" target="著者"/>""",
    """<rel type="ガ" target=">" sid="202209271752-05054-00" id="0"/><rel type="ニ" target="不特定:人"/>""",
    r"""<rel type="ガ" target="ダブル\"クオート\"" sid="202209271752-05054-00" id="0"/>""",
]


def test_from_fstring_0() -> None:
    rels = RelTagList.from_fstring(FSTRINGS[0])
    assert len(rels) == 3

    rel = rels[0]
    assert rel.type == "=≒"
    assert rel.target == "オフェンス"
    assert rel.sid == "w201106-0001519365-1"
    assert rel.base_phrase_index == 3
    assert rel.mode is None

    rel = rels[1]
    assert rel.type == "=≒"
    assert rel.target == "ディフェンス"
    assert rel.sid == "w201106-0001519365-1"
    assert rel.base_phrase_index == 4
    assert rel.mode == RelMode.AND

    rel = rels[2]
    assert rel.type == "ノ？"
    assert rel.target == "著者"
    assert rel.sid is None
    assert rel.base_phrase_index is None
    assert rel.mode is None


def test_from_fstring_1() -> None:
    rels = RelTagList.from_fstring(FSTRINGS[1])
    assert len(rels) == 2

    rel = rels[0]
    assert rel.type == "ガ"
    assert rel.target == ">"
    assert rel.sid == "202209271752-05054-00"
    assert rel.base_phrase_index == 0
    assert rel.mode is None

    rel = rels[1]
    assert rel.type == "ニ"
    assert rel.target == "不特定:人"
    assert rel.sid is None
    assert rel.base_phrase_index is None
    assert rel.mode is None


@pytest.mark.parametrize("fstring", FSTRINGS)
def test_to_fstring(fstring: str) -> None:
    rels = RelTagList.from_fstring(fstring)
    assert rels.to_fstring() == fstring


@pytest.mark.parametrize("fstring", FSTRINGS)
def test_str(fstring: str) -> None:
    rels = RelTagList.from_fstring(fstring)
    assert str(rels) == fstring
