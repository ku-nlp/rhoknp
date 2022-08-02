from pathlib import Path

from rhoknp import Document


def test_ne1() -> None:
    doc_id = "w201106-0000060877"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 2
    ne = nes[0]
    assert (ne.category, ne.text) == ("ORGANIZATION", "柏市ひまわり園")
    ne = nes[1]
    assert (ne.category, ne.text) == ("DATE", "平成２３年度")


def test_ne2() -> None:
    doc_id = "w201106-0000074273"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 3
    ne = nes[0]
    assert (ne.category, ne.text) == ("LOCATION", "ダーマ神殿")
    ne = nes[1]
    assert (ne.category, ne.text) == ("ARTIFACT", "天の箱舟")
    ne = nes[2]
    assert (ne.category, ne.text) == ("LOCATION", "ナザム村")
