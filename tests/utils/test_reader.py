import re
import textwrap
from io import StringIO
from typing import Any, Dict, Optional

import pytest

from rhoknp import Sentence
from rhoknp.utils.reader import _extract_doc_id, chunk_by_document, chunk_by_sentence

CASES = [
    {
        "text": textwrap.dedent(
            """\
            # S-ID:A-X-1
            EOS
            # S-ID:A-X-2
            EOS
            # S-ID:A-Y-1
            EOS
            """
        ),
        "sentences": [
            "# S-ID:A-X-1\nEOS\n",
            "# S-ID:A-X-2\nEOS\n",
            "# S-ID:A-Y-1\nEOS\n",
        ],
        "documents": [
            "# S-ID:A-X-1\nEOS\n# S-ID:A-X-2\nEOS\n",
            "# S-ID:A-Y-1\nEOS\n",
        ],
        "doc_id_format": "default",
    },
    {
        "text": textwrap.dedent(
            """\
            # S-ID:w201106-0000060050-1
            EOS
            # S-ID:w201106-0000060050-2
            EOS
            """
        ),
        "sentences": [
            "# S-ID:w201106-0000060050-1\nEOS\n",
            "# S-ID:w201106-0000060050-2\nEOS\n",
        ],
        "documents": [
            "# S-ID:w201106-0000060050-1\nEOS\n# S-ID:w201106-0000060050-2\nEOS\n",
        ],
        "doc_id_format": "kwdlc",
    },
    {
        "text": textwrap.dedent(
            """\
            # S-ID:wiki00100176-00
            EOS
            # S-ID:wiki00100176-01
            EOS
            """
        ),
        "sentences": [
            "# S-ID:wiki00100176-00\nEOS\n",
            "# S-ID:wiki00100176-01\nEOS\n",
        ],
        "documents": [
            "# S-ID:wiki00100176-00\nEOS\n# S-ID:wiki00100176-01\nEOS\n",
        ],
        "doc_id_format": "wac",
    },
    {
        "text": textwrap.dedent(
            """\
            # 1-1
            EOS
            # 1-2
            EOS
            # 2-1
            EOS
            """
        ),
        "sentences": [
            "# 1-1\nEOS\n",
            "# 1-2\nEOS\n",
            "# 2-1\nEOS\n",
        ],
        "documents": [
            "# 1-1\nEOS\n# 1-2\nEOS\n",
            "# 2-1\nEOS\n",
        ],
        "doc_id_format": lambda x: x.lstrip("# ").split("-")[0],
    },
    # empty line
    {
        "text": textwrap.dedent(
            """\
            # S-ID:1-1
            EOS

            # S-ID:1-2
            EOS
            """
        ),
        "sentences": [
            "# S-ID:1-1\nEOS\n",
            "# S-ID:1-2\nEOS\n",
        ],
        "documents": [
            "# S-ID:1-1\nEOS\n# S-ID:1-2\nEOS\n",
        ],
        "doc_id_format": "default",
    },
    # no sid
    {
        "text": textwrap.dedent(
            """\
            # 1-1
            EOS
            # 1-2
            EOS
            """
        ),
        "sentences": [
            "# 1-1\nEOS\n",
            "# 1-2\nEOS\n",
        ],
        "documents": [
            "# 1-1\nEOS\n",
            "# 1-2\nEOS\n",
        ],
        "doc_id_format": "default",
    },
    # no trailing EOS
    {
        "text": textwrap.dedent(
            """\
            # S-ID:1-1
            EOS
            # S-ID:1-2
            """
        ),
        "sentences": [
            "# S-ID:1-1\nEOS\n",
            "# S-ID:1-2\n",
        ],
        "documents": [
            "# S-ID:1-1\nEOS\n# S-ID:1-2\n",
        ],
        "doc_id_format": "default",
    },
    # invalid sid
    {
        "text": textwrap.dedent(
            """\
            # S-ID:1-1
            EOS
            # S-ID:1-2
            EOS
            # S-ID:2-1
            EOS
            """
        ),
        "sentences": [
            "# S-ID:1-1\nEOS\n",
            "# S-ID:1-2\nEOS\n",
            "# S-ID:2-1\nEOS\n",
        ],
        "documents": [
            "# S-ID:1-1\nEOS\n",
            "# S-ID:1-2\nEOS\n",
            "# S-ID:2-1\nEOS\n",
        ],
        "doc_id_format": "kwdlc",
    },
]


@pytest.mark.parametrize("case", CASES)
def test_chunk_by_sentence(case: Dict[str, Any]) -> None:
    actual = list(chunk_by_sentence(StringIO(case["text"])))
    assert actual == case["sentences"]


@pytest.mark.parametrize("case", CASES)
def test_chunk_by_document(case: Dict[str, Any]) -> None:
    actual = list(chunk_by_document(StringIO(case["text"]), doc_id_format=case["doc_id_format"]))
    assert actual == case["documents"]


@pytest.mark.parametrize("doc_id_format", ["ERROR", 1])
def test_chunk_by_document_error(doc_id_format: Any) -> None:
    with pytest.raises(ValueError):
        _ = list(chunk_by_document(StringIO(""), doc_id_format=doc_id_format))  # noqa


@pytest.mark.parametrize(
    "pat, line, doc_id",
    [
        (Sentence.SID_PAT, "# S-ID:1", "1"),
        (Sentence.SID_PAT, "# S-ID:1-1", "1"),
        (Sentence.SID_PAT, "# S-ID:1-2", "1"),
        (Sentence.SID_PAT, "# S-ID:a-1", "a"),
        (Sentence.SID_PAT, "# S-ID:a-2", "a"),
        (Sentence.SID_PAT_KWDLC, "# S-ID:w201106-0000060050-1", "w201106-0000060050"),
        (Sentence.SID_PAT_WAC, "# S-ID:wiki00100176-00", "wiki00100176"),
    ],
)
def test_extract_doc_id(pat: re.Pattern, line: str, doc_id: Optional[str]) -> None:
    assert _extract_doc_id(pat)(line) == doc_id