import json
import sys
from pathlib import Path
from typing import List, Optional

import typer
import yaml

from rhoknp import Document, __version__
from rhoknp.cli.cat import print_document
from rhoknp.cli.serve import AnalyzerType, serve_analyzer
from rhoknp.cli.show import draw_tree
from rhoknp.cli.stats import get_document_statistics

app = typer.Typer(help="rhoknp CLI utilities.")


def version_callback(value: bool) -> None:
    """バージョンを表示．

    Args:
        value: True ならバージョンを表示してプログラムを終了．
    """
    if value:
        print(f"rhoknp version: {__version__}")
        raise typer.Exit


@app.callback()
def main(
    _: bool = typer.Option(False, "--version", "-v", callback=version_callback, help="Show version and exit."),
) -> None:
    """CLI のメイン関数．"""


@app.command(help="Print KNP files with syntax highlighting.")
def cat(
    knp_path: Optional[Path] = typer.Argument(None, exists=True, dir_okay=False, help="Path to knp file to show."),
    dark: bool = typer.Option(False, "--dark", "-d", help="Use dark background."),
) -> None:
    """KNP ファイルを色付きで表示．

    Args:
        knp_path: KNP ファイルのパス．
        dark: True なら背景を黒にする．
    """
    knp_text = sys.stdin.read() if knp_path is None else knp_path.read_text()
    doc = Document.from_knp(knp_text)
    print_document(doc, is_dark=dark)


@app.command(help="Convert a KNP file into raw text, Juman++ format, or KNP format.")
def convert(
    knp_path: Optional[Path] = typer.Argument(
        None, exists=True, dir_okay=False, help="Path to knp file to convert. If not given, read from stdin"
    ),
    format_: str = typer.Option("text", "--format", "-f", help="Format to convert to."),
) -> None:
    """KNP ファイルを種々のフォーマットに変換．

    Args:
        knp_path: KNP ファイルのパス．
        format_: 変換先のフォーマット．"text", "jumanpp", "knp" のいずれか．
    """
    knp_text = sys.stdin.read() if knp_path is None else knp_path.read_text()
    doc = Document.from_knp(knp_text)
    if format_ == "text":
        print(doc.text)
    elif format_ == "jumanpp":
        print(doc.to_jumanpp(), end="")
    elif format_ == "knp":
        print(doc.to_knp(), end="")
    else:
        raise ValueError(f"Unknown format: {format_}")


@app.command(help="Print given file content in tree format.")
def show(
    knp_path: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to knp file to show"),
    pos: bool = typer.Option(False, "--pos", "-p", help="Show POS characters."),
    rel: bool = typer.Option(False, "--rel", "-r", help="Show contents of <rel> tags."),
    pas: bool = typer.Option(False, "--pas", help="Show predicate-argument structures."),
) -> None:
    """KNP ファイルを読み込み係り受けを可視化．

    Args:
        knp_path: KNP ファイルのパス．
        pos: True なら同時に品詞を表示．
        rel: True なら同時に <rel> タグの内容を表示．
        pas: True なら同時に述語項構造を表示．
    """
    doc = Document.from_knp(knp_path.read_text())
    for sent in doc.sentences:
        print(sent.comment)
        draw_tree(sent.base_phrases, show_pos=pos, show_rel=rel, show_pas=pas)


@app.command(help="Show statistics of given KNP file.")
def stats(
    knp_path: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Path to knp file to calculate statistics on."
    ),
    use_json: bool = typer.Option(False, "--json", "-j", help="Output statistics in JSON format."),
) -> None:
    """KNP ファイルを読み込みその統計情報を出力．

    Args:
        knp_path: KNP ファイルのパス．
        use_json: JSON 形式で出力．
    """
    doc = Document.from_knp(knp_path.read_text())
    doc_stats = get_document_statistics(doc)
    if use_json:
        print(json.dumps(doc_stats, ensure_ascii=False, indent=4))
    else:
        print(yaml.dump(doc_stats, allow_unicode=True, sort_keys=False), end="")


@app.command(help="Serve an analyzer as HTTP server.")
def serve(
    analyzer: AnalyzerType = typer.Argument(..., help="Analyzer to use. Choose from jumanpp, knp, kwja."),
    host: str = typer.Option("localhost", "--host", "-h", help="Host to listen on."),
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on."),
    base_url: str = typer.Option("/", "--base-url", help="Root path of the server."),
    analyzer_args: Optional[List[str]] = typer.Argument(None, help="Additional arguments for the analyzer."),
) -> None:
    """解析器を起動し，HTTP サーバとして提供．

    Args:
        analyzer: 解析器の種類．
        host: ホスト．
        port: ポート．
        base_url: ベース URL．
        analyzer_args: 解析器のオプション．
    """
    serve_analyzer(analyzer, host, port, base_url, analyzer_args)  # pragma: no cover


if __name__ == "__main__":
    app()
