import re

import pytest

from rhoknp import Sentence
from rhoknp.utils.util import _extract_did_and_sid


@pytest.mark.parametrize(
    "pat, line, doc_id, sent_id",
    [
        (Sentence.SID_PAT, "# S-ID:1", "1", "1"),
        (Sentence.SID_PAT, "# S-ID:1-1", "1", "1-1"),
        (Sentence.SID_PAT, "# S-ID:1-2", "1", "1-2"),
        (Sentence.SID_PAT, "# S-ID:a-1", "a", "a-1"),
        (Sentence.SID_PAT, "# S-ID:a-2", "a", "a-2"),
        (Sentence.SID_PAT_KWDLC, "# S-ID:w201106-0000060050-1", "w201106-0000060050", "w201106-0000060050-1"),
        (Sentence.SID_PAT_WAC, "# S-ID:wiki00100176-00", "wiki00100176", "wiki00100176-00"),
    ],
)
def test_extract_doc_id(pat: re.Pattern, line: str, doc_id: str, sent_id: str) -> None:
    did, sid, _ = _extract_did_and_sid(line, [pat])
    assert did == doc_id
    assert sid == sent_id
