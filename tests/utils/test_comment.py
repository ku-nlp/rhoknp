import re
from typing import Optional

import pytest

from rhoknp import Sentence
from rhoknp.utils.comment import extract_did_and_sid, is_comment_line


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("# S-ID:1", True),
        ("# foo-bar", True),
        ("#", True),
        ("// S-ID:1", False),
        ("// foo-bar", False),
        ("//", False),
        ('# # # 未定義語 15 その他 1 * 0 * 0 "未知語:その他 品詞推定:特殊"', False),
    ],
)
def test_is_comment_line(line: str, expected: bool) -> None:
    assert is_comment_line(line) == expected


@pytest.mark.parametrize(
    ("pat", "line", "doc_id", "sent_id"),
    [
        (Sentence.SID_PAT, "# S-ID:", "", ""),
        (Sentence.SID_PAT, "# S-ID:1", "", "1"),
        (Sentence.SID_PAT, "# S-ID:123", "", "123"),
        (Sentence.SID_PAT, "# S-ID:1a", "1a", "1a"),
        (Sentence.SID_PAT, "# S-ID:1-a", "1-a", "1-a"),
        (Sentence.SID_PAT, "# S-ID:1-1", "1", "1-1"),
        (Sentence.SID_PAT, "# S-ID:1-2", "1", "1-2"),
        (Sentence.SID_PAT, "# S-ID:a-1", "a", "a-1"),
        (Sentence.SID_PAT, "# S-ID:a-2", "a", "a-2"),
        (Sentence.SID_PAT_KWDLC, "# S-ID:w201106-0000060050-1", "w201106-0000060050", "w201106-0000060050-1"),
        (Sentence.SID_PAT_WAC, "# S-ID:wiki00100176-00", "wiki00100176", "wiki00100176-00"),
    ],
)
def test_extract_doc_id(pat: re.Pattern, line: str, doc_id: Optional[str], sent_id: Optional[str]) -> None:
    did, sid, _ = extract_did_and_sid(line, [pat])
    assert did == doc_id
    assert sid == sent_id
