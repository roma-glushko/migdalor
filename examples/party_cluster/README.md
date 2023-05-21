# The Party Cluster

An example of using Migdalor to implement peer discovery in Kubernetes cluster.

The Party Cluster simulates a little party where friends (or nodes) can come and go.
Each node is an HTTP server with some state and an ability to discover the rest of peers in the cluster thanks to Migdalor. 
Once a new node is up and running, it discovers all other active nodes and send them the hey request. 
This is an example of propagating membership information as soon as possible on the communication protocol level.

You can ask a node to catch up on mood of its peers. The mood is some arbitrary private state each node holds.

Although, the cluster starts with 3 nodes only, you can "resize" it by up/down-scaling via `kubectl`:

```bash
kubectl -n friendly-cluster scale --replicas=5 deployment node
```

Once the node receives a termination signal, it sends all peers the bye request and then peacefully terminates.

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

