from typing import Literal
from uuid import UUID
from pydantic import BaseModel
import enum
from .achivement import Achivement
from .task import Task
from .bid import Bid
from .slot import Slot
    


class UserBase(BaseModel):
    name:str
    password:str
    block:Literal["A1","A2","A3","A4","B12","B3","B4","C12","C34"]
    room_number:str


class User(UserBase):
    id:UUID
    achivement:list[Achivement]=[]
    experience:list[Task]=[]
    slots:list[Slot]=[]
    create_slot:list[Slot]=[]
    create_task:list[Task]=[]
    point:int=0
    bid:list[Bid]=[]
    
    class Config:
        orm_mode = True
        

class UserDisplay(BaseModel):
    id:UUID
    name:str
    block:Literal["A1","A2","A3","A4","B12","B3","B4","C12","C34"]
    room_number:str
    achivement:list[Achivement]=[]
    exp_task:list[Task]=[]
    slots:list[Slot]=[]
    create_slot:list[Slot]=[]
    create_task:list[Task]=[]
    point:int
    bid:list[Bid]=[]
    is_active:bool
    
    class Config:
        orm_mode=True
        

    