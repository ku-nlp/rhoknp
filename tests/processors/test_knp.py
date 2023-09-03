import concurrent.futures

import pytest

from rhoknp import KNP, Document, Jumanpp, RegexSenter, Sentence

is_knp_available = KNP().is_available()


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_call() -> None:
    jumanpp = Jumanpp()
    knp = KNP()
    text = "外国人参政権"
    sentence = Sentence.from_raw_text(text)
    document = Document.from_raw_text(text)
    assert isinstance(knp(text), Document)
    assert isinstance(knp(sentence), Sentence)
    assert isinstance(knp(document), Document)

    assert isinstance(knp(jumanpp(text)), Document)
    assert isinstance(knp(jumanpp(sentence)), Sentence)
    assert isinstance(knp(jumanpp(document)), Document)

    assert isinstance(knp(knp(text)), Document)
    assert isinstance(knp(knp(sentence)), Sentence)
    assert isinstance(knp(knp(document)), Document)

    with pytest.raises(TypeError):
        knp(1)  # type: ignore


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_apply() -> None:
    jumanpp = Jumanpp()
    knp = KNP()
    text = "外国人参政権"
    sentence = Sentence.from_raw_text(text)
    document = Document.from_raw_text(text)
    assert isinstance(knp.apply(text), Document)
    assert isinstance(knp.apply(sentence), Sentence)
    assert isinstance(knp.apply(document), Document)

    assert isinstance(knp.apply(jumanpp.apply(text)), Document)
    assert isinstance(knp.apply(jumanpp.apply(sentence)), Sentence)
    assert isinstance(knp.apply(jumanpp.apply(document)), Document)

    assert isinstance(knp.apply(knp.apply(text)), Document)
    assert isinstance(knp.apply(knp.apply(sentence)), Sentence)
    assert isinstance(knp.apply(knp.apply(document)), Document)

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


def test_timeout_error() -> None:
    jumanpp = Jumanpp("tests/bin/jumanpp-mock.sh", skip_sanity_check=True, debug=True)
    knp = KNP("tests/bin/knp-mock.sh", jumanpp=jumanpp, skip_sanity_check=True, debug=True)
    with pytest.raises(TimeoutError):
        _ = knp.apply_to_sentence("knp time consuming input", timeout=1)


def test_runtime_error() -> None:
    jumanpp = Jumanpp("tests/bin/jumanpp-mock.sh", skip_sanity_check=True, debug=True)
    knp = KNP("tests/bin/knp-mock.sh", jumanpp=jumanpp, skip_sanity_check=True, debug=True)
    with pytest.raises(RuntimeError):
        _ = knp.apply_to_sentence("knp error causing input", timeout=1)


@pytest.mark.skipif(not is_knp_available, reason="KNP is not available")
def test_runtime_error2() -> None:
    knp = KNP()
    inp = "2001年1月15日に英語版が発足、その後多くの言語へ展開し、2021年12月29日時点では325言語で執筆が行われている[18]。100万記事以上に達しているものは18言語、10万記事以上に達しているものは71言語となっている[18]。ウィキペディアは多言語展開に力を入れており、各言語プロジェクト間の格差を少しでも埋めるためのソフトウェアの開発をスタンフォード大学と共同で行うこともあった[19]。2001年1月15日に英語版が発足、その後多くの言語へ展開し、2021年12月29日時点では325言語で執筆が行われている[18]。100万記事以上に達しているものは18言語、10万記事以上に達しているものは71言語となっている[18]。ウィキペディアは多言語展開に力を入れており、各言語プロジェクト間 の格差を少しでも埋めるためのソフトウェアの開発をスタンフォード大学と共同で行うこともあった[19]。2001年1月15日に英語版が発足、その後多くの言語へ展開し、2021年12月29日時点では325言語で執筆が行われている[18]。100万記事以上に達しているものは18言語、10万記事以上に達しているものは71言語となっている[18]。ウィキペディアは多言語展開に力を入れており、各言語プロジェクト間の格差を少しでも埋めるためのソフトウェアの開発をスタンフォード 大学と共同で行うこともあった[19]。2001年1月15日に英語版が発足、その後多くの言語へ展開し、2021年12月29日時点では325言語で執筆が行われている[18]。100万記事以上に達しているものは18言語、10万記事以上に達しているものは71言語となっている[18]。ウィキペディアは多言語展開に力を入れており、各言語プロジェクト間の格差を少しでも埋めるためのソフトウェアの開発をスタンフォード大学と共同で行うこともあった[19]。2001年1月15日に英語版が発足、その後多くの言語へ展開し、2021年12月29日時点では325言語で執筆が行われている[18]。"
    with pytest.raises(RuntimeError):
        _ = knp.apply_to_sentence(inp)


def test_invalid_option() -> None:
    with pytest.raises(ValueError):
        _ = KNP(options=["--anaphora"])


def test_repr() -> None:
    knp = KNP(options=["-tab"], senter=RegexSenter(), jumanpp=Jumanpp())
    assert (
        repr(knp)
        == "KNP(executable='knp', options=['-tab'], senter=RegexSenter(), jumanpp=Jumanpp(executable='jumanpp'))"
    )
