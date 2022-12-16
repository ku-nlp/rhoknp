import textwrap
from pathlib import Path

from rhoknp import Document, Sentence
from rhoknp.props import NamedEntity, NamedEntityCategory


def test_ne1() -> None:
    doc_id = "w201106-0000060877"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 2
    assert (nes[0].category, str(nes[0])) == (NamedEntityCategory.ORGANIZATION, "柏市ひまわり園")
    assert (nes[1].category, str(nes[1])) == (NamedEntityCategory.DATE, "平成２３年度")


def test_ne2() -> None:
    doc_id = "w201106-0000074273"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 3
    assert (nes[0].category, str(nes[0])) == (NamedEntityCategory.LOCATION, "ダーマ神殿")
    assert (nes[1].category, str(nes[1])) == (NamedEntityCategory.ARTIFACT, "天の箱舟")
    assert (nes[2].category, str(nes[2])) == (NamedEntityCategory.LOCATION, "ナザム村")


def test_from_fstring_malformed_line() -> None:
    fstring = "MALFORMED LINE"
    ne = NamedEntity.from_fstring(fstring, [])
    assert ne is None


def test_unknown_category() -> None:
    fstring = "UNKNOWN:アンノウン"
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
    ne = NamedEntity.from_fstring(
        fstring,
        sentence.morphemes,
    )
    assert ne is None


def test_span_not_found() -> None:
    fstring = "ORGANIZATION:京都大学"
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
    ne = NamedEntity.from_fstring(
        fstring,
        sentence.morphemes,
    )
    assert ne is None
