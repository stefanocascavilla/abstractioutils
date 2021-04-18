from typing import Optional, Dict
from pydantic import BaseModel


class ClusterDTO(BaseModel):
    name: Optional[str]
    image_url: Optional[str]
    vcpus: Optional[int]
    memory: Optional[int]
    user_id: Optional[str]
    port: Optional[int]
    has_ip: Optional[bool]
    type: Optional[str]
    region: Optional[str]
    project: Optional[str]

    id: Optional[str]
    status: Optional[str]
    creation_date: Optional[str]
    env_variables: Optional[Dict[str, str]]
    endpoint: Optional[str]
    ip_address: Optional[str]
    subnetwork: Optional[str]
    error_message: Optional[str]
    username: Optional[str]
    password: Optional[str]
