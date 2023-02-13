from typing import List, Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AchivementBase(BaseModel):
    term:int
    name:str
    
class Achivement(BaseModel):
    id:UUID
    user:List[Dict]
    class Config:
        orm_mode=True
    