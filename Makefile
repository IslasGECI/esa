all: check coverage mutants

repo = eradication_success_assessment
codecov_token = c29d80f3-6501-4816-b788-bc6170024d81

define lint
	pylint \
        --disable=bad-continuation \
        --disable=missing-class-docstring \
        --disable=missing-function-docstring \
        --disable=missing-module-docstring \
        ${1}
endef

.PHONY: \
	all \
	clean \
	coverage \
	check \
	format \
	install \
	linter \
	mutants \
	tests

clean:
	rm --force .mutmut-cache
	rm --recursive --force ${repo}.egg-info
	rm --recursive --force ${repo}/__pycache__
	rm --recursive --force tests/__pycache__
	rm --recursive --force tests/baseline

coverage: setup
	pytest --cov=${repo} --cov-report=xml --verbose && \
	codecov --token=${codecov_token}

check:
	black --check --line-length 100 ${repo}
	black --check --line-length 100 setup.py
	black --check --line-length 100 tests
	flake8 --max-line-length 100 ${repo}
	flake8 --max-line-length 100 setup.py
	flake8 --max-line-length 100 tests

format:
	black --line-length 100 ${repo}
	black --line-length 100 tests

setup:
	pip install --editable .
	pytest --mpl-generate-path=tests/baseline

linter:
	$(call lint, ${repo})
	$(call lint, tests)

mutants: setup
	mutmut run --paths-to-mutate ${repo} --runner "pytest --mpl"

tests:
	pytest --verbose
