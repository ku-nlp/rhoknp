from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Union

import fastapi
import fastapi.staticfiles
import fastapi.templating
import uvicorn
from spacy.displacy import render

from rhoknp import Document
from rhoknp.cli.show import draw_tree
from rhoknp.processors import KNP, KWJA, Jumanpp

here = Path(__file__).parent


class AnalyzerType(Enum):
    """解析器の種類．"""

    JUMANPP = "jumanpp"
    KNP = "knp"
    KWJA = "kwja"


def _draw_tree(document: Document, show_rel: bool = False, show_pas: bool = False) -> str:
    """rhoknp.cli.show.draw_tree の wrapper．

    Args:
        document: 解析結果．

    Returns:
        構文木．
    """
    with StringIO() as buffer:
        for sentence in document.sentences:
            draw_tree(sentence.base_phrases, buffer, show_rel=show_rel, show_pas=show_pas)
        return buffer.getvalue()


def _get_ner_svg(document: Document) -> str:
    """NER の結果を spacy.displacy.render で SVG に変換．

    Args:
        document: 解析結果．

    Returns:
        NER の SVG 画像．
    """
    text = document.text
    ents = []
    for named_entity in document.named_entities:
        start, _ = named_entity.morphemes[0].global_span
        _, end = named_entity.morphemes[-1].global_span
        label = named_entity.category.value
        ents.append({"start": start, "end": end, "label": label})
    options = {
        "colors": {
            "ORGANIZATION": "#7aecec",
            "PERSON": "#aa9cfc",
            "LOCATION": "#ff9561",
            "ARTIFACT": "#bfeeb7",
            "DATE": "#bfe1d9",
            "TIME": "#bfe1d9",
            "MONEY": "#e4e7d2",
            "PERCENT": "#e4e7d2",
        }
    }
    return render({"text": text, "ents": ents, "title": None}, style="ent", options=options, manual=True)


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
    templates.env.globals["get_ner_svg"] = _get_ner_svg

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
