from typing import List, Optional,Literal,TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel
import enum
if TYPE_CHECKING:
    from schemas.achivement import Achivement
    from schemas.slot import Slot
    from schemas.task import Task
    from schemas.bid import Bid


    


class UserBase(BaseModel):
    name:str
    password:str
    block:Literal["A1","A2","A3","A4","B12","B3","B4","C12","C34"]
    room_number:str


class User(UserBase):
    id:UUID
    achivement:List["Achivement"]=[]
    experience:List["Task"]=[]
    slots:List["Slot"]=[]
    create_slot:List["Slot"]=[]
    create_task:List["Task"]=[]
    point:int=0
    bid:List["Bid"]=[]
    
    class Config:
        orm_mode = True