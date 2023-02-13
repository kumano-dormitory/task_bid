from typing import Dict,TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel
if TYPE_CHECKING:
    from schemas.task import Slot


class TemplateBase(BaseModel):
    name:str
    slots:list[Dict]=[]


class Template(BaseModel):
    id:UUID
    class Config:
        orm_mode=True
    