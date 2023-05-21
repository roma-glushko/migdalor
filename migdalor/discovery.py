import asyncio
import socket

from migdalor.logger import logger

NodeAddress = tuple[str, int]
RawNodeAddress = tuple[socket.AddressFamily, socket.SocketKind, int, str, NodeAddress]


class NodeDiscovery:
    async def get_all_nodes(self) -> set[NodeAddress]:
        raise NotImplementedError


class KubernetesServiceDiscovery(NodeDiscovery):
    """
    Perform node discovery via the Kubernetes headless service
    """

    def __init__(self, service_address: NodeAddress) -> None:
        self._hostname, self._port = service_address

    async def get_all_nodes(self) -> set[NodeAddress]:
        loop = asyncio.get_running_loop()

        raw_node_addresses: list[RawNodeAddress] = await loop.getaddrinfo(
            self._hostname,
            self._port,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
        )

        logger.debug(f"raw node addresses ({raw_node_addresses})")

        return {address for _, _, _, _, address in raw_node_addresses}


class StaticDiscovery(NodeDiscovery):
    """
    Use predefined static list of node addresses to discover. Useful for testing purposes mostly
    """

    def __init__(self, nodes: list[NodeAddress]) -> None:
        self._nodes = set(nodes)

    async def get_all_nodes(self) -> set[NodeAddress]:
        return self._nodes
