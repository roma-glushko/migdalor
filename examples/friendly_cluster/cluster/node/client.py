import httpx

from cluster.node.entities import DiscoveryRequest, MoodResponse
from migdalor import NodeAddress
from migdalor.logger import logger


class NodeClient:
    def __init__(self, node_ip: str, port: int) -> None:
        self._node_ip = node_ip
        self._port = port
        self._client = httpx.AsyncClient(base_url=f"http://{node_ip}:{port}")

    async def hey(self, current_node_address: NodeAddress) -> None:
        response = await self._client.post(
            "/hey/",
            json=DiscoveryRequest(node=current_node_address).dict(),
        )

        if response.status_code == 202:
            logger.debug(f"{current_node_address} friend node greeted ({self._node_ip}:{self._node_ip})")
        else:
            logger.warning(
                f"{current_node_address} error happened while greeted a friend node "
                f"({self._node_ip}:{self._node_ip}): {response.content}"
            )

    async def bye(self, current_node_address: NodeAddress) -> None:
        response = await self._client.post(
            "/bye/",
            json=DiscoveryRequest(node=current_node_address).dict(),
        )

        if response.status_code == 202:
            logger.debug(f"({current_node_address}) friend node byed ({self._node_ip}:{self._node_ip})")
        else:
            logger.warning(
                f"{current_node_address} error happened while byed a friend node "
                f"({self._node_ip}:{self._node_ip}): {response.content}"
            )

    async def mood(self) -> str:
        response = await self._client.get("/mood/")

        if response.status_code != 200:
            logger.warning(f"could not get friend node mood ({self._node_ip}:{self._node_ip}): {response.content}")

        return MoodResponse(**response.json()).mood
