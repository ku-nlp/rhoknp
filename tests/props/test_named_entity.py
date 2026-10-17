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
    doc = Document.from_knp(Path(f"tests/data/{case['doc_id']}.knp").read_text(encoding="utf-8"))
    actual_nes = doc.named_entities
    expected_nes = case["named_entities"]
    assert len(actual_nes) == len(expected_nes)
    for actual_ne, expected_ne in zip(actual_nes, expected_nes, strict=True):
        assert actual_ne.category == expected_ne["category"]
        assert actual_ne.text == expected_ne["text"]
        assert str(actual_ne) == expected_ne["text"]
        assert actual_ne.to_fstring() == expected_ne["fstring"]
        assert actual_ne.possible_categories == []
        assert actual_ne.optional_type is None


def test_from_fstring_malformed_line() -> None:
    fstring = "<MALFORMED LINE>"
    ne = NamedEntity.from_fstring(fstring, [])
    assert ne is None


@pytest.mark.parametrize("category", ["UNKNOWN", "NONE"])
def test_invalid_category(category: str) -> None:
    fstring = f"<NE:{category}:アンノウン>"
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
    ("optional_value", "categories", "optional_type"),
    [
        ("ORGANIZATION,NONE:0", ["ORGANIZATION", "NONE"], 0),
        ("NONE:0", ["NONE"], 0),
        ("ORGANIZATION,PERSON,LOCATION:0", ["ORGANIZATION", "PERSON", "LOCATION"], 0),
        ("LOCATION:1", ["LOCATION"], 1),
        ("PERSON,NONE:2", ["PERSON", "NONE"], 2),
        ("PERSON,NONE:3", ["PERSON", "NONE"], 3),
        ("PERSON,NONE:4", ["PERSON", "NONE"], 4),
    ],
)
def test_ne_optional(optional_value: str, categories: list[str], optional_type: int) -> None:
    fstring = f"<NE:OPTIONAL:新幹線総局><NE-OPTIONAL:{optional_value}>"
    knp_text = textwrap.dedent(
        f"""\
        # S-ID:1
        * -1D
        + 1D
        新幹線 しんかんせん 新幹線 名詞 6 普通名詞 1 * 0 * 0
        + -1D {fstring}
        総局 そうきょく 総局 名詞 6 普通名詞 1 * 0 * 0
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert len(document.named_entities) == 1
    ne = document.named_entities[0]
    assert ne.category == NamedEntityCategory.OPTIONAL
    assert ne.text == "新幹線総局"
    assert [category.value for category in ne.possible_categories] == categories
    assert ne.optional_type == optional_type
    assert ne.to_fstring() == fstring
    assert document.to_knp() == knp_text

    parsed_ne = NamedEntity.from_fstring(f"{fstring}<体言>", document.morphemes)
    assert parsed_ne == ne


@pytest.mark.parametrize(
    "fstring",
    [
        "<NE:OPTIONAL:アンノウン><NE-OPTIONAL:UNKNOWN:0>",
        "<NE:OPTIONAL:アンノウン><NE-OPTIONAL:OPTIONAL:0>",
        "<NE:PERSON:アンノウン><NE-OPTIONAL:PERSON:0>",
    ],
)
def test_ne_optional_invalid(fstring: str) -> None:
    sentence = Sentence.from_jumanpp("アンノウン アンノウン アンノウン 名詞 6 普通名詞 1 * 0 * 0\nEOS\n")
    assert NamedEntity.from_fstring(fstring, sentence.morphemes) is None


@pytest.mark.parametrize(
    "suffix",
    [
        "",
        "<体言>",
        "<NE-OPTIONAL:PERSON:x>",
    ],
)
def test_ne_optional_unmatched(suffix: str) -> None:
    sentence = Sentence.from_jumanpp("アンノウン アンノウン アンノウン 名詞 6 普通名詞 1 * 0 * 0\nEOS\n")
    ne = NamedEntity.from_fstring(f"<NE:OPTIONAL:アンノウン>{suffix}", sentence.morphemes)
    assert ne is not None
    assert ne.category == NamedEntityCategory.OPTIONAL
    assert ne.text == "アンノウン"
    assert ne.possible_categories == []
    assert ne.optional_type is None
    assert ne.to_fstring() == "<NE:OPTIONAL:アンノウン>"


def test_ne_optional_tag_in_name() -> None:
    text = "<NE-OPTIONAL:PERSON:3>"
    sentence = Sentence.from_jumanpp(f"{text} {text} {text} 名詞 6 普通名詞 1 * 0 * 0\nEOS\n")
    fstring = r"<NE:OPTIONAL:<NE-OPTIONAL:PERSON:3\>>"
    ne = NamedEntity.from_fstring(fstring, sentence.morphemes)
    assert ne is not None
    assert ne.text == text
    assert ne.possible_categories == []
    assert ne.optional_type is None
    assert ne.to_fstring() == fstring


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


@pytest.mark.parametrize("optional_fstring", ["", "<NE-OPTIONAL:ARTIFACT,NONE:0>"])
def test_escape_in_knp(optional_fstring: str) -> None:
    knp_text = textwrap.dedent(
        rf"""
        # S-ID:1
        * -1D
        + 1D
        < ＜ < 特殊 1 括弧始 3 * 0 * 0
        html html html 名詞 6 普通名詞 1 * 0 * 0
        > ＞ > 特殊 1 括弧終 4 * 0 * 0
        + -1D <NE:OPTIONAL:html\>タグ>{optional_fstring}
        タグ たぐ タグ 名詞 6 普通名詞 1 * 0 * 0
        EOS
        """.lstrip("\n")
    )
    sentence = Sentence.from_knp(knp_text)
    assert sentence.named_entities[0].text == "html>タグ"
    assert sentence.named_entities[0].to_fstring() == rf"<NE:OPTIONAL:html\>タグ>{optional_fstring}"
    assert sentence.to_knp() == knp_text
