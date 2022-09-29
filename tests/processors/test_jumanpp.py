import pytest

from rhoknp import Jumanpp, RegexSenter


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        # "これは\rどう",  # carriage return  # TODO
    ],
)
def test_jumanpp_apply(text: str) -> None:
    jumanpp = Jumanpp(options=["--juman"])
    doc = jumanpp.apply(text)
    assert doc.text == text.replace(" ", "　").replace('"', "”")


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        # "これは\rどう",  # carriage return  # TODO
    ],
)
def test_jumanpp_apply_to_sentence(text: str) -> None:
    jumanpp = Jumanpp(options=["--juman"])
    sent = jumanpp.apply_to_sentence(text)
    assert sent.text == text.replace(" ", "　").replace('"', "”")


@pytest.mark.parametrize(
    "text",
    [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",  # EOS
        "Canon EOS 80D買った",  # EOS
        '"最高"の気分',  # double quotes
        "&lt;tag&gt;\\エス'ケープ",  # escape
        # "これは\rどう",  # carriage return  # TODO
    ],
)
def test_jumanpp_apply_to_document(text: str) -> None:
    jumanpp = Jumanpp()
    doc = jumanpp.apply_to_document(text)
    assert doc.text == text.replace(" ", "　").replace('"', "”")


def test_jumanpp_batch_apply() -> None:
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    jumanpp = Jumanpp()
    docs = jumanpp.batch_apply(texts)
    assert [doc.text for doc in docs] == texts

    # parallel
    docs = jumanpp.batch_apply(texts, processes=2)
    assert [doc.text for doc in docs] == texts

    docs = jumanpp.batch_apply(texts, processes=4)
    assert [doc.text for doc in docs] == texts


def test_jumanpp_batch_apply_to_sentences() -> None:
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    jumanpp = Jumanpp()
    sents = jumanpp.batch_apply(texts)
    assert [sent.text for sent in sents] == texts

    # parallel
    sents = jumanpp.batch_apply(texts, processes=2)
    assert [sent.text for sent in sents] == texts

    sents = jumanpp.batch_apply(texts, processes=4)
    assert [sent.text for sent in sents] == texts


def test_jumanpp_batch_apply_to_documents() -> None:
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    jumanpp = Jumanpp()
    docs = jumanpp.batch_apply_to_documents(texts)
    assert [doc.text for doc in docs] == texts

    # parallel
    docs = jumanpp.batch_apply_to_documents(texts, processes=2)
    assert [doc.text for doc in docs] == texts

    docs = jumanpp.batch_apply_to_documents(texts, processes=4)
    assert [doc.text for doc in docs] == texts


def test_jumanpp_normal() -> None:
    jumanpp = Jumanpp()
    text = "この文を解析してください。"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 7
    assert "".join(m.text for m in sent.morphemes) == text


def test_jumanpp_nominalization() -> None:
    jumanpp = Jumanpp()
    text = "音の響きを感じる。"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 6
    assert "".join(m.text for m in sent.morphemes) == text
    assert sent.morphemes[2].surf == "響き"
    assert sent.morphemes[2].pos == "名詞"


def test_jumanpp_whitespace() -> None:
    jumanpp = Jumanpp()
    text = "半角 スペース"
    sent = jumanpp.apply(text)
    assert len(sent.morphemes) == 3
    assert "".join(m.text for m in sent.morphemes) == text.replace(" ", "　")
    assert sent.morphemes[1].pos == "特殊"
    assert sent.morphemes[1].subpos == "空白"


def test_jumanpp_is_available() -> None:
    jumanpp = Jumanpp()
    assert jumanpp.is_available() is True

    jumanpp = Jumanpp("jumanp")
    assert jumanpp.is_available() is False


def test_jumanpp_repr() -> None:
    jumanpp = Jumanpp(options=["--juman"], senter=RegexSenter())
    assert repr(jumanpp) == "Jumanpp(executable='jumanpp', options=['--juman'], senter=RegexSenter())"
