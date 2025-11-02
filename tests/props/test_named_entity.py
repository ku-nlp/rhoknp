import textwrap
from pathlib import Path
from typing import Any

import pytest

from rhoknp import Document, Sentence
from rhoknp.props import NamedEntity, NamedEntityCategory


@pytest.mark.parametrize(
    "case",
    [
        {
            "doc_id": "w201106-0000060877",
            "named_entities": [
                {
                    "category": NamedEntityCategory.ORGANIZATION,
                    "text": "柏市ひまわり園",
                    "fstring": "<NE:ORGANIZATION:柏市ひまわり園>",
                },
                {
                    "category": NamedEntityCategory.DATE,
                    "text": "平成２３年度",
                    "fstring": "<NE:DATE:平成２３年度>",
                },
            ],
        },
        {
            "doc_id": "w201106-0000074273",
            "named_entities": [
                {
                    "category": NamedEntityCategory.LOCATION,
                    "text": "ダーマ神殿",
                    "fstring": "<NE:LOCATION:ダーマ神殿>",
                },
                {
                    "category": NamedEntityCategory.ARTIFACT,
                    "text": "天の箱舟",
                    "fstring": "<NE:ARTIFACT:天の箱舟>",
                },
                {
                    "category": NamedEntityCategory.LOCATION,
                    "text": "ナザム村",
                    "fstring": "<NE:LOCATION:ナザム村>",
                },
            ],
        },
    ],
)
def test_ne(case: dict[str, Any]) -> None:
    doc = Document.from_knp(Path(f"tests/data/{case['doc_id']}.knp").read_text())
    actual_nes = doc.named_entities
    expected_nes = case["named_entities"]
    assert len(actual_nes) == len(expected_nes)
    for actual_ne, expected_ne in zip(actual_nes, expected_nes, strict=True):
        assert actual_ne.category == expected_ne["category"]
        assert actual_ne.text == expected_ne["text"]
        assert str(actual_ne) == expected_ne["text"]
        assert actual_ne.to_fstring() == expected_ne["fstring"]


def test_from_fstring_malformed_line() -> None:
    fstring = "<MALFORMED LINE>"
    ne = NamedEntity.from_fstring(fstring, [])
    assert ne is None


def test_unknown_category() -> None:
    fstring = "<NE:UNKNOWN:アンノウン>"
    sentence = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:1
            * -1D
            + -1D
            アンノウン アンノウン アンノウン 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )
    ne = NamedEntity.from_fstring(fstring, sentence.morphemes)
    assert ne is None


def test_span_not_found() -> None:
    fstring = "<NE:ORGANIZATION:京都大学>"
    sentence = Sentence.from_knp(
        textwrap.dedent(
            """\
            # S-ID:1
            * -1D
            + 1D
            東京 とうきょう 東京 名詞 6 地名 4 * 0 * 0
            + -1D
            大学 だいがく 大学 名詞 6 普通名詞 1 * 0 * 0
            EOS
            """
        )
    )
    ne = NamedEntity.from_fstring(fstring, sentence.morphemes)
    assert ne is None


@pytest.mark.parametrize(
    "case",
    [
        dict(
            fstring=r"<NE:OPTIONAL:html\>タグ>",
            category=NamedEntityCategory.OPTIONAL,
            text="html>タグ",
            knp=textwrap.dedent(
                """\
                # S-ID:1
                * -1D
                + 1D
                < ＜ < 特殊 1 括弧始 3 * 0 * 0
                html html html 名詞 6 普通名詞 1 * 0 * 0
                > ＞ > 特殊 1 括弧終 4 * 0 * 0
                + -1D
                タグ たぐ タグ 名詞 6 普通名詞 1 * 0 * 0
                EOS
                """
            ),
        ),
        dict(
            fstring=r"<NE:OPTIONAL:<html>",
            category=NamedEntityCategory.OPTIONAL,
            text="<html",
            knp=textwrap.dedent(
                """\
                # S-ID:1
                * -1D
                + 1D
                < ＜ < 特殊 1 括弧始 3 * 0 * 0
                html html html 名詞 6 普通名詞 1 * 0 * 0
                > ＞ > 特殊 1 括弧終 4 * 0 * 0
                + -1D
                タグ たぐ タグ 名詞 6 普通名詞 1 * 0 * 0
                EOS
                """
            ),
        ),
        dict(
            fstring=r"<NE:OPTIONAL:バック\スラッシュ>",
            category=NamedEntityCategory.OPTIONAL,
            text=r"バック\スラッシュ",
            knp=textwrap.dedent(
                r"""
                * 1D
                + 2D
                バック ばっく バック 名詞 6 サ変名詞 2 * 0 * 0
                + 2D
                \ \ \ 特殊 1 記号 5 * 0 * 0
                * -1D
                + -1D
                スラッシュ すらっしゅ スラッシュ 名詞 6 普通名詞 1 * 0 * 0
                EOS
                """.lstrip("\n")
            ),
        ),
    ],
)
def test_escape(case: dict[str, Any]) -> None:
    sentence = Sentence.from_knp(case["knp"])
    ne = NamedEntity.from_fstring(case["fstring"], sentence.morphemes)
    assert ne is not None
    assert ne.category == case["category"]
    assert ne.text == case["text"]
    assert ne.to_fstring() == case["fstring"]


def test_escape_in_knp() -> None:
    knp_text = textwrap.dedent(
        r"""
        # S-ID:1
        * -1D
        + 1D
        < ＜ < 特殊 1 括弧始 3 * 0 * 0
        html html html 名詞 6 普通名詞 1 * 0 * 0
        > ＞ > 特殊 1 括弧終 4 * 0 * 0
        + -1D <NE:OPTIONAL:html\>タグ>
        タグ たぐ タグ 名詞 6 普通名詞 1 * 0 * 0
        EOS
        """.lstrip("\n")
    )
    sentence = Sentence.from_knp(knp_text)
    assert sentence.named_entities[0].text == "html>タグ"
    assert sentence.to_knp() == knp_text
