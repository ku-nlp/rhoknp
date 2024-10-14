import pytest

from rhoknp import KNP, KWJA, Document, Jumanpp, Sentence

is_kwja_available = KWJA(options=["--model-size", "tiny", "--tasks", "typo"]).is_available()


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
def test_char() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "char"])
    text = "こんにちは。さようなら。"
    doc = kwja.apply_to_document(text)
    morphemes = doc.morphemes
    assert len(morphemes) > 0
    morpheme = morphemes[0]
    assert text.startswith(morpheme.text)
    assert morpheme.reading == "*"
    assert morpheme.lemma == "*"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_seq2seq() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "char,seq2seq"])
    text = "こんにちは。さようなら。"
    doc = kwja.apply_to_document(text)
    morphemes = doc.morphemes
    assert len(morphemes) > 0
    morpheme = morphemes[0]
    assert text.startswith(morpheme.text)
    assert text.startswith(morpheme.reading)
    assert text.startswith(morpheme.lemma)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_word() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "char,word"])
    text = "こんにちは。さようなら。"
    doc = kwja.apply_to_document(text)
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
def test_raw_input() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "typo", "--input-format", "raw"])
    text = "人口知能"
    doc = kwja.apply_to_document(text)
    assert doc.text == "人工知能"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_jumanpp_input() -> None:
    doc0 = Document.from_raw_text("こんにちは。さようなら。")
    doc0.doc_id = "test"
    doc1 = Jumanpp().apply_to_document(doc0)
    for idx, sent in enumerate(doc1.sentences):
        sent.sent_id = f"test-{idx}"
    assert not doc1.is_jumanpp_required()
    doc2 = KWJA(options=["--model-size", "tiny", "--tasks", "word", "--input-format", "jumanpp"]).apply_to_document(
        doc1
    )
    assert doc1.doc_id == doc2.doc_id
    assert [sent.sid for sent in doc2.sentences] == [sent.sid for sent in doc1.sentences]
    assert [sent.text for sent in doc2.sentences] == [sent.text for sent in doc1.sentences]
    assert [mrph.text for mrph in doc2.morphemes] == [mrph.text for mrph in doc1.morphemes]


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_knp_input() -> None:
    text = "こんにちは。さようなら。"
    doc1 = KNP().apply_to_document(text)
    assert not doc1.is_knp_required()
    doc2 = KWJA(options=["--model-size", "tiny", "--tasks", "word", "--input-format", "knp"]).apply_to_document(doc1)
    assert doc1.doc_id == doc2.doc_id
    assert [sent.sid for sent in doc2.sentences] == [sent.sid for sent in doc1.sentences]
    assert [sent.text for sent in doc2.sentences] == [sent.text for sent in doc1.sentences]
    assert [mrph.text for mrph in doc2.morphemes] == [mrph.text for mrph in doc1.morphemes]


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
def test_keep_doc_id_document() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    doc = Document.from_sentences(["こんにちは。", "さようなら。"])
    doc.doc_id = "test"
    for sent in doc.sentences:
        sent.doc_id = "test"
    doc = kwja.apply_to_document(doc)
    assert doc.doc_id == "test"
    for sent in doc.sentences:
        assert sent.doc_id == "test"


def test_timeout_error() -> None:
    kwja = KWJA("tests/bin/kwja-mock.sh", skip_sanity_check=True)
    with pytest.raises(TimeoutError):
        _ = kwja.apply_to_document("time consuming input", timeout=1)


def test_runtime_error() -> None:
    kwja = KWJA("tests/bin/kwja-mock.sh", skip_sanity_check=True)
    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_document("error causing input")


def test_unsupported_option() -> None:
    with pytest.raises(ValueError, match=r"invalid task: \['wakachi'\]"):
        _ = KWJA(options=["--model-size", "tiny", "--tasks", "wakachi"])
    with pytest.raises(ValueError, match="invalid input format: seq2seq"):
        _ = KWJA(options=["--model-size", "tiny", "--input-format", "seq2seq"])


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_apply_to_sentence() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    with pytest.raises(NotImplementedError):
        _ = kwja.apply_to_sentence("外国人参政権")


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_repr() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "char,word"])
    assert repr(kwja) == "KWJA(executable='kwja', options=['--model-size', 'tiny', '--tasks', 'char,word'])"
