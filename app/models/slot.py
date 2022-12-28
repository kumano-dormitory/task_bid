from sqlalchemy import Column,String,Table,ForeignKey,DateTime,Text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .timestamp import TimestampMixin
from .users import slots_table,experience_table

authority_table=Table(
    "authority_table",
    Base.metadata,
    Column("task",ForeignKey("task.id"),primary_key=True),
    Column("authority",ForeignKey("authority.id"),primary_key=True),
)

tag_table=Table(
    "tasktag_table",
    Base.metadata,
    Column("task",ForeignKey("task.id"),primary_key=True),
    Column("tasktag",ForeignKey("tasktag.id"),primary_key=True)
)
class Slot(Base,TimestampMixin):
    __tablename__="slot"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(20))
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    assignees=relationship("User",secondary=slots_table,back_populates="slots")
    creater_id=Column(UUIDType(binary=False),ForeignKey("user.id"))
    creater=relationship("User",back_populates="create_slot")
    task_id=Column(UUIDType(binary=False),ForeignKey("task.id"))
    task=relationship("Task",back_populates="slot",uselist=False)
    bid_id=Column(UUIDType(binary=False),ForeignKey("bid.id"))
    bid=relationship("Bid",back_populates="slot")
    
class Task(Base,TimestampMixin):
    __tablename__="task"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(20))
    detail=Column(Text(400))
    slot=relationship("Slot",back_populates="task")
    expert=relationship("User" ,secondary=experience_table,back_populates="exp_task")
    creater_id=Column(UUIDType(binary=False),ForeignKey("user.id"))
    creater=relationship("User",back_populates="create_task")
    authority=relationship("Authority",secondary=authority_table,back_populates="task")
    tag=relationship("TaskTag",secondary=tag_table,back_populates="task")
    
class TaskTag(Base):
    __tablename__="tasktag"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(10))
    task=relationship("Task",secondary=tag_table,back_populates="tag")