from typing import Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.originaldatetime import DateTime



class TenderRequest(BaseModel):
    tender_point: int

    class Config:
        orm_mode = True


class BidBase(BaseModel):
    name: str=Field(max_length=20)
    open_time: DateTime
    close_time: DateTime
    slot: Dict


class Bid(BaseModel):
    id: UUID
    name: str=Field(max_length=20)
    is_complete: bool
    lowest_user_id: UUID
    lowest_user: Dict


class BidRequest(BaseModel):
    name: str | None=Field(default=None,max_length=20)
    open_time: DateTime
    close_time: DateTime
    slot_id: UUID

    class Config:
        orm_mode = True


class BidConvertRequest(BaseModel):
    user_id: UUID

    class Config:
        orm_mode = True
