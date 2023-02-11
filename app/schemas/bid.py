from typing import Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class BidBase(BaseModel):
    name:str
    open_time:datetime
    close_time:datetime
    slot:Dict
    start_point:int
    buyout_point:int
    
class Bid(BaseModel):
    id:UUID
    name:str
    is_complete:bool
    lowest_user_id:UUID
    lowest_user:Dict

class BidRequest(BaseModel):
    name:str|None
    open_time:datetime
    close_time:datetime
    slot:UUID
    start_point:int
    buyout_point:int
    class Config:
        orm_mode=True
    