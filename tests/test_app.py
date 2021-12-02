import subprocess
import pkg_resources

from typer.testing import CliRunner

from eradication_success_assessment.get_required_effort import app

runner = CliRunner()


def test_app_traps_camera__get_required_effort():
    bash_command = "python eradication_success_assessment/get_required_effort.py get-required-effort --n-bootstrapping 30"
    subprocess.check_call(bash_command, shell=True)


def test_app_traps__write_methodology():
    result = runner.invoke(app, ["write-methodology"])
    assert result.exit_code == 0


def test_app_traps__version():
    expected_version = pkg_resources.require("eradication_success_assessment")[0].version
    result = runner.invoke(app, ["version"])
    assert expected_version in result.stdout
