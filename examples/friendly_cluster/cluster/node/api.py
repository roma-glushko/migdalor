from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Request

from cluster.node.entities import DiscoveryRequest, NodeList
from cluster.node.friends import FriendsManager
from cluster.node.config import config

manager = FriendsManager(
    node_address=(config.node_ip, config.port),
    cluster_address=(config.cluster_hostname, config.port),
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.start()
    yield
    await manager.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/hey/", status_code=status.HTTP_202_ACCEPTED)
async def hey_from_other_node(request: DiscoveryRequest) -> None:
    await manager.add_friend(request.node)


@app.post("/catchUp/", status_code=status.HTTP_202_ACCEPTED)
async def catchup_with_all_nodes() -> None:
    await manager.greet_friends()


@app.post("/bye/", status_code=status.HTTP_202_ACCEPTED)
async def bye_from_other_node(request: DiscoveryRequest) -> None:
    await manager.remove_friend(request.node)


@app.get("/friends/")
async def list_all_active_nodes(request: Request) -> NodeList:
    return NodeList(
        nodes=manager.friends,
    )
