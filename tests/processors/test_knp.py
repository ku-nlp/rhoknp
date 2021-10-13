import pytest

from rhoknp import KNP, Jumanpp, RegexSenter


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
def test_knp_apply(text: str):
    knp = KNP()
    sent = knp.apply(text)
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
def test_knp_apply_to_document(text: str):
    knp = KNP()
    doc = knp.apply_to_document(text)
    assert doc.text == text.replace(" ", "　").replace('"', "”")


def test_knp_batch_apply():
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    knp = KNP()
    sents = knp.batch_apply(texts)
    assert [sent.text for sent in sents] == [
        text.replace(" ", "　").replace('"', "”") for text in texts
    ]

    # parallel
    sents = knp.batch_apply(texts, processes=2)
    assert [sent.text for sent in sents] == [
        text.replace(" ", "　").replace('"', "”") for text in texts
    ]

    sents = knp.batch_apply(texts, processes=4)
    assert [sent.text for sent in sents] == [
        text.replace(" ", "　").replace('"', "”") for text in texts
    ]


def test_knp_batch_apply_to_documents():
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    knp = KNP()
    docs = knp.batch_apply_to_documents(texts)
    assert [doc.text for doc in docs] == [
        text.replace(" ", "　").replace('"', "”") for text in texts
    ]

    # parallel
    docs = knp.batch_apply_to_documents(texts, processes=2)
    assert [doc.text for doc in docs] == [
        text.replace(" ", "　").replace('"', "”") for text in texts
    ]

    docs = knp.batch_apply_to_documents(texts, processes=4)
    assert [doc.text for doc in docs] == [
        text.replace(" ", "　").replace('"', "”") for text in texts
    ]


def test_knp_is_available():
    knp = KNP()
    assert knp.is_available() is True

    knp = KNP("knpp")
    assert knp.is_available() is False


def test_knp_repr():
    jumanpp = KNP(options=["--tab"], senter=RegexSenter(), jumanpp=Jumanpp())
    assert (
        repr(jumanpp)
        == "KNP(executable='knp', options=['--tab'], senter=RegexSenter(), jumanpp=Jumanpp(executable='jumanpp'))"
    )
