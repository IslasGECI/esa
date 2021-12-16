from setuptools import setup, find_packages

setup(
    name="esa",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": ["traps_camera=esa.get_required_effort:app"]
    },
)
