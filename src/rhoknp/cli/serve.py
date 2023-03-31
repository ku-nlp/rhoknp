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
    title: str
    template_name: str
    version: str
    if analyzer == AnalyzerType.JUMANPP:
        title = "Juman++ Demo"
        template_name = "jumanpp.jinja2"
        processor = Jumanpp(*args, **kwargs)
    elif analyzer == AnalyzerType.KNP:
        title = "KNP Demo"
        template_name = "knp.jinja2"
        processor = KNP(*args, **kwargs)
    elif analyzer == AnalyzerType.KWJA:
        title = "KWJA Demo"
        template_name = "kwja.jinja2"
        processor = KWJA(*args, **kwargs)
    else:
        raise AssertionError  # unreachable
    version = processor.get_version()

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
        if text == "":
            result = None
        else:
            result = {"text": text, "result": get_result(text)}
        return templates.TemplateResponse(
            template_name, {"request": request, "title": title, "version": version, "result": result}
        )

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
