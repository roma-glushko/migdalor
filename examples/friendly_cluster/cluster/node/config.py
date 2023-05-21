from pydantic import BaseSettings, Field


class Config(BaseSettings):
    port: int = 8888
    node_ip: str = Field(env="NODE_IP")
    cluster_hostname: str = Field(env="CLUSTER_HOSTNAME")


config = Config()
