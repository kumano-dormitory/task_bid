from sqlalchemy import Column,String,Table,ForeignKey
from typing import Optional
from app.database import Base
from sqlalchemy.orm import mapped_column,relationship,Mapped
from uuid import uuid4,UUID
from .timestamp import TimestampMixin
from .users import slots_table,experience_table
from datetime import datetime
from app.models.users import User
from app.models.bid import Bid
from app.models.template import Template
from app.models.authority import Authority
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

template_table=Table(
    "template_table",
    Base.metadata,
    Column("template",ForeignKey("template.id"),primary_key=True),
    Column("slot",ForeignKey("slot.id"),primary_key=True),
)
class Slot(Base,TimestampMixin):
    __tablename__="slot"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(20))
    start_time:Mapped[datetime]
    end_time:Mapped[datetime]
    assignees:Mapped[Optional[list["User"]]]=relationship(secondary=slots_table,back_populates="slots")
    creater_id:Mapped[UUID]=mapped_column(ForeignKey("user.id",ondelete="SET NULL"))
    creater:Mapped["User"]=relationship(back_populates="create_slot")
    task_id:Mapped[UUID]=mapped_column(ForeignKey("task.id",ondelete="CASCADE"))
    task:Mapped["Task"]=relationship(back_populates="slot",uselist=False)
    bid:Mapped[Optional["Bid"]]=relationship(back_populates="slot",uselist=False)
    template:Mapped[list["Template"]]=relationship(secondary=template_table,back_populates="slots")
    
class Task(Base,TimestampMixin):
    __tablename__="task"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(20))
    detail:Mapped[str]=mapped_column(String(400))
    max_woker_num:Mapped[int]=mapped_column(default=1) #最大人数
    min_woker_num:Mapped[int]=mapped_column(default=1) #最少人数
    exp_woker_num:Mapped[int]=mapped_column(default=0) #必要な経験者の人数
    slot:Mapped[Optional[list["Slot"]]]=relationship(back_populates="task",cascade="all")
    expert:Mapped[Optional[list["User"]]]=relationship(secondary=experience_table,back_populates="exp_task")
    creater_id:Mapped[UUID]=mapped_column(ForeignKey("user.id",ondelete="SET NULL"))
    creater:Mapped["User"]=relationship(back_populates="create_task")
    authority:Mapped[Optional[list["Authority"]]]=relationship(secondary=authority_table,back_populates="task")
    tag:Mapped[Optional[list["TaskTag"]]]=relationship(secondary=tag_table,back_populates="task",lazy="joined")
    
class TaskTag(Base):
    __tablename__="tasktag"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(10))
    task:Mapped[Optional[list["Task"]]]=relationship(secondary=tag_table,back_populates="tag")