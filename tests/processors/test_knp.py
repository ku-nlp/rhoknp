import concurrent.futures

import pytest

from rhoknp import KNP, Document, Jumanpp, RegexSenter, Sentence

is_knp_available = KNP().is_available()


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_call() -> None:
    knp = KNP()
    text = "外国人参政権"
    assert isinstance(knp(text), Document)
    assert isinstance(knp(Document.from_raw_text(text)), Document)
    assert isinstance(knp(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        knp(1)  # type: ignore


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_apply() -> None:
    knp = KNP()
    text = "外国人参政権"
    assert isinstance(knp.apply(text), Document)
    assert isinstance(knp.apply(Document.from_raw_text(text)), Document)
    assert isinstance(knp.apply(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        knp.apply(1)  # type: ignore


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;エス'ケープ",  # escape
        "\\エス'ケープ",  # backslash
        "キャリッジ\rリターン",  # carriage return
        "ライン\nフィード",  # line feed
        "CR\r\nLF",  # CR+LF
    ],
)
def test_apply_to_sentence(text: str) -> None:
    knp = KNP()
    sent = knp.apply_to_sentence(text)
    assert sent.text == text.replace("\r", "").replace("\n", "")


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_thread_safe() -> None:
    knp = KNP()
    texts = ["外国人参政権", "望遠鏡で泳いでいる少女を見た。", "エネルギーを素敵にENEOS"]
    texts *= 10
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(knp.apply_to_sentence, text) for text in texts]
        for i, future in enumerate(futures):
            sentence = future.result()
            assert sentence.text == texts[i]


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;エス'ケープ",  # escape
        "\\エス'ケープ",  # backslash
        "キャリッジ\rリターン",  # carriage return
        "ライン\nフィード",  # line feed
        "CR\r\nLF",  # CR+LF
    ],
)
def test_apply_to_document(text: str) -> None:
    knp = KNP()
    doc = knp.apply_to_document(text)
    assert doc.text == text.replace("\r", "").replace("\n", "")


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_get_version() -> None:
    knp = KNP()
    _ = knp.get_version()


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_is_available() -> None:
    knp = KNP()
    assert knp.is_available() is True

    knp = KNP("knpppppppppppppppppppp")
    assert knp.is_available() is False

    with pytest.raises(RuntimeError):
        _ = knp.apply_to_sentence("test")

    with pytest.raises(RuntimeError):
        _ = knp.apply_to_document("test")

    with pytest.raises(RuntimeError):
        _ = knp.get_version()


def test_invalid_option() -> None:
    with pytest.raises(ValueError):
        _ = KNP(options=["--anaphora"])


def test_repr() -> None:
    knp = KNP(options=["-tab"], senter=RegexSenter(), jumanpp=Jumanpp())
    assert (
        repr(knp)
        == "KNP(executable='knp', options=['-tab'], senter=RegexSenter(), jumanpp=Jumanpp(executable='jumanpp'))"
    )
