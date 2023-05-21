from pydantic import BaseSettings, Field


class Config(BaseSettings):
    node_ip: str = Field(env="NODE_IP")
    cluster_address: str = Field(env="CLUSTER_HOSTNAME")


config = Config()
