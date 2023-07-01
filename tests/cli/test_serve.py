import textwrap
from typing import Generator, List

import pytest
from fastapi.testclient import TestClient

from rhoknp import Document
from rhoknp.cli.serve import AnalyzerType, _draw_tree, _get_entity_spans, _get_string_diff, _Span, create_app


@pytest.fixture
def jumanpp_client() -> Generator[TestClient, None, None]:
    app = create_app(AnalyzerType.JUMANPP)
    yield TestClient(app)


@pytest.mark.parametrize("text", ["こんにちは"])
def test_analyze_jumanpp(jumanpp_client: TestClient, text: str) -> None:
    response = jumanpp_client.get("/analyze", params={"text": text})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_jumanpp(json["result"])
    assert document.text == text


def test_analyze_jumanpp_error_empty(jumanpp_client: TestClient) -> None:
    error_causing_text = ""
    response = jumanpp_client.get("/analyze", params={"text": error_causing_text})
    assert response.status_code == 400
    json = response.json()
    assert "error" in json
    assert json["error"]["code"] == 400
    assert json["error"]["message"] == "text is empty"


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_index_jumanpp(jumanpp_client: TestClient, text: str) -> None:
    response = jumanpp_client.get("/", params={"text": text})
    assert response.status_code == 200


@pytest.fixture
def knp_client() -> Generator[TestClient, None, None]:
    app = create_app(AnalyzerType.KNP)
    yield TestClient(app)


@pytest.mark.parametrize("text", ["こんにちは"])
def test_analyze_knp(knp_client: TestClient, text: str) -> None:
    response = knp_client.get("/analyze", params={"text": text})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_knp(json["result"])
    assert document.text == text


def test_analyze_knp_error_empty(knp_client: TestClient) -> None:
    error_causing_text = ""
    response = knp_client.get("/analyze", params={"text": error_causing_text})
    assert response.status_code == 400
    json = response.json()
    assert "error" in json
    assert json["error"]["code"] == 400
    assert json["error"]["message"] == "text is empty"


def test_analyze_knp_error_long(knp_client: TestClient) -> None:
    error_causing_text = "http://localhost:8000" * 30
    response = knp_client.get("/analyze", params={"text": error_causing_text})
    assert response.status_code == 500
    json = response.json()
    assert "error" in json
    assert json["error"]["code"] == 500
    assert json["error"]["message"] == "malformed phrase line: "


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_index_knp(knp_client: TestClient, text: str) -> None:
    response = knp_client.get("/", params={"text": text})
    assert response.status_code == 200


def test_index_knp_error(knp_client: TestClient) -> None:
    error_causing_text = "http://localhost:8000" * 30
    response = knp_client.get("/", params={"text": error_causing_text})
    assert response.status_code == 500


# KWJA is tested in `tests/processors/test_kwja.py` to isolate tests that require KWJA installed.


@pytest.mark.parametrize(
    "pre_text, post_text, expected",
    [
        ("あ", "あ", [_Span("あ", "=")]),
        ("あ", "い", [_Span("あ", "-"), _Span("い", "+")]),
        ("あい", "あ", [_Span("あ", "="), _Span("い", "-")]),
        ("あ", "あい", [_Span("あ", "="), _Span("い", "+")]),
        ("人口知能", "人工知能", [_Span("人", "="), _Span("口", "-"), _Span("工", "+"), _Span("知能", "=")]),
        ("", "", [_Span("", "=")]),
    ],
)
def test_get_string_diff(pre_text: str, post_text: str, expected: List[_Span]) -> None:
    assert _get_string_diff(pre_text, post_text) == expected


def test_draw_tree() -> None:
    knp_text = textwrap.dedent(
        textwrap.dedent(
            """\
            # S-ID:001-0-0
            * 1D
            + 1D
            クロール くろーる クロール 名詞 6 普通名詞 1 * 0 * 0 "代表表記:クロール/くろーる カテゴリ:抽象物 ドメイン:スポーツ"
            で で で 助詞 9 格助詞 1 * 0 * 0 "代表表記:で/で"
            * 3D
            + 3D
            泳いで およいで 泳ぐ 動詞 2 * 0 子音動詞ガ行 4 タ系連用テ形 14 "代表表記:泳ぐ/およぐ"
            いる いる いる 接尾辞 14 動詞性接尾辞 7 母音動詞 1 基本形 2 "代表表記:いる/いる"
            * 3P
            + 3P
            太郎 たろう 太郎 名詞 6 人名 5 * 0 * 0 "代表表記:太郎/たろう 人名:日本:名:45:0.00106"
            と と と 助詞 9 格助詞 1 * 0 * 0 "代表表記:と/と"
            * 4D
            + 4D
            次郎 じろう 次郎 名詞 6 人名 5 * 0 * 0 "代表表記:次郎/じろう 人名:日本:名:135:0.00068"
            を を を 助詞 9 格助詞 1 * 0 * 0 "代表表記:を/を"
            * -1D
            + -1D
            見た みた 見る 動詞 2 * 0 母音動詞 1 タ形 10 "代表表記:見る/みる 補文ト 自他動詞:自:見える/みえる"
            。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
            EOS
            """
        )
    )
    document = Document.from_knp(knp_text)
    _ = _draw_tree(document)


def test_get_entity_spans() -> None:
    knp_text = textwrap.dedent(
        """\
        # S-ID:0
        * 1D
        + 1D
        お お お 接頭辞 13 名詞接頭辞 1 * 0 * 0 "代表表記:御/お"
        会計 かいけい 会計 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:会計/かいけい カテゴリ:抽象物 ドメイン:ビジネス"
        は は は 助詞 9 副助詞 2 * 0 * 0 "代表表記:は/は"
        * -1D
        + -1D <NE:MONEY:108円>
        108 ひゃくはち 108 名詞 6 数詞 7 * 0 * 0
        円 えん 円 接尾辞 14 名詞性名詞助数辞 3 * 0 * 0 "代表表記:円/えん 準内容語"
        で で だ 判定詞 4 * 0 判定詞 25 ダ列タ系連用テ形 12 "代表表記:だ/だ"
        ございます ございます ございます 接尾辞 14 動詞性接尾辞 7 動詞性接尾辞ます型 31 基本形 2 "代表表記:御座います/ございます"
        。 。 。 特殊 1 句点 1 * 0 * 0 "代表表記:。/。"
        EOS
        """
    )
    document = Document.from_knp(knp_text)
    assert _get_entity_spans(document) == [_Span("お会計は", None), _Span("108円", "MONEY"), _Span("でございます。", None)]
