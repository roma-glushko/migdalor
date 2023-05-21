import asyncio
from typing import Optional

import httpx as httpx

import migdalor
from cluster.node.client import NodeClient
from cluster.node.logger import logger


class FriendsManager:
    def __init__(self, node_address: migdalor.NodeAddress, cluster_address: migdalor.NodeAddress) -> None:
        self._cluster = migdalor.Cluster(
            node_address=(node_address),
            discovery=migdalor.KubernetesServiceDiscovery(service_address=cluster_address),
            nodes_added_handlers=[self._on_nodes_added],
            nodes_removed_handlers=[self._on_nodes_removed],
            update_every_secs=10,
        )

        self._greet_task: Optional[asyncio.Task] = None

    @property
    def friends(self) -> list[migdalor.NodeAddress]:
        return self._cluster.other_nodes + [self._cluster.current_node]

    async def greet_friends(self) -> None:
        for node_ip, port in self._cluster.other_nodes:
            try:
                client = NodeClient(node_ip=node_ip, port=port)

                await client.hey(current_node_address=self._cluster.current_node)
            except httpx.ConnectError:
                logger.warning(
                    f"{self._cluster.current_node} could not greet a friend node ({node_ip}:{port}),"
                    f" the node is still starting up"
                )

        logger.info(f"({self._cluster.current_node}) greeted friend nodes ({self._cluster.other_nodes})")

    async def bye_friends(self) -> None:
        for node_ip, port in self._cluster.other_nodes:
            try:
                client = NodeClient(node_ip=node_ip, port=port)

                await client.bye(current_node_address=self._cluster.current_node)
            except httpx.ConnectError:
                logger.warning(f"{self._cluster.current_node} {node_ip}:{port} node was shut down already")

        logger.info(f"({self._cluster.current_node}) byed friend nodes ({self._cluster.other_nodes})")

    async def add_friend(self, node: migdalor.NodeAddress) -> None:
        await self._cluster.add(node)

    async def remove_friend(self, node: migdalor.NodeAddress) -> None:
        await self._cluster.remove(node)

    async def start(self) -> None:
        logger.info(f"({self._cluster.current_node}) node is starting up")

        self._greet_task = asyncio.create_task(self._greet_friends_in_background())
        await self._cluster.start()

    async def stop(self) -> None:
        logger.info(f"{self._cluster.current_node} node is shutting down")
        await self._cluster.stop()
        await self.bye_friends()

        if self._greet_task:
            self._greet_task.cancel()
            await self._greet_task

    async def _greet_friends_in_background(self) -> None:
        """
        Greet friends in background to unblock API server startup. Otherwise, it would end up in a deadlock
        """
        logger.info(f"{self._cluster.current_node} waiting for a friend list update")

        async with self._cluster.nodes_updated:
            await self._cluster.nodes_updated.wait()

        logger.info(f"{self._cluster.current_node} friend list updated")

        await self.greet_friends()

    async def _on_nodes_added(self, nodes: set[migdalor.NodeAddress]) -> None:
        logger.info(f"{self._cluster.current_node} nodes added ({nodes})")

    async def _on_nodes_removed(self, nodes: set[migdalor.NodeAddress]) -> None:
        logger.info(f"{self._cluster.current_node} nodes removed ({nodes})")
