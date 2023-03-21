from typing import Literal
from uuid import UUID
from pydantic import BaseModel, Field
import enum
from .achivement import Achivement
from .task import Task
from .bid import Bid
from .slot import Slot


class AddUserTask(BaseModel):
    exp_task: list[UUID]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str = Field(max_length=20)
    password: str
    block: Literal["A1", "A2", "A3", "A4", "B12", "B3", "B4", "C12", "C34"]
    room_number: str = Field(max_length=10)
    exp_task:list[UUID]|None
    class Config:
        schema_extra = {
            "example": {
                "name": "恒川平",
                "password": "testuser",
                "block": "B3",
                "room_number": "B310",
            }
        }


class User(UserBase):
    id: UUID
    achivement: list[Achivement] = []
    experience: list[Task] = []
    slots: list[Slot] = []
    create_slot: list[Slot] = []
    create_task: list[Task] = []
    point: int = 0
    bid: list[Bid] = []

    class Config:
        orm_mode = True


class UserDisplay(BaseModel):
    id: UUID
    name: str
    block: Literal["A1", "A2", "A3", "A4", "B12", "B3", "B4", "C12", "C34"]
    room_number: str
    achivement: list[Achivement] = []
    exp_task: list[Task] = []
    slots: list[Slot] = []
    create_slot: list[Slot] = []
    create_task: list[Task] = []
    point: int
    bid: list[Bid] = []
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=20)
    block: Literal[
        "A1", "A2", "A3", "A4", "B12", "B3", "B4", "C12", "C34"
    ] | None
    room_number: str | None = Field(max_length=10)
    old_password: str | None
    password: str | None
