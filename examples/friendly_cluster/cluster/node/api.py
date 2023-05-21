from contextlib import asynccontextmanager
from fastapi import FastAPI, status, Request
from pydantic import BaseModel

import migdalor
from cluster.node.friends import FriendsManager
from cluster.node.config import config

manager = FriendsManager(
    node_address=(config.node_ip, config.port), cluster_address=(config.cluster_hostname, config.port)
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.start()
    yield
    await manager.stop()


app = FastAPI(lifespan=lifespan)


class DiscoveryRequest(BaseModel):
    node: migdalor.NodeAddress


class NodeList(BaseModel):
    nodes: list[migdalor.NodeAddress]


@app.post("/hey/", status_code=status.HTTP_202_ACCEPTED)
async def hey_from_other_node(request: DiscoveryRequest):
    return None


@app.post("/bye/", status_code=status.HTTP_202_ACCEPTED)
async def bye_from_other_node(request: DiscoveryRequest):
    return None


@app.get("/friends/")
async def list_all_active_nodes(request: Request) -> NodeList:
    return NodeList(
        nodes=manager.friends,
    )
