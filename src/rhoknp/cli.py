from pathlib import Path

import typer

from rhoknp import Document, __version__

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
    print(Document.from_knp(knp_path.read_text()).to_raw_text(), end="")


@app.command(help="Show statistics of given file or directory.")
def stats(
    knp_path: Path = typer.Argument(
        ..., exists=True, dir_okay=True, help="Path to knp file or directory to calculate statistics on."
    ),
    json: bool = typer.Option(False, "--json", "-j", help="Output statistics in JSON format."),
):
    print(f"knp_path: {knp_path}, json: {json}")


if __name__ == "__main__":
    app()
