from typing import List,Dict,Literal
from uuid import UUID
from pydantic import BaseModel

class AuthorityBase(BaseModel):
    name:str

class Authority(AuthorityBase):
    id:UUID
    task:List[Dict]
    
class AuthorityRequest(BaseModel):
    name:str
    url:str
    method:Literal["GET","POST","PUT","PATCH","DELETE"]
    class Config:
        orm_mode=True