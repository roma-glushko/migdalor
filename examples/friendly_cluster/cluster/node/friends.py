import migdalor
from cluster.node.logger import logger


class FriendsManager:
    def __init__(self, node_address: migdalor.NodeAddress, cluster_address: migdalor.NodeAddress) -> None:
        self._cluster = migdalor.Cluster(
            node_address=(node_address),
            discovery=migdalor.KubernetesServiceDiscovery(service_address=cluster_address),
            nodes_added_handlers=[self._on_nodes_added],
            nodes_removed_handlers=[self._on_nodes_removed],
        )

    @property
    def friends(self) -> list[migdalor.NodeAddress]:
        return self._cluster.other_nodes + [self._cluster.current_node]

    async def start(self) -> None:
        logger.info(f"node is starting up ({self._cluster.current_node})")
        await self._cluster.start()

    async def stop(self) -> None:
        logger.info(f"node is shutting down ({self._cluster.current_node})")
        await self._cluster.stop()

    async def _on_nodes_added(self, nodes: set[migdalor.NodeAddress]) -> None:
        logger.info(f"nodes added ({nodes})")

    async def _on_nodes_removed(self, nodes: set[migdalor.NodeAddress]) -> None:
        logger.info(f"nodes removed ({nodes})")
