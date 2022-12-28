from sqlalchemy import Column,String,Enum,Table,ForeignKey,Integer,Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .timestamp import TimestampMixin
import enum

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
    Column("user",ForeignKey("user.id")),
    Column("achivement",ForeignKey("achivement.id")),
)

experience_table=Table(
    "experience_table",
    Base.metadata,
    Column("user",ForeignKey("user.id")),
    Column("task",ForeignKey("task.id"))
)

slots_table=Table(
    "slots_table",
    Base.metadata,
    Column("user",ForeignKey("user.id"),primary_key=True),
    Column("slot",ForeignKey("slot.id"),primary_key=True),
)

class User(Base, TimestampMixin):
    __tablename__="user"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(20))
    password=Column(String(400))
    block=Column(Enum(Block))
    room_number=Column(String(10))
    achivement=relationship("Achivement",secondary=achivement_table,back_populates="user")
    exp_task=relationship("Task",secondary=experience_table,back_populates="expert")
    slots=relationship("Slot",secondary=slots_table,back_populates="assignees")
    create_slot=relationship("Slot",back_populates="creater")
    create_task=relationship("Task",back_populates="creater")
    point=Column(Integer,default=0)
    bid=relationship("Bid",back_populates="lowest_user")
    is_active=Column(Boolean,default=True)