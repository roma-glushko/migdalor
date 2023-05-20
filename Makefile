SOURCE?=migdalor
TESTS?=tests

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	@poetry install

lint: ## Lint codebase
	@echo "🧹 Ruff"
	@ruff --fix $(SOURCE) $(TESTS)
	@echo "🧹 Black"
	@black $(SOURCE) $(TESTS)
	@echo "🧹 MyPy"
	@mypy --pretty $(SOURCE)
