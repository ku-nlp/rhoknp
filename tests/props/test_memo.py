import pytest

from rhoknp.props.memo import MemoTag

CASES = [
    {
        "from_fstring": """<rel type="ノ" target="不特定:人"/><memo text="メモ"/><体言>""",
        "to_fstring": """<memo text="メモ"/>""",
        "text": "メモ",
        "bool": True,
    },
    {
        "from_fstring": """<memo text="メモ1"/><memo text="メモ2"/>""",
        "to_fstring": """<memo text="メモ1"/>""",
        "text": "メモ1",
        "bool": True,
    },
    {
        "from_fstring": """<memo text=""/>""",
        "to_fstring": """<memo text=""/>""",
        "text": "",
        "bool": False,
    },
    {
        "from_fstring": """<memo text="<メモ>  'quote' "double quote""/>""",
        "to_fstring": """<memo text="<メモ>  'quote' "double quote""/>""",
        "text": """<メモ>  'quote' "double quote\"""",
        "bool": True,
    },
]


@pytest.mark.parametrize("case", CASES)
def test_from_fstring(case: dict) -> None:
    memo_tag = MemoTag.from_fstring(case["from_fstring"])
    assert memo_tag.text == case["text"]


@pytest.mark.parametrize("case", CASES)
def test_to_fstring(case: dict) -> None:
    memo_tag = MemoTag.from_fstring(case["from_fstring"])
    assert memo_tag.to_fstring() == case["to_fstring"]


@pytest.mark.parametrize("case", CASES)
def test_str(case: dict) -> None:
    memo_tag = MemoTag.from_fstring(case["from_fstring"])
    assert str(memo_tag) == case["to_fstring"]


@pytest.mark.parametrize("case", CASES)
def test_bool(case: dict) -> None:
    memo_tag = MemoTag.from_fstring(case["from_fstring"])
    assert bool(memo_tag) == case["bool"]
