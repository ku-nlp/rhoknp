import pytest

from rhoknp.cohesion.rel import RelMode, RelTagList

FSTRINGS = [
    """<rel type="=≒" target="オフェンス" sid="w201106-0001519365-1" id="3"/><rel type="=≒" mode="AND" target="ディフェンス" sid="w201106-0001519365-1" id="4"/><rel type="ノ？" target="著者"/>""",
    """<rel type="ガ" target=">" sid="202209271752-05054-00" id="0"/><rel type="ニ" target="不特定:人"/>""",
    """<rel type="ほげ" target="ふが" sid="000-00" id="0"/><rel type="=hoge" target="fuga"/>""",
]


def test_from_fstring_0() -> None:
    rel_tags = RelTagList.from_fstring(FSTRINGS[0])
    assert len(rel_tags) == 3

    rel_tag = rel_tags[0]
    assert rel_tag.type == "=≒"
    assert rel_tag.target == "オフェンス"
    assert rel_tag.sid == "w201106-0001519365-1"
    assert rel_tag.base_phrase_index == 3
    assert rel_tag.mode is None

    rel_tag = rel_tags[1]
    assert rel_tag.type == "=≒"
    assert rel_tag.target == "ディフェンス"
    assert rel_tag.sid == "w201106-0001519365-1"
    assert rel_tag.base_phrase_index == 4
    assert rel_tag.mode == RelMode.AND

    rel_tag = rel_tags[2]
    assert rel_tag.type == "ノ？"
    assert rel_tag.target == "著者"
    assert rel_tag.sid is None
    assert rel_tag.base_phrase_index is None
    assert rel_tag.mode is None


def test_from_fstring_1() -> None:
    rel_tags = RelTagList.from_fstring(FSTRINGS[1])
    assert len(rel_tags) == 2

    rel_tag = rel_tags[0]
    assert rel_tag.type == "ガ"
    assert rel_tag.target == ">"
    assert rel_tag.sid == "202209271752-05054-00"
    assert rel_tag.base_phrase_index == 0
    assert rel_tag.mode is None

    rel_tag = rel_tags[1]
    assert rel_tag.type == "ニ"
    assert rel_tag.target == "不特定:人"
    assert rel_tag.sid is None
    assert rel_tag.base_phrase_index is None
    assert rel_tag.mode is None


@pytest.mark.parametrize("fstring", FSTRINGS)
def test_to_fstring(fstring: str) -> None:
    rel_tags = RelTagList.from_fstring(fstring)
    assert rel_tags.to_fstring() == fstring


@pytest.mark.parametrize("fstring", FSTRINGS)
def test_str(fstring: str) -> None:
    rel_tags = RelTagList.from_fstring(fstring)
    assert str(rel_tags) == fstring
