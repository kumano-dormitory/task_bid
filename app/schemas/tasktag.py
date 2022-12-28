from typing import List, Optional,TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.task import Task


class TaskBase(BaseModel):
    name:str
    task:List["Task"]


class TaskTag(BaseModel):
    id:UUID
    class Config:
        orm_mode=True
    