import subprocess
import pkg_resources


def test_app_traps_camera__get_required_effort():
    bash_command = "python esa/get_required_effort.py get-required-effort --n-bootstrapping 30"
    subprocess.check_call(bash_command, shell=True)
