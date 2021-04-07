all: mutants

repo = eradication_success_assessment
codecov_token = c29d80f3-6501-4816-b788-bc6170024d81

.PHONY: all clean format install lint mutants tests

clean:
	rm --force .mutmut-cache
	rm --recursive --force ${repo}.egg-info
	rm --recursive --force ${repo}/__pycache__
	rm --recursive --force tests/__pycache__

check:
	black --check --line-length 100 ${repo}
	black --check --line-length 100 tests
	flake8 --max-line-length 100 ${repo}
	flake8 --max-line-length 100 tests

format:
	black --line-length 100 ${repo}
	black --line-length 100 tests

install:
	pip install --editable .

lint:
	flake8 --max-line-length 100 ${repo}
	flake8 --max-line-length 100 tests
	pylint \
		--disable=bad-continuation \
		--disable=missing-function-docstring \
		--disable=missing-module-docstring \
		${repo}
	pylint \
		--disable=bad-continuation \
		--disable=missing-function-docstring \
		--disable=missing-module-docstring \
		tests

mutants:
	mutmut run --paths-to-mutate ${repo}

coverage:
	pytest --cov=${repo} --cov-report=xml --verbose && \
	codecov --token=${codecov_token}

tests:
	pytest --verbose