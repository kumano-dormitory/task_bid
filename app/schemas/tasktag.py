from typing import Dict
from uuid import UUID
from pydantic import BaseModel


class TaskTagBase(BaseModel):
    name:str
    task:list[Dict]=[]


class TaskTag(BaseModel):
    id:UUID
    class Config:
        orm_mode=True
    