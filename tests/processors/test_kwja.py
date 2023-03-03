from typing import Generator

import pytest
from fastapi.testclient import TestClient

from rhoknp import KWJA, Document, Sentence
from rhoknp.cli.serve import AnalyzerType, create_app


def test_typo() -> None:
    kwja = KWJA(options=["--model-size", "tiny", "--tasks", "typo"])
    text = "人口知能"
    document = kwja.apply_to_document(text)
    sentence = kwja.apply_to_sentence(text)
    assert document.text == "人工知能"
    assert sentence.text == "人工知能"


@pytest.fixture()
def kwja() -> Generator[KWJA, None, None]:
    model = KWJA(options=["--model-size", "tiny", "--tasks", "char,word"])
    # Workaround for the formatting error due to the debug message emitted from transformers
    # TODO: Remove this after KWJA that depends on transformers>=4.27.0 is released
    try:
        _ = model.apply("...")
    except ValueError:
        pass
    yield model


def test_apply(kwja: KWJA) -> None:
    text = "外国人参政権"
    assert isinstance(kwja.apply(text), Document)
    assert isinstance(kwja.apply(Document.from_raw_text(text)), Document)
    assert isinstance(kwja.apply(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        kwja.apply(1)  # type: ignore


def test_unsupported_option() -> None:
    with pytest.raises(ValueError):
        _ = KWJA(options=["--model-size", "tiny", "--tasks", "typo,char"])

    with pytest.raises(ValueError):
        _ = KWJA(options=["--model-size", "tiny", "--tasks", "wakati"])


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80Dを買った",  # EOS
        # "文書終端記号は EOD",  # EOD  # TODO
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        "\\エス'ケープ",  # backslash
        "キャリッジ\rリターン",  # carriage return
        "ライン\nフィード",  # line feed
        "CR\r\nLF",  # CR+LF
    ],
)
def test_apply_to_sentence(kwja: KWJA, text: str) -> None:
    sent = kwja.apply_to_sentence(text)
    assert sent.text == text.replace('"', "”").replace(" ", "␣").replace("\r", "").replace("\n", "")


def test_is_available(kwja: KWJA) -> None:
    assert kwja.is_available() is True

    kwja = KWJA("kwjaaaaaaaaaaaaaaaaa")
    assert kwja.is_available() is False

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_sentence("test")

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_document("test")


def test_repr(kwja: KWJA) -> None:
    assert repr(kwja) == "KWJA(executable='kwja', options=['--model-size', 'tiny', '--tasks', 'char,word'])"


@pytest.fixture()
def kwja_client() -> Generator[TestClient, None, None]:
    app = create_app(AnalyzerType.KWJA, options=["--model-size", "tiny", "--tasks", "char,word"])
    yield TestClient(app)


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_cli_serve_analyze_kwja(kwja_client: TestClient, text: str) -> None:
    response = kwja_client.get("/analyze", params={"text": text})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_knp(json["result"])
    assert document.text == text


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_cli_serve_index_kwja(kwja_client: TestClient, text: str) -> None:
    response = kwja_client.get("/", params={"text": text})
    assert response.status_code == 200
