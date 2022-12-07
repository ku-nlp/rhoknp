import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from rhoknp import Document
from rhoknp.cli.serve import AnalyzerType, create_app


@pytest.mark.parametrize(
    "analyzer",
    [AnalyzerType.JUMANPP, AnalyzerType.KNP, AnalyzerType.KWJA],
)
def test_create_app(analyzer: AnalyzerType) -> None:
    app = create_app(analyzer)
    assert isinstance(app, FastAPI)


def test_analyze_jumanpp():
    app = create_app(AnalyzerType.JUMANPP)
    client = TestClient(app)
    response = client.get("/analyze", params={"text": "こんにちは"})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_jumanpp(json["result"])
    assert document.text == "こんにちは"


def test_analyze_knp():
    app = create_app(AnalyzerType.KNP)
    client = TestClient(app)
    response = client.get("/analyze", params={"text": "こんにちは"})
    assert response.status_code == 200
    json = response.json()
    assert "text" in json
    assert "result" in json
    document = Document.from_knp(json["result"])
    assert document.text == "こんにちは"


def test_index_jumanpp():
    app = create_app(AnalyzerType.JUMANPP)
    client = TestClient(app)
    response = client.get("/", params={"text": "こんにちは"})
    assert response.status_code == 200


def test_index_knp():
    app = create_app(AnalyzerType.KNP)
    client = TestClient(app)
    response = client.get("/", params={"text": "こんにちは"})
    assert response.status_code == 200
