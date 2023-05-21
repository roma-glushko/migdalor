CLUSTER?=party-cluster
REGISTRY_PORT?=8800
SOURCE?=cluster

.PHONY: help

help:
	@echo "🔆 Party Cluster - An Example of Using Migdalor in Kubernetes cluster to bring peer discovery on"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

cluster-start:  ## Start the cluster
	@k3d cluster create $(CLUSTER) --agents 2 \
		--registry-create $(CLUSTER)-registry:0.0.0.0:$(REGISTRY_PORT) \
		--kubeconfig-update-default --kubeconfig-switch-context

cluster-ctx:  ## Configure the cluster context
	@kubectl config set current-context k3d-$(CLUSTER)

cluster-stop: ## Stop the cluster
	@k3d cluster delete $(CLUSTER)

start: cluster-ctx ## Start the whole system
	@tilt up

image-build: ## Build the image
	@docker build -t party-cluster/node:dev -f Dockerfile .

lint: ## Lint source code
	@black $(SOURCE)
	@ruff --fix $(SOURCE)
	@mypy --pretty $(SOURCE)

api-docs: ## Open Friendly Cluster API specification (OpenAPI)
	@open http://localhost:8888/docs#/
