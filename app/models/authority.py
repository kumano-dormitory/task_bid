from sqlalchemy import Column,String,Table,ForeignKey,DateTime,Text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .timestamp import TimestampMixin
from .users import slots_table
from .slot import authority_table


class Authority(Base,TimestampMixin):
    __tablename__="authority"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(30))
    task=relationship("Task",secondary=authority_table,back_populates="authority")