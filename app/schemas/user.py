from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from schemas.achivement import Achivement
from schemas.slot import Task,Slot
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


class User(BaseModel):
    id:UUID
    name:str
    password:str
    block:Block
    room_number:str
    achivement:List[Achivement]
    experience:List[Task]
    slots:List[Slot]
    point:int