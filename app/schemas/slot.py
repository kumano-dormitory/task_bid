from typing import List,TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.task import Task
    from schemas.users import User
    from schemas.bid import Bid
    
class SlotBase(BaseModel):
    name:str
    start_time:datetime
    end_time:datetime
    creater:"User"
    task:"Task"
    bid:"Bid"
    
class Slot(BaseModel):
    id:UUID
    name:str
    start_time:datetime
    end_time:datetime
    creater_id: UUID
    task_id:UUID
    bid_id:UUID
    assignees:List["User"]
    task:List["Task"]