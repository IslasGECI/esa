FROM python:3
WORKDIR /workdir
COPY . .
RUN pip install \
    autopep8 \
    black \
    codecov \
    flake8 \
    git+https://github.com/IslasGECI/geci_plots.git@v0.1.0 \
    mutmut \
    numpy \
    pandas \
    pylint \
    pylint-fail-under \
    pytest \
    pytest-cov \
    rope \
    scipy \
    typer
CMD make
