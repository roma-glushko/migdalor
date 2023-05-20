from contextlib import asynccontextmanager

from fastapi import FastAPI

from cluster.node.logger import logger
from cluster.node.config import NODE_IP


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"node is starting up ({NODE_IP})")
    yield
    logger.info(f"node is shutting down ({NODE_IP})")


app = FastAPI(lifespan=lifespan)


@app.post("/hey/")
def hey_from_other_node():
    return {"Hello": "World"}


@app.post("/bye/")
def bye_from_other_node():
    return {"Hello": "World"}


@app.post("/friends/")
def list_all_active_nodes():
    return {"Hello": "World"}
