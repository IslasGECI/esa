import subprocess
import pkg_resources


def test_app_traps__version():
    expected_version = pkg_resources.require("eradication_success_assessment")[0].version
    bash_command = "python eradication_success_assessment/get_required_effort.py version"
    subprocess.check_call(bash_command, shell=True)
    obtained_version = subprocess.getoutput(bash_command)
    assert obtained_version == expected_version
