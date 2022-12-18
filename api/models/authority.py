from sqlalchemy import Column,String,Table,ForeignKey,DateTime,Text
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from timestamp import TimestampMixin
from users import slots_table


class Authority(Base,TimestampMixin):
    __tablename__="user"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(30))
    