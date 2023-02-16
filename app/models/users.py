from sqlalchemy import Column,String,Table,ForeignKey
from typing import Optional
from app.database import Base
from sqlalchemy.orm import relationship,Mapped
from sqlalchemy.orm import mapped_column
from uuid import uuid4,UUID
from .timestamp import TimestampMixin
import enum
from app.models.achivement import Achivement
from app.models.bid import Bidder
from app.models.slot import Slot,Task
class Block(str,enum.Enum):
    A1="A1"
    A2="A2"
    A3="A3"
    A4="A4"
    B12="B12"
    B3="B3"
    B4="B4"
    C12="C12"
    C34="C34"

achivement_table=Table(
    "achivement_table",
    Base.metadata,
    Column("user",ForeignKey("user.id"),primary_key=True),
    Column("achivement",ForeignKey("achivement.id"),primary_key=True),
)

experience_table=Table(
    "experience_table",
    Base.metadata,
    Column("user",ForeignKey("user.id"),primary_key=True),
    Column("task",ForeignKey("task.id"),primary_key=True)
)

slots_table=Table(
    "slots_table",
    Base.metadata,
    Column("user",ForeignKey("user.id"),primary_key=True),
    Column("slot",ForeignKey("slot.id"),primary_key=True),
)

class User(Base, TimestampMixin):
    __tablename__="user"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(20))
    password:Mapped[str]=mapped_column(String(400))
    block:Mapped["Block"]
    room_number:Mapped[str]=mapped_column(String(10))
    achivement:Mapped[Optional[list["Achivement"]]]=relationship(secondary=achivement_table,back_populates="user")
    exp_task:Mapped[Optional[list["Task"]]]=relationship(secondary=experience_table,back_populates="expert")
    slots:Mapped[Optional[list["Slot"]]]=relationship(secondary=slots_table,back_populates="assignees")
    create_slot:Mapped[UUID]=relationship(back_populates="creater")
    create_task:Mapped[Optional[list["Task"]]]=relationship(back_populates="creater")
    point:Mapped[int]=mapped_column(default=0)
    bid:Mapped[Optional[list["Bidder"]]]=relationship(back_populates="user",cascade="all")
    is_active:Mapped[bool]=mapped_column(default=True)