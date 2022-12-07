import html
import textwrap
from enum import Enum
from typing import Optional, Union

try:
    import fastapi
    import uvicorn
except ImportError:
    fastapi = None
    uvicorn = None

from rhoknp.processors import KNP, KWJA, Jumanpp


class AnalyzerType(Enum):
    """解析器の種類．"""

    JUMANPP = "jumanpp"
    KNP = "knp"
    KWJA = "kwja"


BASE_TEMPLATE = textwrap.dedent(
    """\
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
            integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
            crossorigin="anonymous"
        >
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand" href="#">{title}</a>
            </div>
        </nav>
        <div class="container mt-3">
            <div class="row">
                <div class="col">
                    <form>
                        <div>
                            <label for="text" class="form-label">テキスト</label>
                            <textarea class="form-control" id="text" name="text" rows="3" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-outline-primary mt-3">解析</button>
                    </form>
                </div>
            </div>
        </div>
        {result}
    </body>
    </html>
    """
)

RESULT_TEMPLATE = textwrap.dedent(
    """\
    <div class="container mt-3">
        <hr>
        <div class="row">
            <div class="col">
                <h6>テキスト</h6>
                <pre>{text}</pre>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <h6>解析結果</h6>
                <pre>{result}</pre>
            </div>
        </div>
    </div>
    """
)


def create_app(analyzer: AnalyzerType) -> "fastapi.FastAPI":
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
    """
    if fastapi is None:
        raise ImportError("fastapi is required to run the server. Install it with `pip install rhoknp[serve]`.")

    processor: Optional[Union[Jumanpp, KNP, KWJA]] = None
    if analyzer == AnalyzerType.JUMANPP:
        processor = Jumanpp()
    elif analyzer == AnalyzerType.KNP:
        processor = KNP()
    elif analyzer == AnalyzerType.KWJA:
        processor = KWJA()
    else:
        raise AssertionError  # unreachable

    app = fastapi.FastAPI()

    def get_result(text: str) -> str:
        if text == "":
            return ""
        assert processor is not None
        document = processor.apply(text)
        if analyzer == AnalyzerType.JUMANPP:
            return document.to_jumanpp()
        else:
            return document.to_knp()

    @app.get("/", response_class=fastapi.responses.HTMLResponse)
    async def index(text: str = ""):
        if analyzer == AnalyzerType.JUMANPP:
            title = "Juman++ Demo"
        elif analyzer == AnalyzerType.KNP:
            title = "KNP Demo"
        elif analyzer == AnalyzerType.KWJA:
            title = "KWJA Demo"
        else:
            raise AssertionError  # unreachable
        if text == "":
            return BASE_TEMPLATE.format(title=title, result="")
        else:
            result = get_result(text)
            return BASE_TEMPLATE.format(
                title=title,
                result=RESULT_TEMPLATE.format(
                    text=html.escape(text),
                    result=html.escape(result),
                ),
            )

    @app.get("/analyze", response_class=fastapi.responses.JSONResponse)
    async def analyze(text: str = ""):
        return {"text": text, "result": get_result(text)}

    return app


def serve_analyzer(analyzer: AnalyzerType, host: str, port: int) -> None:
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
        host: ホスト．
        port: ポート．
    """
    if uvicorn is None:
        raise ImportError("uvicorn is required to run the server. Install it with `pip install rhoknp[serve]`.")

    app = create_app(analyzer)
    config = uvicorn.Config(app, host=host, port=port)
    server = uvicorn.Server(config)
    server.run()
