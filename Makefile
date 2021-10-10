new_hash = $(shell sha2 -256 -q Pipfile)
old_hash = $(shell cat pipfile_hash)
PIPENV_VENV_IN_PROJECT = 1
PROJECT_NAME = lagrange_interpolating_polynomial_viewer
PYTHON_CMD = pipenv run python

.PHONY: default
default: lint

.PHONY: setup
setup:
	if ! pipenv --venv; then PIPENV_VENV_IN_PROJECT=$(PIPENV_VENV_IN_PROJECT) pipenv install --dev; fi

.PHONY: update
update: setup
	if [[ "$(new_hash)" != "$(old_hash)" ]]; then PIPENV_VENV_IN_PROJECT=$(PIPENV_VENV_IN_PROJECT) pipenv update --dev; echo "$(new_hash)" > pipfile_hash; fi
	if [[ ! -s .git/hooks/pre-commit ]]; then pipenv run pre-commit install; fi

.PHONY: run
run: update
	$(PYTHON_CMD) main.py

.PHONY: lint
lint: update
	pipenv run autoflake -i -r --imports $(PROJECT_NAME) $(PROJECT_NAME)
	pipenv run black $(PROJECT_NAME)
	pipenv run flake8 $(PROJECT_NAME)
	pipenv run mypy --strict -p $(PROJECT_NAME)

# .PHONY: test
# test: update
# 	pipenv run pytest --cov=$(PROJECT_NAME) $(PROJECT_NAME)
# 	pipenv run coverage xml -i
