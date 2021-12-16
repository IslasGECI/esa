import subprocess
import pkg_resources


def test_app_traps_camera__get_required_effort():
    bash_command = "python esa/get_required_effort.py get-required-effort --n-bootstrapping 30"
    subprocess.check_call(bash_command, shell=True)


def test_app_traps__write_methodology():
    bash_command = "python esa/get_required_effort.py write-methodology"
    subprocess.check_call(bash_command, shell=True)


def test_app_traps__version():
    expected_version = pkg_resources.require("esa")[0].version
    bash_command = "traps_camera version"
    subprocess.check_call(bash_command, shell=True)
    obtained_version = subprocess.getoutput(bash_command)
    assert obtained_version == expected_version
