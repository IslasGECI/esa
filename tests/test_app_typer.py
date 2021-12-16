import pytest
from typer.testing import CliRunner
from esa.get_required_effort import app


runner = CliRunner()


COMMANDS = ["write-methodology", "plot-histogram-effort", "version", "get-required-effort"]


@pytest.mark.parametrize("command", COMMANDS)
def test_app_traps__write_methodology(command):
    result = runner.invoke(app, [command])
    assert result.exit_code == 0
