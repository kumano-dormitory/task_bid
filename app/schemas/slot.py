from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from schemas.user import User
from schemas.authority import Authority


class Task(BaseModel):
    __tablename__="task"
    id:UUID
    name:str
    detail:str
    authority:List[Authority]
    
class Slot(BaseModel):
    id:UUID
    name:str
    start_time:datetime
    end_time:datetime
    assignees:List[User]
    task:List[Task]