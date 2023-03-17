from sqlalchemy import String, Column, Table, ForeignKey
from app.database import Base
from typing import Optional
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from uuid import uuid4
from datetime import datetime
import enum

authority_table = Table(
    "authority_table",
    Base.metadata,
    Column("task", ForeignKey("task.id"), primary_key=True),
    Column("authority", ForeignKey("authority.id"), primary_key=True),
)

tag_table = Table(
    "tasktag_table",
    Base.metadata,
    Column("task", ForeignKey("task.id"), primary_key=True),
    Column("tasktag", ForeignKey("tasktag.id"), primary_key=True),
)

template_table = Table(
    "template_table",
    Base.metadata,
    Column("template", ForeignKey("template.id")),
    Column("slot", ForeignKey("slot.id")),
)


achivement_table = Table(
    "achivement_table",
    Base.metadata,
    Column("user", ForeignKey("user.id"), primary_key=True),
    Column("achivement", ForeignKey("achivement.id"), primary_key=True),
)

experience_table = Table(
    "experience_table",
    Base.metadata,
    Column("user", ForeignKey("user.id"), primary_key=True),
    Column("task", ForeignKey("task.id"), primary_key=True),
)

slots_table = Table(
    "slots_table",
    Base.metadata,
    Column("user", ForeignKey("user.id")),
    Column("slot", ForeignKey("slot.id")),
)


class Achivement(Base):
    __tablename__ = "achivement"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    term: Mapped[int]
    name: Mapped[str] = mapped_column(String(20))
    user: Mapped[Optional[list["User"]]] = relationship(
        secondary=achivement_table, back_populates="achivement"
    )


class Method(str, enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class Authority(Base):
    __tablename__ = "authority"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(30))
    method: Mapped["Method"]
    task: Mapped[Optional[list["Task"]]] = relationship(
        secondary=authority_table, back_populates="authority"
    )


class Bid(Base):
    __tablename__ = "bid"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    open_time: Mapped[datetime]
    close_time: Mapped[datetime]
    slot_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("slot.id", ondelete="SET NULL")
    )
    slot: Mapped["Slot"] = relationship(back_populates="bid")
    is_complete: Mapped[bool] = mapped_column(default=False)
    bidder: Mapped[Optional[list["Bidder"]]] = relationship(
        back_populates="bid", cascade="all,delete"
    )


class Bidder(Base):
    __tablename__ = "bidder"
    bid_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bid.id", ondelete="CASCADE"), primary_key=True
    )
    bid: Mapped["Bid"] = relationship(back_populates="bidder")
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    user: Mapped["User"] = relationship(back_populates="bid")
    point: Mapped[int] = mapped_column(default=0)
    is_canceled: Mapped[bool] = mapped_column(default=False)


class Slot(Base):
    __tablename__ = "slot"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    assignees: Mapped[Optional[list["User"]]] = relationship(
        secondary=slots_table, back_populates="slots"
    )
    creater_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    creater: Mapped[Optional["User"]] = relationship(
        back_populates="create_slot"
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE")
    )
    task: Mapped["Task"] = relationship(back_populates="slot", uselist=False)
    bid: Mapped[Optional["Bid"]] = relationship(
        back_populates="slot", uselist=False,cascade="all,delete"
    )
    template: Mapped[list["Template"]|None] = relationship(
        secondary=template_table, back_populates="slots"
    )


class Task(Base):
    __tablename__ = "task"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    detail: Mapped[str] = mapped_column(String(400))
    max_woker_num: Mapped[int] = mapped_column(default=1)  # 最大人数
    min_woker_num: Mapped[int] = mapped_column(default=1)  # 最少人数
    exp_woker_num: Mapped[int] = mapped_column(default=0)  # 必要な経験者の人数
    start_point: Mapped[int] = mapped_column(default=0)
    buyout_point: Mapped[int] = mapped_column(default=0)
    slot: Mapped[list["Slot"]|None] = relationship(
        back_populates="task", cascade="all,delete"
    )
    expert: Mapped[Optional[list["User"]]] = relationship(
        secondary=experience_table, back_populates="exp_task"
    )
    creater_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    creater: Mapped[Optional["User"]] = relationship(
        back_populates="create_task"
    )
    authority: Mapped[Optional[list["Authority"]]] = relationship(
        secondary=authority_table, back_populates="task"
    )
    tag: Mapped[Optional[list["TaskTag"]]] = relationship(
        secondary=tag_table, back_populates="task", lazy="joined"
    )


class TaskTag(Base):
    __tablename__ = "tasktag"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(10))
    task: Mapped[Optional[list["Task"]]] = relationship(
        secondary=tag_table, back_populates="tag"
    )


class Template(Base):
    __tablename__ = "template"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    slots: Mapped[Optional[list["Slot"]]] = relationship(
        secondary=template_table, back_populates="template"
    )


class Block(str, enum.Enum):
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    B12 = "B12"
    B3 = "B3"
    B4 = "B4"
    C12 = "C12"
    C34 = "C34"


class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(400))
    block: Mapped["Block"]
    room_number: Mapped[str] = mapped_column(String(10))
    achivement: Mapped[Optional[list["Achivement"]]] = relationship(
        secondary=achivement_table, back_populates="user"
    )
    exp_task: Mapped[Optional[list["Task"]]] = relationship(
        secondary=experience_table, back_populates="expert"
    )
    slots: Mapped[Optional[list["Slot"]]] = relationship(
        secondary=slots_table, back_populates="assignees"
    )
    create_slot: Mapped[Optional[list["Slot"]]] = relationship(
        back_populates="creater"
    )
    create_task: Mapped[Optional[list["Task"]]] = relationship(
        back_populates="creater"
    )
    point: Mapped[int] = mapped_column(default=0)
    bid: Mapped[Optional[list["Bidder"]]] = relationship(
        back_populates="user", cascade="all"
    )
    is_active: Mapped[bool] = mapped_column(default=True)

    def has_exp(self, task: Task):
        return task in self.exp_task
