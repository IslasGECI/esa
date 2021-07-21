from setuptools import setup, find_packages

setup(
    name="eradication_success_assessment",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": ["traps_camera=eradication_success_assessment.get_required_effort:app"]
    },
)
