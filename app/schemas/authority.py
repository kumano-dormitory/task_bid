from typing import List,Dict,Literal
from uuid import UUID
from pydantic import BaseModel,Field

class AuthorityBase(BaseModel):
    name:str

class Authority(AuthorityBase):
    id:UUID
    task:List[Dict]
    
class AuthorityRequest(BaseModel):
    name:str=Field(max_length=50)
    url:str=Field(max_length=30)
    method:Literal["GET","POST","PUT","PATCH","DELETE"]
    class Config:
        orm_mode=True