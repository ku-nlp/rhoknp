from typing import Generator

import pytest

from rhoknp import KWJA, Document, Sentence


@pytest.fixture()
def kwja() -> Generator[KWJA, None, None]:
    model = KWJA(options=["--model-size", "tiny"])
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
def test_apply_to_sentence(kwja: KWJA, text: str) -> None:
    sent = kwja.apply_to_sentence(text)
    assert sent.text == text.replace('"', "”").replace(" ", "␣").replace("\r", "").replace("\n", "")


def test_is_available() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    assert kwja.is_available() is True

    kwja = KWJA("kwjaaaaaaaaaaaaaaaaa")
    assert kwja.is_available() is False

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_sentence("test")

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_document("test")


def test_repr() -> None:
    kwja = KWJA(options=["--model-size", "tiny"])
    assert repr(kwja) == "KWJA(executable='kwja', options=['--model-size', 'tiny'])"
