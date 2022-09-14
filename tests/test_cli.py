from typer.testing import CliRunner

from rhoknp import __version__
from rhoknp.cli import app

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["-v"])
    assert result.exit_code == 0
    assert result.stdout.strip() == f"rhoknp version: {__version__}"
