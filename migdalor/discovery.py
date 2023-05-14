import asyncio
import socket

NodeAddress = tuple[str, int]


def parse_address(service_address: str) -> NodeAddress:
    ...


class NodeDiscovery:
    async def get_all_nodes(self) -> set[NodeAddress]:
        ...


class KubernetesServiceDiscovery(NodeDiscovery):
    """
    Perform peer discovery via the Kubernetes headless service
    """

    def __init__(self, service_address: str) -> None:
        self._hostname, self._port = parse_address(service_address)

    async def get_all_nodes(self) -> set[NodeAddress]:
        loop = asyncio.get_running_loop()

        raw_node_addresses = await loop.getaddrinfo(
            self._hostname,
            self._port,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
        )

        return {(ip, port) for _, _, ip, port, in raw_node_addresses}


class StaticDiscovery(NodeDiscovery):
    """
    Use predefined static list of node addresses to discover. Useful for testing purposes mostly
    """

    def __init__(self, nodes: list[NodeAddress]) -> None:
        self._nodes = set(nodes)

    async def get_all_nodes(self) -> set[NodeAddress]:
        return self._nodes
