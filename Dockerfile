FROM python:3.8
WORKDIR /workdir
COPY . .
RUN pip install \
    autopep8 \
    black \
    codecov \
    flake8 \
    git+https://github.com/IslasGECI/geci_plots.git@feature/return_fig_in_histogram_with_limits \
    mutmut \
    numpy \
    pandas \
    pylint \
    pylint-fail-under \
    pytest \
    pytest-cov \
    pytest-mpl \
    rope \
    scipy \
    typer
CMD make
