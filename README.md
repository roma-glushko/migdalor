<p align="center">
<img src="https://github.com/roma-glushko/migdalor/blob/main/docs/imgs/logo-wide.png?raw=true" width="100%" alt="Migdalor - a Kubernetes native cluster management for modern Python>" />
</p>

# Migdalor

Migdalor is a cluster membership library for modern asyncio Python distributed systems.

Migdalor doesn't require a separate broker (e.g. Redis, etcd, Zookeeper, Chabby, etc) to work, but leverage Kubernetes out-of-the-box capabilities
to solve the peer discovery problem.

## Features

- Modern Asyncio Python 🐍
- Brokerless Kubernetes native peer discovery based on headless services 🔦
- Hooks into membership change events 🔭
