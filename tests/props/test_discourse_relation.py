import pytest

from rhoknp.props import DiscourseRelationTag, DiscourseRelationTagValue


@pytest.mark.parametrize("sid, base_phrase_index, label, fstring", [("1", 0, "原因・理由", "1/0/原因・理由")])
def test_discourse_relation_tag_value(sid: str, base_phrase_index: int, label: str, fstring: str) -> None:
    v = DiscourseRelationTagValue(sid, base_phrase_index, label)
    assert v.sid == sid
    assert v.base_phrase_index == base_phrase_index
    assert v.label == label
    assert v.to_fstring() == fstring


@pytest.mark.parametrize(
    "fstring, values",
    [
        ("<談話関係:1/0/原因・理由>", [DiscourseRelationTagValue("1", 0, "原因・理由")]),
        (
            "<談話関係:1/0/原因・理由;2/1/原因・理由>",
            [DiscourseRelationTagValue("1", 0, "原因・理由"), DiscourseRelationTagValue("2", 1, "原因・理由")],
        ),
        (
            "<節-区切><談話関係:1/0/原因・理由;2/1/原因・理由>",
            [DiscourseRelationTagValue("1", 0, "原因・理由"), DiscourseRelationTagValue("2", 1, "原因・理由")],
        ),
        ("<節-区切>", []),
    ],
)
def test_from_fstring(fstring: str, values: list[DiscourseRelationTagValue]) -> None:
    discourse_relation_tag = DiscourseRelationTag.from_fstring(fstring)
    assert discourse_relation_tag.values == values
