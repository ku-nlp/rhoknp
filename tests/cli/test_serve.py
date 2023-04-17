from typing import Generator

import pytest
from fastapi.testclient import TestClient

from rhoknp import Document
from rhoknp.cli.serve import AnalyzerType, create_app


@pytest.fixture()
def jumanpp_client() -> Generator[TestClient, None, None]:
    app = create_app(AnalyzerType.JUMANPP)
    yield TestClient(app)


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_analyze_jumanpp(jumanpp_client: TestClient, text: str) -> None:
    response = jumanpp_client.get("/analyze", params={"text": text})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_jumanpp(json["result"])
    assert document.text == text


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_index_jumanpp(jumanpp_client: TestClient, text: str) -> None:
    response = jumanpp_client.get("/", params={"text": text})
    assert response.status_code == 200


@pytest.fixture()
def knp_client() -> Generator[TestClient, None, None]:
    app = create_app(AnalyzerType.KNP)
    yield TestClient(app)


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_analyze_knp(knp_client: TestClient, text: str) -> None:
    response = knp_client.get("/analyze", params={"text": text})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_knp(json["result"])
    assert document.text == text


@pytest.mark.parametrize("text", ["こんにちは", ""])
def test_index_knp(knp_client: TestClient, text: str) -> None:
    response = knp_client.get("/", params={"text": text})
    assert response.status_code == 200


# KWJA is tested in `tests/processors/test_kwja.py` to isolate tests that require KWJA installed.
