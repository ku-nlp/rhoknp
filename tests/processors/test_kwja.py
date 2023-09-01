import pytest

from rhoknp import KWJA, Document, Sentence

is_kwja_available = KWJA(options=["--model-size", "tiny", "--tasks", "senter"]).is_available()


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_get_version() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    _ = kwja.get_version()


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_is_available() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    assert kwja.is_available() is True

    kwja = KWJA("kwjaaaaaaaaaaaaaaaaa")
    assert kwja.is_available() is False

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_sentence("test")

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_document("test")

    with pytest.raises(RuntimeError):
        _ = kwja.get_version()


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_typo() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "typo"])
    text = "人口知能"
    doc = kwja.apply_to_document(text)
    assert doc.text == "人工知能"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_senter() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter"])
    text = "こんにちは。さようなら。"
    document = kwja.apply_to_document(text)
    sentences = document.sentences
    assert len(sentences) == 2
    assert sentences[0].text == "こんにちは。"
    assert sentences[1].text == "さようなら。"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_seq2seq() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,seq2seq"])
    text = "こんにちは。さようなら。"
    doc = kwja.apply_to_document(text)
    assert isinstance(doc, Document)
    morphemes = doc.morphemes
    assert len(morphemes) > 0
    morpheme = morphemes[0]
    assert text.startswith(morpheme.text)
    assert text.startswith(morpheme.reading)
    assert text.startswith(morpheme.lemma)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_char() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char"])
    text = "こんにちは。さようなら。"
    doc = kwja.apply_to_document(text)
    assert isinstance(doc, Document)
    morphemes = doc.morphemes
    assert len(morphemes) > 0
    morpheme = morphemes[0]
    assert text.startswith(morpheme.text)
    assert morpheme.reading == "*"
    assert morpheme.lemma == "*"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_word() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char,word"])
    text = "こんにちは。さようなら。"
    doc = kwja.apply_to_document(text)
    assert isinstance(doc, Document)
    morphemes = doc.morphemes
    assert len(morphemes) > 0
    assert text.startswith(morphemes[0].text)
    base_phrases = doc.base_phrases
    assert len(base_phrases) > 0
    assert text.startswith(base_phrases[0].text)
    phrases = doc.phrases
    assert len(phrases) > 0
    assert text.startswith(phrases[0].text)
    clauses = doc.clauses
    assert len(clauses) > 0
    assert text.startswith(clauses[0].text)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_apply() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    text = "外国人参政権"
    assert isinstance(kwja.apply(text), Document)
    assert isinstance(kwja.apply(Document.from_raw_text(text)), Document)
    with pytest.raises(NotImplementedError):
        _ = kwja.apply(Sentence.from_raw_text(text))
    with pytest.raises(TypeError):
        _ = kwja.apply(1)  # type: ignore


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_timeout_error() -> None:
    kwja = KWJA("tests/bin/kwja-mock.sh", skip_sanity_check=True)
    with pytest.raises(TimeoutError):
        _ = kwja.apply_to_document("time consuming input", timeout=1)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_runtime_error() -> None:
    kwja = KWJA("tests/bin/kwja-mock.sh", skip_sanity_check=True)
    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_document("error causing input")


def test_unsupported_option() -> None:
    with pytest.raises(ValueError):
        _ = KWJA(options=["--model-size", "tiny", "--tasks", "wakati"])


def test_apply_to_sentence() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    with pytest.raises(NotImplementedError):
        _ = kwja.apply_to_sentence("外国人参政権")


def test_repr() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char,word"])
    assert repr(kwja) == "KWJA(executable='kwja', options=['--model-size', 'tiny', '--tasks', 'senter,char,word'])"
