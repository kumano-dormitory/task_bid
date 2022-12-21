from sqlalchemy import Column,String,Integer
from conf.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from timestamp import TimestampMixin
import enum


class Achivement(Base,TimestampMixin):
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    term=Column(Integer)
    name=Column(String(20))