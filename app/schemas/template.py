from pydantic import BaseModel,Field
from uuid import UUID

class TemplateBase(BaseModel):
    id:UUID
    class Config:
        orm_mode=True
        
class Template(TemplateBase):
    name:str=Field(max_length=20)
    class Config:
        orm_mode=True

class TemplateDate(BaseModel):
    year: int=Field(ge=2022)
    month: int=Field(ge=1,le=12)
    day: int=Field(ge=1,le=31)


class TemplateCreate(BaseModel):
    name: str=Field(max_length=20)
    slots: list[UUID] = []


class TemplateGenRequest(BaseModel):
    first_day: TemplateDate


    class Config:
        orm_mode = True

class TemplateBulkGenRequest(BaseModel):
    first_days: list[TemplateDate]


    class Config:
        orm_mode = True
        
class TemplateSlotDeleteRequest(BaseModel):
    slot_id:str