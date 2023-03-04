from typing import Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from .task import Task
from .bid import Bid
from .template import Template
    
        
class SlotBase(BaseModel):
    name:str
    start_time:datetime
    end_time:datetime
    creater:Dict
    task:Task

class DateTime(BaseModel):
    year:int
    month:int
    day:int
    hour:int
    minute:int

class SlotCancelRequest(BaseModel):
    premire_point:int

class SlotRequest(BaseModel):
    name:str
    start_time:DateTime
    end_time:DateTime
    task:str
    class Config:
        orm_mode=True
    
    
class Slot(BaseModel):
    id:UUID
    name:str
    start_time:datetime
    end_time:datetime
    creater_id: UUID
    task_id:UUID
    bid_id:UUID
    bid:Bid
    assignees:list[Dict]=[]
    template:list[Template]=[]

