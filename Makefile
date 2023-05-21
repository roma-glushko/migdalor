SOURCE?=migdalor
TESTS?=tests

.PHONY: help
help:
	@echo "========================================================================"
	@echo "🔆\033[36mMigdalor\033[0m, a peer discovery library for Kubernetes era"
	@echo "========================================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install project dependencies
	@pdm install

lint: ## Lint codebase
	@echo "🧹 Ruff"
	@ruff --fix $(SOURCE) $(TESTS)
	@echo "🧹 Black"
	@black $(SOURCE) $(TESTS)
	@echo "🧹 MyPy"
	@mypy --pretty $(SOURCE)

publish: ## Publish the package on Pypi
	@pdm publish
