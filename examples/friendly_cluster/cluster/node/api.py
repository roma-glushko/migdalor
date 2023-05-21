from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from pydantic import BaseModel

from cluster.node.logger import logger
from cluster.node.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"node is starting up ({config.node_ip})")
    yield
    logger.info(f"node is shutting down ({config.node_ip})")


app = FastAPI(lifespan=lifespan)


class DiscoveryRequest(BaseModel):
    node: str


class NodeList(BaseModel):
    nodes: list[str]


@app.post("/hey/", status_code=status.HTTP_202_ACCEPTED)
async def hey_from_other_node(request: DiscoveryRequest):
    return None


@app.post("/bye/", status_code=status.HTTP_202_ACCEPTED)
async def bye_from_other_node(request: DiscoveryRequest):
    return None


@app.get("/friends/")
async def list_all_active_nodes() -> NodeList:
    return NodeList(
        nodes=[],
    )
