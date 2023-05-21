# Friendly Cluster

An example of using Migdalor in Kubernetes cluster to implement peer discovery.

## Getting Started

In order to start the application, you need to have k3d and Tilt installed locally.
Then you can just call a few make commands that will bake the local Kubernetes cluster for you:

```bash
make cluster-start start
```

## Shutdown the cluster

```bash
make cluster-stop
```

## API Docs

```bash
make api-docs
```

Additionally, you can find a Postman API collection in the `docs` directory.

