SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy coverage_conditional_plugin tests/*.py
	poetry run flake8 .

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report --ignore=51457

.PHONY: test
test: lint unit package
