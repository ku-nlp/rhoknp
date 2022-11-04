from pathlib import Path

from rhoknp import Document, Morpheme
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


def test_double_quote() -> None:
    fstring = r"ORGANIZATION:ダブル\"クオート\""
    ne = NamedEntity.from_fstring(fstring, [Morpheme('ダブル"'), Morpheme('クオート"')])
    assert ne is not None
    assert ne.category == NamedEntityCategory.ORGANIZATION
    assert str(ne) == 'ダブル"クオート"'
    assert ne.to_fstring() == f"<NE:{fstring}>"
