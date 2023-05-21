from pydantic.main import BaseModel

import migdalor


class DiscoveryRequest(BaseModel):
    node: migdalor.NodeAddress


class NodeList(BaseModel):
    nodes: list[migdalor.NodeAddress]


class MoodResponse(BaseModel):
    mood: str


class CatchupResponse(BaseModel):
    moods: dict[str, str]
