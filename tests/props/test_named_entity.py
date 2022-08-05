import re
import textwrap
from pathlib import Path

from rhoknp import Document, Sentence
from rhoknp.props import NamedEntity, NamedEntityCategory


def test_ne1() -> None:
    doc_id = "w201106-0000060877"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 2
    assert (nes[0].category, nes[0].text) == (NamedEntityCategory.ORGANIZATION, "柏市ひまわり園")
    assert (nes[1].category, nes[1].text) == (NamedEntityCategory.DATE, "平成２３年度")


def test_ne2() -> None:
    doc_id = "w201106-0000074273"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    nes = doc.named_entities
    assert len(nes) == 3
    assert (nes[0].category, nes[0].text) == (NamedEntityCategory.LOCATION, "ダーマ神殿")
    assert (nes[1].category, nes[1].text) == (NamedEntityCategory.ARTIFACT, "天の箱舟")
    assert (nes[2].category, nes[2].text) == (NamedEntityCategory.LOCATION, "ナザム村")


def test_clear() -> None:
    doc_id = "w201106-0000060877"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    assert len(doc.named_entities) == 2
    for sentence in doc.sentences:
        sentence.named_entities.clear()
    assert len(doc.named_entities) == 0
    assert "NE" not in doc.to_knp()


def test_remove() -> None:
    doc_id = "w201106-0000060877"
    doc = Document.from_knp(Path(f"tests/data/{doc_id}.knp").read_text())
    assert len(doc.named_entities) == 2
    doc.sentences[0].named_entities.remove(doc.named_entities[0])
    assert len(doc.named_entities) == 1
    assert len(re.findall("NE", doc.to_knp())) == 1


knp_text = textwrap.dedent(
    """\
    # S-ID:1
    * 1D
    + 1D
    100 100 100 名詞 6 数詞 7 * 0 * 0
    円 えん 円 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0
    を を を 助詞 9 格助詞 1 * 0 * 0
    * -1D
    + -1D
    拾う ひろう 拾う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
    EOS
    """
)
knp_text_with_ne = textwrap.dedent(
    """\
    # S-ID:1
    * 1D
    + 1D <NE:MONEY:100円>
    100 100 100 名詞 6 数詞 7 * 0 * 0
    円 えん 円 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0
    を を を 助詞 9 格助詞 1 * 0 * 0
    * -1D
    + -1D
    拾う ひろう 拾う 動詞 2 * 0 子音動詞ワ行 12 基本形 2
    EOS
    """
)


def test_append() -> None:
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.named_entities) == 0
    sentence.named_entities.append(NamedEntity(NamedEntityCategory.MONEY, sentence.morphemes[0:2]))
    assert len(sentence.named_entities) == 1
    assert sentence.to_knp() == knp_text_with_ne


def test_insert() -> None:
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.named_entities) == 0
    sentence.named_entities.insert(0, NamedEntity(NamedEntityCategory.MONEY, sentence.morphemes[0:2]))
    assert len(sentence.named_entities) == 1
    assert sentence.to_knp() == knp_text_with_ne


def test_extend() -> None:
    sentence = Sentence.from_knp(knp_text)
    assert len(sentence.named_entities) == 0
    sentence.named_entities.extend([NamedEntity(NamedEntityCategory.MONEY, sentence.morphemes[0:2])])
    assert len(sentence.named_entities) == 1
    assert sentence.to_knp() == knp_text_with_ne
