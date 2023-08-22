import concurrent.futures

import pytest

from rhoknp import Document, Jumanpp, RegexSenter, Sentence

is_jumanpp_available = Jumanpp(options=["--juman"]).is_available()


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_call() -> None:
    jumanpp = Jumanpp()
    text = "外国人参政権"
    assert isinstance(jumanpp(text), Document)
    assert isinstance(jumanpp(Document.from_raw_text(text)), Document)
    assert isinstance(jumanpp(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        jumanpp(1)  # type: ignore


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_apply() -> None:
    jumanpp = Jumanpp()
    text = "外国人参政権"
    assert isinstance(jumanpp.apply(text), Document)
    assert isinstance(jumanpp.apply(Document.from_raw_text(text)), Document)
    assert isinstance(jumanpp.apply(Sentence.from_raw_text(text)), Sentence)
    with pytest.raises(TypeError):
        jumanpp.apply(1)  # type: ignore


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
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
def test_apply_to_sentence(text: str) -> None:
    jumanpp = Jumanpp()
    sent = jumanpp.apply_to_sentence(text)
    assert sent.text == text.replace("\r", "").replace("\n", "")


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
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
def test_apply_to_document(text: str) -> None:
    jumanpp = Jumanpp()
    doc = jumanpp.apply_to_document(text)
    assert doc.text == text.replace("\r", "").replace("\n", "")


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_thread_safe() -> None:
    jumanpp = Jumanpp()
    texts = ["外国人参政権", "望遠鏡で泳いでいる少女を見た。", "エネルギーを素敵にENEOS"]
    texts *= 10
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(jumanpp.apply_to_sentence, text) for text in texts]
        for i, future in enumerate(futures):
            sentence = future.result()
            assert sentence.text == texts[i]


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_normal() -> None:
    jumanpp = Jumanpp()
    text = "この文を解析してください。"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 7
    assert "".join(m.text for m in sent.morphemes) == text


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_nominalization() -> None:
    jumanpp = Jumanpp()
    text = "音の響きを感じる。"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 6
    assert "".join(m.text for m in sent.morphemes) == text
    assert sent.morphemes[2].surf == "響き"
    assert sent.morphemes[2].pos == "名詞"


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_whitespace() -> None:
    jumanpp = Jumanpp()
    text = "半角 スペース"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 3
    assert "".join(m.text for m in sent.morphemes) == text
    assert sent.morphemes[1].pos == "特殊"
    assert sent.morphemes[1].subpos == "空白"


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_get_version() -> None:
    jumanpp = Jumanpp()
    _ = jumanpp.get_version()


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
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


@pytest.mark.skipif(not is_jumanpp_available, reason="Juman++ is not available")
def test_timeout() -> None:
    jumanpp = Jumanpp()
    with pytest.raises(TimeoutError):
        _ = jumanpp.apply_to_sentence("test", timeout=0)

    # Ensure that it works after timeout
    _ = jumanpp.apply_to_sentence("test")


def test_repr() -> None:
    jumanpp = Jumanpp(options=["--juman"], senter=RegexSenter())
    assert repr(jumanpp) == "Jumanpp(executable='jumanpp', options=['--juman'], senter=RegexSenter())"
