from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List


class Cutomer(BaseModel):
    name: str
    phone_number: str
    any: str


class Schedule(BaseModel):
    time: int = 0
    runtime: int = 0
    loop: bool = False
    isStarting: bool = False


class Campaign(BaseModel):
    id: UUID = uuid4()
    name: str
    cutomer_data: List[Cutomer]
    schedule: Schedule
