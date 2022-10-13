import json
from pathlib import Path

import typer
import yaml

from rhoknp import Document, __version__
from rhoknp.utils.draw_tree import draw_tree
from rhoknp.utils.stats import get_document_statistics

app = typer.Typer(help="rhoknp CLI utilities.")


def version_callback(value: bool) -> None:
    """バージョンを表示．

    Args:
        value: True ならバージョンを表示してプログラムを終了．
    """
    if value:
        typer.echo(f"rhoknp version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    _: bool = typer.Option(False, "--version", "-v", callback=version_callback, help="Show version and exit."),
) -> None:
    """CLI のメイン関数．"""
    pass


@app.command(help="Print given file content in tree format.")
def show(
    knp_path: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to knp file to show"),
) -> None:
    """KNP ファイルを読み込み係り受けを可視化．

    Args:
        knp_path: KNP ファイルのパス．
    """
    doc = Document.from_knp(knp_path.read_text())
    for sent in doc.sentences:
        print(sent.comment)
        draw_tree(sent.base_phrases, show_pos=False)


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
        typer.echo(json.dumps(doc_stats, ensure_ascii=False, indent=4))
    else:
        typer.echo(yaml.dump(doc_stats, allow_unicode=True, sort_keys=False))


if __name__ == "__main__":
    app()
