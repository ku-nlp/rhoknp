import pytest

from rhoknp import Jumanpp


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
def test_jumanpp_apply(text: str):
    jumanpp = Jumanpp()
    document = jumanpp.apply(text)
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
def test_jumanpp_apply_to_sentence(text: str):
    jumanpp = Jumanpp()
    sentence = jumanpp.apply_to_sentence(text)
    assert sentence.text == text.replace(" ", "　").replace('"', "”")


def test_jumanpp_batch_apply():
    texts = [
        "外国人参政権",
        "望遠鏡で泳いでいる少女を見た。",
        "エネルギーを素敵にENEOS",
    ]
    jumanpp = Jumanpp()
    documents = jumanpp.batch_apply(texts)
    assert [document.text for document in documents] == texts

    # parallel
    documents = jumanpp.batch_apply(texts, processes=2)
    assert [document.text for document in documents] == texts

    documents = jumanpp.batch_apply(texts, processes=4)
    assert [document.text for document in documents] == texts


def test_jumanpp_normal():
    jumanpp = Jumanpp()
    text = "この文を解析してください。"
    document = jumanpp.apply(text)
    assert len(document.morphemes) == 7
    assert "".join(m.text for m in document.morphemes) == text


def test_jumanpp_nominalization():
    jumanpp = Jumanpp()
    text = "音の響きを感じる。"
    document = jumanpp.apply(text)
    assert len(document.morphemes) == 6
    assert "".join(m.text for m in document.morphemes) == text
    assert document.morphemes[2].surf == "響き"
    assert document.morphemes[2].pos == "名詞"


def test_jumanpp_whitespace():
    jumanpp = Jumanpp()
    text = "半角 スペース"
    document = jumanpp.apply(text)
    assert len(document.morphemes) == 3
    assert "".join(m.text for m in document.morphemes) == text.replace(" ", "　")
    assert document.morphemes[1].pos == "特殊"
    assert document.morphemes[1].subpos == "空白"
