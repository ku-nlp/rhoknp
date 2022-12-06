from enum import Enum
from typing import Dict, Optional, Union

try:
    import fastapi
    import uvicorn
except ImportError:
    fastapi = None
    uvicorn = None

from rhoknp.processors import KNP, KWJA, Jumanpp


class AnalyzerType(Enum):
    """解析器の種類．"""

    jumanpp = "jumanpp"
    knp = "knp"
    kwja = "kwja"


def create_app(analyzer: AnalyzerType) -> "fastapi.FastAPI":
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
    """
    if fastapi is None:
        raise ImportError("fastapi is required to run the server. Install it with `pip install fastapi`.")

    processor: Optional[Union[Jumanpp, KNP, KWJA]] = None
    if analyzer == AnalyzerType.jumanpp:
        processor = Jumanpp()
    elif analyzer == AnalyzerType.knp:
        processor = KNP()
    elif analyzer == AnalyzerType.kwja:
        processor = KWJA()
    else:
        raise AssertionError  # unreachable

    app = fastapi.FastAPI()

    def get_result(text: str) -> Dict[str, str]:
        if text == "":
            return {"text": text, "result": ""}

        assert processor is not None
        document = processor.apply(text)
        if document.need_knp is False:
            return {"text": text, "result": document.to_knp()}
        else:
            return {"text": text, "result": document.to_jumanpp()}

    @app.get("/")
    async def index(text: str = ""):
        return get_result(text)  # TODO: Return HTML

    @app.get("/analyze")
    async def analyze(text: str = ""):
        return get_result(text)

    return app


def serve_analyzer(analyzer: AnalyzerType, host: str, port: int) -> None:
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
        host: ホスト．
        port: ポート．
    """
    if uvicorn is None:
        raise ImportError("uvicorn is required to run the server. Install it with `pip install uvicorn`.")

    app = create_app(analyzer)
    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config)
    server.run()
