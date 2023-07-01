import pytest

from rhoknp import KWJA, Document, Sentence

is_kwja_available = KWJA(options=["--model-size", "tiny"]).is_available()


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
    for doc_or_sent in (kwja.apply_to_document(text), kwja.apply_to_sentence(text)):
        assert doc_or_sent.text == "人工知能"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_senter() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter"])
    document = kwja.apply_to_document("こんにちは。さようなら。")
    sentences = document.sentences
    assert len(sentences) == 2
    assert sentences[0].text == "こんにちは。"
    assert sentences[1].text == "さようなら。"
    sentence = kwja.apply_to_sentence("こんにちは。")
    assert sentence.text == "こんにちは。"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_seq2seq() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,seq2seq"])
    for doc_or_sent, text in zip(
        (kwja.apply_to_document("こんにちは。さようなら"), kwja.apply_to_sentence("さようなら")),
        ("こんにちは。さようなら", "さようなら"),
    ):
        assert isinstance(doc_or_sent, (Document, Sentence))
        morphemes = doc_or_sent.morphemes
        assert len(morphemes) > 0
        morpheme = morphemes[0]
        assert text.startswith(morpheme.text)
        assert text.startswith(morpheme.reading)
        assert text.startswith(morpheme.lemma)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_char() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char"])
    for doc_or_sent, text in zip(
        (kwja.apply_to_document("こんにちは。さようなら"), kwja.apply_to_sentence("さようなら")),
        ("こんにちは。さようなら", "さようなら"),
    ):
        assert isinstance(doc_or_sent, (Document, Sentence))
        morphemes = doc_or_sent.morphemes
        assert len(morphemes) > 0
        morpheme = morphemes[0]
        assert text.startswith(morpheme.text)
        assert morpheme.reading == "*"
        assert morpheme.lemma == "*"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_word() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char,word"])
    for doc_or_sent, text in zip(
        (kwja.apply_to_document("こんにちは。さようなら"), kwja.apply_to_sentence("さようなら")),
        ("こんにちは。さようなら", "さようなら"),
    ):
        assert isinstance(doc_or_sent, (Document, Sentence))
        morphemes = doc_or_sent.morphemes
        assert len(morphemes) > 0
        assert text.startswith(morphemes[0].text)
        base_phrases = doc_or_sent.base_phrases
        assert len(base_phrases) > 0
        assert text.startswith(base_phrases[0].text)
        phrases = doc_or_sent.phrases
        assert len(phrases) > 0
        assert text.startswith(phrases[0].text)
        clauses = doc_or_sent.clauses
        assert len(clauses) > 0
        assert text.startswith(clauses[0].text)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_apply() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    text = "外国人参政権"
    assert isinstance(kwja.apply(text), Document)
    assert isinstance(kwja.apply(Document.from_raw_text(text)), Document)
    assert isinstance(kwja.apply(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        kwja.apply(1)  # type: ignore


def test_unsupported_option() -> None:
    with pytest.raises(ValueError):
        _ = KWJA(options=["--model-size", "tiny", "--tasks", "wakati"])


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80Dを買った",  # EOS
        "文書終端記号は EOD",  # EOD
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        "\\エス'ケープ",  # backslash
        "キャリッジ\rリターン",  # carriage return
        "ライン\nフィード",  # line feed
        "CR\r\nLF",  # CR+LF
    ],
)
def test_apply_to_sentence(text: str) -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    sent = kwja.apply_to_sentence(text)
    assert sent.text == text.replace('"', "”").replace(" ", "␣").replace("\r", "").replace("\n", "")


def test_repr() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char,word"])
    assert repr(kwja) == "KWJA(executable='kwja', options=['--model-size', 'tiny', '--tasks', 'senter,char,word'])"
