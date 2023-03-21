from typing import Dict
from uuid import UUID
from pydantic import BaseModel,Field


class TaskTagBase(BaseModel):
    name:str=Field(max_length=10)
    task:list[Dict]=[]


class TaskTag(BaseModel):
    id:UUID
    class Config:
        orm_mode=True
    