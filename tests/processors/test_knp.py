import concurrent.futures

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
def test_apply(text: str) -> None:
    knp = KNP(options=["-tab"])
    doc = knp.apply(text)
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
def test_apply_to_sentence(text: str) -> None:
    knp = KNP(options=["-tab"])
    sent = knp.apply_to_sentence(text)
    assert sent.text == text.replace(" ", "　").replace('"', "”")


def test_thread_safe() -> None:
    knp = KNP(options=["-tab"])
    texts = ["外国人参政権", "望遠鏡で泳いでいる少女を見た。", "エネルギーを素敵にENEOS"]
    texts *= 10
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(knp.apply_to_sentence, text) for text in texts]
        for i, future in enumerate(futures):
            sentence = future.result()
            assert sentence.text == texts[i]


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
def test_apply_to_document(text: str) -> None:
    knp = KNP()
    doc = knp.apply_to_document(text)
    assert doc.text == text.replace(" ", "　").replace('"', "”")


def test_is_available() -> None:
    knp = KNP()
    assert knp.is_available() is True

    knp = KNP("knpp")
    assert knp.is_available() is False


def test_repr() -> None:
    jumanpp = KNP(options=["--tab"], senter=RegexSenter(), jumanpp=Jumanpp())
    assert (
        repr(jumanpp)
        == "KNP(executable='knp', options=['--tab'], senter=RegexSenter(), jumanpp=Jumanpp(executable='jumanpp'))"
    )
