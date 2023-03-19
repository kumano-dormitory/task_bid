from typing import Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from .task import Task
from .bid import Bid
from .template import Template
from app.schemas.originaldatetime import DateTime


class SlotBase(BaseModel):
    name: str = Field(max_length=20)
    start_time: datetime
    end_time: datetime
    creater: Dict
    task: Task


class SlotCancelRequest(BaseModel):
    premire_point: int

class SlotRequest(BaseModel):
    name: str = Field(max_length=20)
    start_time: DateTime
    end_time: DateTime
    task_id: UUID

    class Config:
        orm_mode = True


class SlotDeleteRequest(BaseModel):
    slots_id: list[UUID]


class Slot(BaseModel):
    id: UUID
    name: str=Field(max_length=20)
    start_time: datetime
    end_time: datetime
    creater_id: UUID
    task_id: UUID
    bid_id: UUID
    bid: Bid
    assignees: list[Dict] = []
    template: list[Template] = []


class SlotUpdate(BaseModel):
    name: str|None=Field(default=None,max_length=20)
    start_time: DateTime
    end_time: DateTime
    task_id: UUID

    class Config:
        orm_mode = True
