import concurrent.futures
from typing import Generator

import pytest

from rhoknp import Document, Jumanpp, RegexSenter, Sentence


@pytest.fixture()
def jumanpp() -> Generator[Jumanpp, None, None]:
    yield Jumanpp(options=["--juman"])


def test_call(jumanpp: Jumanpp) -> None:
    text = "外国人参政権"
    assert isinstance(jumanpp(text), Document)
    assert isinstance(jumanpp(Document.from_raw_text(text)), Document)
    assert isinstance(jumanpp(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        jumanpp(1)  # type: ignore


def test_apply(jumanpp: Jumanpp) -> None:
    text = "外国人参政権"
    assert isinstance(jumanpp.apply(text), Document)
    assert isinstance(jumanpp.apply(Document.from_raw_text(text)), Document)
    assert isinstance(jumanpp.apply(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        jumanpp.apply(1)  # type: ignore


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        "キャリッジ\rリターン",  # carriage return
        "ライン\nフィード",  # line feed
        "CR\r\nLF",  # CR+LF
    ],
)
def test_apply_to_sentence(jumanpp: Jumanpp, text: str) -> None:
    sent = jumanpp.apply_to_sentence(text)
    assert sent.text == text.replace(" ", "　").replace('"', "”").replace("\r", "").replace("\n", "")


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        "キャリッジ\rリターン",  # carriage return
        "ライン\nフィード",  # line feed
        "CR\r\nLF",  # CR+LF
    ],
)
def test_apply_to_document(jumanpp: Jumanpp, text: str) -> None:
    doc = jumanpp.apply_to_document(text)
    assert doc.text == text.replace(" ", "　").replace('"', "”").replace("\r", "").replace("\n", "")


def test_thread_safe(jumanpp: Jumanpp) -> None:
    texts = ["外国人参政権", "望遠鏡で泳いでいる少女を見た。", "エネルギーを素敵にENEOS"]
    texts *= 10
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(jumanpp.apply_to_sentence, text) for text in texts]
        for i, future in enumerate(futures):
            sentence = future.result()
            assert sentence.text == texts[i]


def test_normal(jumanpp: Jumanpp) -> None:
    text = "この文を解析してください。"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 7
    assert "".join(m.text for m in sent.morphemes) == text


def test_nominalization(jumanpp: Jumanpp) -> None:
    text = "音の響きを感じる。"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 6
    assert "".join(m.text for m in sent.morphemes) == text
    assert sent.morphemes[2].surf == "響き"
    assert sent.morphemes[2].pos == "名詞"


def test_whitespace(jumanpp: Jumanpp) -> None:
    text = "半角 スペース"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 3
    assert "".join(m.text for m in sent.morphemes) == text.replace(" ", "　")
    assert sent.morphemes[1].pos == "特殊"
    assert sent.morphemes[1].subpos == "空白"


def test_get_version() -> None:
    jumanpp = Jumanpp()
    _ = jumanpp.get_version()


def test_is_available() -> None:
    jumanpp = Jumanpp()
    assert jumanpp.is_available() is True

    jumanpp = Jumanpp("jumanppppppppppppppppppppppppppppp")
    assert jumanpp.is_available() is False

    with pytest.raises(RuntimeError):
        _ = jumanpp.apply_to_sentence("test")

    with pytest.raises(RuntimeError):
        _ = jumanpp.apply_to_document("test")

    with pytest.raises(RuntimeError):
        _ = jumanpp.get_version()


def test_repr() -> None:
    jumanpp = Jumanpp(options=["--juman"], senter=RegexSenter())
    assert repr(jumanpp) == "Jumanpp(executable='jumanpp', options=['--juman'], senter=RegexSenter())"
