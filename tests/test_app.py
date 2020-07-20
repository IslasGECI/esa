import subprocess

def test_app_traps_camera__get_required_effort():
    bash_command = (
        f"python eradication_success_assessment/get_required_effort.py get-required-effort"
    )
    subprocess.check_call(bash_command, shell=True)


def test_app_traps__write_methodology():
    bash_command = (
        f"python eradication_success_assessment/get_required_effort.py write-methodology"
    )
    subprocess.check_call(bash_command, shell=True)


def test_app_traps__version():
    bash_command = (
        f"python eradication_success_assessment/get_required_effort.py version"
    )
    subprocess.check_call(bash_command, shell=True)
    output = subprocess.getoutput(bash_command)
    assert output == 'v0.1.0'

