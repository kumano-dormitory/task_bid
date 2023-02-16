from sqlalchemy import String
from typing import Optional
from app.database import Base
from sqlalchemy.orm import relationship,Mapped,mapped_column
from uuid import uuid4,UUID
from .timestamp import TimestampMixin
from .slot import authority_table
from app.models.slot import Task

class Authority(Base,TimestampMixin):
    __tablename__="authority"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(30))
    task:Mapped[Optional[list["Task"]]]=relationship(secondary=authority_table,back_populates="authority")