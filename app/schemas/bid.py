from typing import List, Optional,TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from schemas.authority import Authority
from schemas.slot import Slot
if TYPE_CHECKING:
    from schemas.users import User

class Bid(BaseModel):
    id:UUID
    name:str
    start_time:datetime
    end_time:datetime
    slot:Slot
    start_point:int
    lowest_point:int
    second_point:int
    buyout_point:int
    is_complete:bool
    lowest_user_id:str
    lowest_user:"User"