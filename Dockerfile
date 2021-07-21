FROM python:3
WORKDIR /workdir
COPY . .
RUN pip install \
    autopep8 \
    black \
    codecov \
    flake8 \
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
