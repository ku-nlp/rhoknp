import pytest

from rhoknp import KWJA


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
def test_kwja_apply(text: str) -> None:
    kwja = KWJA(options=["--text"])
    sent = kwja.apply(text)
    assert sent.text == text.replace(" ", "　").replace('"', "”")


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
def test_kwja_apply_to_document(text: str) -> None:
    kwja = KWJA(options=["--text"])
    doc = kwja.apply_to_document(text)
    assert doc.text == text.replace(" ", "　").replace('"', "”")


def test_kwja_batch_apply() -> None:
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    kwja = KWJA()
    sents = kwja.batch_apply(texts)
    assert [sent.text for sent in sents] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    # parallel
    sents = kwja.batch_apply(texts, processes=2)
    assert [sent.text for sent in sents] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    sents = kwja.batch_apply(texts, processes=4)
    assert [sent.text for sent in sents] == [text.replace(" ", "　").replace('"', "”") for text in texts]


def test_kwja_batch_apply_to_documents() -> None:
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    kwja = KWJA()
    docs = kwja.batch_apply_to_documents(texts)
    assert [doc.text for doc in docs] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    # parallel
    docs = kwja.batch_apply_to_documents(texts, processes=2)
    assert [doc.text for doc in docs] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    docs = kwja.batch_apply_to_documents(texts, processes=4)
    assert [doc.text for doc in docs] == [text.replace(" ", "　").replace('"', "”") for text in texts]


def test_kwja_is_available() -> None:
    pass  # TODO


def test_kwja_repr() -> None:
    kwja = KWJA(options=["--text"])
    assert repr(kwja) == "KWJA(executable='kwja', options=['--text'])"
