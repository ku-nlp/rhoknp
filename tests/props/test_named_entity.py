from pathlib import Path

from rhoknp import Document


def test_ne1() -> None:
    doc_id = "w201106-0000060877"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 2
    assert (nes[0].category, nes[0].text) == ("ORGANIZATION", "柏市ひまわり園")
    assert (nes[1].category, nes[1].text) == ("DATE", "平成２３年度")


def test_ne2() -> None:
    doc_id = "w201106-0000074273"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 3
    assert (nes[0].category, nes[0].text) == ("LOCATION", "ダーマ神殿")
    assert (nes[1].category, nes[1].text) == ("ARTIFACT", "天の箱舟")
    assert (nes[2].category, nes[2].text) == ("LOCATION", "ナザム村")
