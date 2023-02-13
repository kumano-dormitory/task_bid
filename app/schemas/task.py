from typing import Optional,Dict,Any
from uuid import UUID
from pydantic import BaseModel,Field
from .tasktag import TaskTag
from .authority import Authority
    
    

class TaskBase(BaseModel):
    name:str
    detail:str
    


class TaskCreate(BaseModel):
    name:str
    detail:str
    max_woker_num:int=Field(1)
    min_woker_num:int=Field(1)
    exp_woker_num:int=Field(0)
    tag:list[UUID]=[]
    authority:list[UUID]=[]


class Task(TaskBase):
    id:UUID
    creater_id:UUID
    creater:Any=None
    slot:list[ Dict]=[]
    expert:list[Dict]=[]
    authority:list[Authority]=[]
    tag:list[TaskTag]=[]
    class Config:
        orm_mode=True
        
        
class TaskList(TaskBase):
    id:UUID
    create_id:UUID
    class Config:
        orm_mode=True
        
        
class TaskUpdate(BaseModel):
    name:str|None
    detail:str|None
    max_woker_num:int|None
    min_woker_num:int|None
    exp_woker_num:int|None
    class Config:
        orm_mode=True
