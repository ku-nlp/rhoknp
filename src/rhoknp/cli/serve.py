from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Union

import fastapi
import fastapi.staticfiles
import fastapi.templating
import uvicorn

from rhoknp import Document
from rhoknp.cli.show import draw_tree
from rhoknp.processors import KNP, KWJA, Jumanpp

here = Path(__file__).parent


class AnalyzerType(Enum):
    """解析器の種類．"""

    JUMANPP = "jumanpp"
    KNP = "knp"
    KWJA = "kwja"


def _draw_tree(document: Document) -> str:
    """rhoknp.cli.show.draw_tree の wrapper．

    Args:
        document: 解析結果．

    Returns:
        構文木．
    """
    with StringIO() as buffer:
        draw_tree(document.phrases, buffer)
        return buffer.getvalue()


def create_app(analyzer: AnalyzerType, *args, **kwargs) -> "fastapi.FastAPI":
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
        args: 解析器のオプション．
        kwargs: 解析器のオプション．
    """
    app = fastapi.FastAPI()
    app.mount("/static", fastapi.staticfiles.StaticFiles(directory=here.joinpath("static")), name="static")

    templates = fastapi.templating.Jinja2Templates(directory=here.joinpath("templates"))
    templates.env.globals["draw_tree"] = _draw_tree

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

    @app.get("/", response_class=fastapi.responses.HTMLResponse)
    async def index(request: fastapi.Request, text: str = ""):
        return templates.TemplateResponse(
            template_name,
            {
                "request": request,
                "title": title,
                "version": version,
                "text": text,
                "analyzed_document": None if text == "" else processor.apply(text),
            },
        )

    @app.get("/analyze", response_class=fastapi.responses.JSONResponse)
    async def analyze(text: str = ""):
        if text == "":
            result = ""
        else:
            document = processor.apply(text)
            if analyzer == AnalyzerType.JUMANPP:
                result = document.to_jumanpp()
            else:
                result = document.to_knp()
        return {"text": text, "result": result}

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
