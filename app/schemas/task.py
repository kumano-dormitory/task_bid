from typing import List, Optional,TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.slot import Slot
    from schemas.users import User
    from schemas.tasktag import TaskTag
    from schemas.authority import Authority

class TaskBase(BaseModel):
    name:str
    detail:str
    creater:"User"
    authority:List[Authority]
    tag:List["TaskTag"]=[]

class Task(TaskBase):
    id:UUID
    creater_id:UUID
    slot:List["Slot"]
    expert:List["User"]
    authority:List["Authority"]
    class Config:
        orm_mode=True