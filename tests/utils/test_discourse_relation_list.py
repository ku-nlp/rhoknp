import re

import pytest

from rhoknp.units.utils import DiscourseRelation, DiscourseRelationList


def test_discourse_relation_init() -> None:
    _ = DiscourseRelation("w-1111", 2, "逆接(逆方向)")


@pytest.mark.parametrize(
    "fstring, expected",
    [
        ("w-1111/2/逆接(逆方向)", 1),
        ("w-1111/2/逆接(逆方向);w-1111/3/対比", 2),
    ],
)
def test_discourse_relation_pat(fstring: str, expected: int) -> None:
    matches = re.findall(DiscourseRelation.PAT, fstring)
    assert len(matches) == expected


@pytest.mark.parametrize(
    "fstring", ["w-1111/2/逆接(逆方向)", "w-1111/2/逆接(逆方向);w-1111/3/対比"]
)
def test_discourse_relation_list_init(fstring: str) -> None:
    _ = DiscourseRelationList(fstring)


@pytest.mark.parametrize(
    "fstring, expected",
    [
        ("w-1111/2/逆接(逆方向)", 1),
        ("w-1111/2/逆接(逆方向);w-1111/3/対比", 2),
    ],
)
def test_discourse_relation_list_len(fstring: str, expected: int) -> None:
    discourse_relations = DiscourseRelationList(fstring)
    assert len(discourse_relations) == expected


@pytest.mark.parametrize(
    "fstring", ["w-1111/2/逆接(逆方向)", "w-1111/2/逆接(逆方向);w-1111/3/対比"]
)
def test_discourse_relation_list_to_fstring(fstring: str) -> None:
    discourse_relations = DiscourseRelationList(fstring)
    assert discourse_relations.to_fstring() == fstring
