from pydantic import BaseModel, Field


class DateTime(BaseModel):
    year: int = Field(ge=2022)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    hour: int = Field(ge=0, lt=23)
    minute: int = Field(ge=0, lt=60)
