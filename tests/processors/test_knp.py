import pytest

from rhoknp import KNP, Document, Jumanpp


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
    jumanpp = Jumanpp()
    knp = KNP()
    document = knp.apply(jumanpp.apply(Document.from_sentence(text)))
    assert document.text == text.replace(" ", "　").replace('"', "”")


def test_knp_batch_apply():
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    documents = list(map(Document.from_sentence, texts))
    jumanpp = Jumanpp()
    knp = KNP()
    documents = knp.batch_apply(jumanpp.batch_apply(documents))
    assert [document.text for document in documents] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    # parallel
    documents = knp.batch_apply(jumanpp.batch_apply(documents), processes=2)
    assert [document.text for document in documents] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    documents = knp.batch_apply(jumanpp.batch_apply(documents), processes=4)
    assert [document.text for document in documents] == [text.replace(" ", "　").replace('"', "”") for text in texts]
