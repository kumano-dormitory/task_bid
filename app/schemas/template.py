from pydantic import BaseModel
from uuid import UUID

class TemplateBase(BaseModel):
    id:UUID
    class Config:
        orm_mode=True
        
class Template(TemplateBase):
    name:str
    class Config:
        orm_mode=True

class TemplateDate(BaseModel):
    year: int
    month: int
    day: int


class TemplateCreate(BaseModel):
    name: str
    slots: list[str] = []


class TemplateGenRequest(BaseModel):
    first_day: TemplateDate
    start_point: int
    buyout_point: int

    class Config:
        orm_mode = True

class TemplateBulkGenRequest(BaseModel):
    first_days: list[TemplateDate]
    start_point: int
    buyout_point: int

    class Config:
        orm_mode = True
        
class TemplateSlotDeleteRequest(BaseModel):
    slot_id:str