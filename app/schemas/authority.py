from typing import List,TYPE_CHECKING
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.users import Task

class AuthorityBase(BaseModel):
    name:str

class Authority(AuthorityBase):
    id:UUID
    task:List["Task"]
    
