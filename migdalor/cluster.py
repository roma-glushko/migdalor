import asyncio
from typing import Optional, Callable, Awaitable

from migdalor.discovery import NodeDiscovery, NodeAddress
from migdalor.logger import logger

ClusterListener = Callable[[set[NodeAddress]], Awaitable[None]]


class Cluster:
    """
    Manages membership of nodes that belongs to the same group or cluster
    """

    def __init__(
        self,
        node_address: NodeAddress,
        discovery: NodeDiscovery,
        update_every_secs: float = 5,
        nodes_added_handlers: Optional[list[ClusterListener]] = None,
        nodes_removed_handlers: Optional[list[ClusterListener]] = None,
    ) -> None:
        self._node_address = node_address
        self._discovery = discovery
        self._update_every_secs = update_every_secs

        self._other_nodes: set[NodeAddress] = set()
        self._update_nodes_task: Optional[asyncio.Task] = None
        self._nodes_updated = asyncio.Condition()

        self._nodes_added_handlers = nodes_added_handlers or []
        self._nodes_removed_handlers = nodes_removed_handlers or []

    @property
    def current_node(self) -> NodeAddress:
        return self._node_address

    @property
    def other_nodes(self) -> list[NodeAddress]:
        return list(self._other_nodes)

    @property
    def nodes_updated(self) -> asyncio.Condition:
        return self._nodes_updated

    async def start(self) -> None:
        logger.info("starting cluster")

        self._update_nodes_task = asyncio.create_task(self._update_nodes_periodically(self._update_every_secs))

    async def stop(self) -> None:
        logger.info("stopping cluster")

        if self._update_nodes_task:
            self._update_nodes_task.cancel()
            await self._update_nodes_task

    async def add(self, node_address: NodeAddress) -> None:
        """Manually add a new node to the cluster"""
        if node_address in self._other_nodes:
            return

        self._other_nodes.add(node_address)

        await self._on_nodes_added({node_address})

    async def remove(self, node_address: NodeAddress) -> None:
        """Manually remove a new node to the cluster"""
        if node_address not in self._other_nodes:
            return

        self._other_nodes.remove(node_address)

        await self._on_nodes_removed({node_address})

    async def _update_nodes_periodically(self, updates_every_secs: float) -> None:
        # init the node list as soon as possible
        await self._update_nodes()

        while True:
            try:
                await asyncio.sleep(updates_every_secs)
                await self._update_nodes()
            except asyncio.CancelledError:
                logger.debug("update cluster task canceled")
                return

    async def _update_nodes(self) -> None:
        current_nodes = await self._discovery.get_all_nodes()

        try:
            current_nodes.remove(self._node_address)
        except KeyError:
            # if self IP is not on the list, then it's fine
            # there is no guarantees that, for example, Kubernetes would update its DNS before the node is starting up
            ...

        previous_other_nodes = self._other_nodes

        logger.debug("update cluster", extra={"current": current_nodes, "previous": previous_other_nodes})

        logger.debug(
            "updating cluster nodes",
            extra={"current": current_nodes, "prev": previous_other_nodes},
        )

        added_nodes = current_nodes - previous_other_nodes
        removed_nodes = previous_other_nodes - current_nodes

        async with self._nodes_updated:
            self._other_nodes = current_nodes
            self._nodes_updated.notify_all()

        if added_nodes:
            await self._on_nodes_added(added_nodes)

        if removed_nodes:
            await self._on_nodes_removed(removed_nodes)

    async def _on_nodes_added(self, added_nodes: set[NodeAddress]) -> None:
        logger.debug("added nodes", extra={"nodes": added_nodes})

        for handler in self._nodes_added_handlers:
            await handler(added_nodes)

    async def _on_nodes_removed(self, removed_nodes: set[NodeAddress]) -> None:
        logger.debug("removed nodes", extra={"nodes": removed_nodes})

        for handler in self._nodes_removed_handlers:
            await handler(removed_nodes)
