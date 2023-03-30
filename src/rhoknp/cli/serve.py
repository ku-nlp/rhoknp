from enum import Enum
from pathlib import Path
from typing import Union

import fastapi
import fastapi.staticfiles
import fastapi.templating
import uvicorn

from rhoknp.processors import KNP, KWJA, Jumanpp

here = Path(__file__).parent


class AnalyzerType(Enum):
    """解析器の種類．"""

    JUMANPP = "jumanpp"
    KNP = "knp"
    KWJA = "kwja"


def create_app(analyzer: AnalyzerType, *args, **kwargs) -> "fastapi.FastAPI":
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
        args: 解析器のオプション．
        kwargs: 解析器のオプション．
    """
    processor: Union[Jumanpp, KNP, KWJA]
    if analyzer == AnalyzerType.JUMANPP:
        processor = Jumanpp(*args, **kwargs)
    elif analyzer == AnalyzerType.KNP:
        processor = KNP(*args, **kwargs)
    elif analyzer == AnalyzerType.KWJA:
        processor = KWJA(*args, **kwargs)
    else:
        raise AssertionError  # unreachable

    app = fastapi.FastAPI()
    app.mount("/static", fastapi.staticfiles.StaticFiles(directory=here.joinpath("static")), name="static")

    templates = fastapi.templating.Jinja2Templates(directory=here.joinpath("templates"))

    def get_result(text: str) -> str:
        if text == "":
            return ""
        document = processor.apply(text)
        if analyzer == AnalyzerType.JUMANPP:
            return document.to_jumanpp()
        else:
            return document.to_knp()

    @app.get("/", response_class=fastapi.responses.HTMLResponse)
    async def index(request: fastapi.Request, text: str = ""):
        if analyzer == AnalyzerType.JUMANPP:
            title = "Juman++ Demo"
        elif analyzer == AnalyzerType.KNP:
            title = "KNP Demo"
        elif analyzer == AnalyzerType.KWJA:
            title = "KWJA Demo"
        else:
            raise AssertionError  # unreachable
        if text == "":
            result = None
        else:
            result = {"text": text, "result": get_result(text)}
        return templates.TemplateResponse("index.jinja2", {"request": request, "title": title, "result": result})

    @app.get("/analyze", response_class=fastapi.responses.JSONResponse)
    async def analyze(text: str = ""):
        return {"text": text, "result": get_result(text)}

    return app


def serve_analyzer(analyzer: AnalyzerType, host: str, port: int) -> None:  # pragma: no cover
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
        host: ホスト．
        port: ポート．
    """
    app = create_app(analyzer)
    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config)
    server.run()
