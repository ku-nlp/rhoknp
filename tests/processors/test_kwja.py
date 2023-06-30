from typing import Generator

import pytest
from fastapi.testclient import TestClient

from rhoknp import KWJA, Document, Sentence
from rhoknp.cli.serve import AnalyzerType, create_app

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
    text = "こんにちは。さようなら。"
    document = kwja.apply_to_document(text)
    sentences = document.sentences
    assert len(sentences) == 2
    assert sentences[0].text == "こんにちは。"
    assert sentences[1].text == "さようなら。"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_seq2seq() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,seq2seq"])
    text = "こんにちは"
    for doc_or_sent in (kwja.apply_to_document(text), kwja.apply_to_sentence(text)):
        assert isinstance(doc_or_sent, (Document, Sentence))
        morphemes = doc_or_sent.morphemes
        assert len(morphemes) == 1
        morpheme = morphemes[0]
        assert morpheme.text == morpheme.reading == morpheme.lemma == "こんにちは"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_char() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "senter,char"])
    text = "こんにちは"
    for doc_or_sent in (kwja.apply_to_document(text), kwja.apply_to_sentence(text)):
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
    text = "こんにちは"
    for doc_or_sent in (kwja.apply_to_document(text), kwja.apply_to_sentence(text)):
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


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
@pytest.fixture()
def kwja_client() -> Generator[TestClient, None, None]:
    app = create_app(AnalyzerType.KWJA, options=["--model-size", "tiny", "--tasks", "senter,char,word"])
    yield TestClient(app)


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
@pytest.mark.parametrize("text", ["こんにちは"])
def test_cli_serve_analyze_kwja(kwja_client: TestClient, text: str) -> None:
    response = kwja_client.get("/analyze", params={"text": text})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_knp(json["result"])
    assert document.text == text


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
def test_analyze_kwja_error_empty(kwja_client: TestClient) -> None:
    error_causing_text = ""
    response = kwja_client.get("/analyze", params={"text": error_causing_text})
    assert response.status_code == 400
    json = response.json()
    assert "error" in json
    assert json["error"]["code"] == 400
    assert json["error"]["message"] == "text is empty"


@pytest.mark.skipif(not is_kwja_available, reason="KWJA is not available")
@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_cli_serve_index_kwja(kwja_client: TestClient, text: str) -> None:
    response = kwja_client.get("/", params={"text": text})
    assert response.status_code == 200
