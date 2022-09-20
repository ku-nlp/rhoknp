from pathlib import Path

import typer

from rhoknp import Document, __version__
from rhoknp.utils.draw_tree import draw_tree

app = typer.Typer(help="rhoknp CLI utilities.")


def version_callback(value: bool):
    if value:
        typer.echo(f"rhoknp version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    _: bool = typer.Option(False, "--version", "-v", callback=version_callback, help="Show version and exit."),
):
    pass


@app.command(help="Print given file content in tree format.")
def show(
    knp_path: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to knp file to show"),
):
    document = Document.from_knp(knp_path.read_text())
    for sentence in document.sentences:
        print(sentence.comment)
        draw_tree(sentence.base_phrases, show_pos=False)


@app.command(help="Show statistics of given KNP file.")
def stats(
    knp_path: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Path to knp file to calculate statistics on."
    ),
    json: bool = typer.Option(False, "--json", "-j", help="Output statistics in JSON format."),
):
    print(f"knp_path: {knp_path}, json: {json}")


if __name__ == "__main__":
    app()
