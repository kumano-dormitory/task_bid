from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from schemas.achivement import Achivement
from schemas.slot import Task,Slot
from schemas.bid import Bid
import enum

class Block(str,enum.Enum):
    A1="A1"
    A2="A2"
    A3="A3"
    A4="A4"
    B12="B12"
    B3="B3"
    B4="B4"
    C12="C12"
    C34="C34"


class UserBase(BaseModel):
    name:str
    password:str
    block:Block
    room_number:str


class User(UserBase):
    id:UUID
    achivement:List[Achivement]=[]
    experience:List[Task]=[]
    slots:List[Slot]=[]
    create_slot:List[Slot]=[]
    create_task:List[Task]=[]
    point:int=0
    bid:List[Bid]=[]
    
    class Config:
        orm_mode = True