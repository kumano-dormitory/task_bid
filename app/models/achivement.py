from sqlalchemy import Column,String,Integer
from conf.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .timestamp import TimestampMixin
from .users import achivement_table
import enum


class Achivement(Base,TimestampMixin):
    __tablename__="achivement"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    term=Column(Integer)
    name=Column(String(20))
    user=relationship("User",secondary=achivement_table, back_populates="achivement")