import pytest

from rhoknp import KNP


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
    document = knp.apply(text)
    assert document.text == text.replace(" ", "　").replace('"', "”")


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
def test_knp_apply_to_sentence(text: str):
    knp = KNP()
    sentence = knp.apply_to_sentence(text)
    assert sentence.text == text.replace(" ", "　").replace('"', "”")


def test_knp_batch_apply():
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    knp = KNP()
    documents = knp.batch_apply(texts)
    assert [document.text for document in documents] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    # parallel
    documents = knp.batch_apply(texts, processes=2)
    assert [document.text for document in documents] == [text.replace(" ", "　").replace('"', "”") for text in texts]

    documents = knp.batch_apply(texts, processes=4)
    assert [document.text for document in documents] == [text.replace(" ", "　").replace('"', "”") for text in texts]
