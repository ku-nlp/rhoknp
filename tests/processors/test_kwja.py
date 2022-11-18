import pytest

from rhoknp import KWJA, Document, Sentence


def test_apply() -> None:
    kwja = KWJA()
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
        # "Canon EOS 80D買った",  # EOS  # TODO
        # '"最高"の気分',  # double quotes  # TODO
        "&lt;tag&gt;\\エス'ケープ",  # escape
        # "これは\rどう",  # carriage return  # TODO
    ],
)
def test_apply_to_sentence(text: str) -> None:
    kwja = KWJA()
    sent = kwja.apply_to_sentence(text)
    assert sent.text == text


def test_is_available() -> None:
    kwja = KWJA()
    assert kwja.is_available() is True

    kwja = KWJA("kwjaa")
    assert kwja.is_available() is False

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_sentence("test")

    with pytest.raises(RuntimeError):
        _ = kwja.apply_to_document("test")


def test_repr() -> None:
    kwja = KWJA(options=["--text"])
    assert repr(kwja) == "KWJA(executable='kwja', options=['--text'])"