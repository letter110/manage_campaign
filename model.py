from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import List


class Customer(BaseModel):
    name: str
    phone_number: str
    any: str


class Campaign(BaseModel):
    id: UUID = uuid4()
    name: str
    customer_data: List[Customer]
