import html
import textwrap
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


BASE = textwrap.dedent(
    """\
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>rhoknp</title>
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
                <a class="navbar-brand" href="#">rhoknp</a>
            </div>
        </nav>
        <div class="container mt-3">
            <div class="row">
                <div class="col">
                    <form>
                        <div>
                            <label for="text" class="form-label">テキスト</label>
                            <textarea class="form-control" id="text" name="text" rows="3"></textarea>
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

    @app.get("/", response_class=fastapi.responses.HTMLResponse)
    async def index(text: str = ""):
        if text == "":
            return BASE.format(result="")
        else:
            result = get_result(text)
            return BASE.format(
                result=RESULT_TEMPLATE.format(
                    text=html.escape(text),
                    result=html.escape(result["result"]),
                )
            )

    @app.get("/analyze", response_class=fastapi.responses.JSONResponse)
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
