from pydantic import BaseModel


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
