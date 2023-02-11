from typing import List,Dict
from uuid import UUID
from pydantic import BaseModel

class AuthorityBase(BaseModel):
    name:str

class Authority(AuthorityBase):
    id:UUID
    task:List[Dict]
    
