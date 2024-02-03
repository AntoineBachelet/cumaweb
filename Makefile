PYTHON_INTERPRETER=python

.PHONY: style
style:
	echo "Running style checks"
	pre-commit run --all-files

.PHONY: test
test:
	echo "Running tests"
	$(PYTHON_INTERPRETER) -m pytest -v

.PHONY: pre-up
pre-update:
	echo "Running pre-update checks"
	pre-commit autoupdate