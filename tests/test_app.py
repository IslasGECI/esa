import subprocess
import pkg_resources
import pytest

from typer.testing import CliRunner

from eradication_success_assessment.get_required_effort import app

runner = CliRunner()


COMMANDS = ["write-methodology", "plot-histogram-effort", "version", "get-required-effort"]


@pytest.mark.parametrize("command", COMMANDS)
def test_app_traps__write_methodology(command):
    result = runner.invoke(app, [command])
    assert result.exit_code == 0


def test_app_traps__version():
    expected_version = pkg_resources.require("eradication_success_assessment")[0].version
    result = runner.invoke(app, ["version"])
    assert expected_version in result.stdout
