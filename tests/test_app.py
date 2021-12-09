import subprocess
import pkg_resources
import pytest

from typer.testing import CliRunner

from eradication_success_assessment.get_required_effort import app


def test_app_traps__version():
    expected_version = pkg_resources.require("eradication_success_assessment")[0].version
    bash_command = "python eradication_success_assessment/get_required_effort.py version"
    subprocess.check_call(bash_command, shell=True)
    obtained_version = subprocess.getoutput(bash_command)
    assert obtained_version == expected_version


runner = CliRunner()


COMMANDS = ["write-methodology", "plot-histogram-effort", "version", "get-required-effort"]


@pytest.mark.parametrize("command", COMMANDS)
def test_app_traps__write_methodology(command):
    result = runner.invoke(app, [command])
    assert result.exit_code == 0
