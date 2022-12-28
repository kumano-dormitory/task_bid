from sqlalchemy import Column,String,Boolean, Table,ForeignKey,DateTime,Integer
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .timestamp import TimestampMixin
from .users import slots_table


class Bid(Base,TimestampMixin):
    __tablename__="bid"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(20))
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    slot=relationship("Slot",back_populates="bid",uselist=False)
    start_point=Column(Integer,default=0)
    lowest_point=Column(Integer,default=0)
    second_point=Column(Integer,default=0)
    buyout_point=Column(Integer,default=0)
    is_complete=Column(Boolean,default=False)
    lowest_user_id=Column(UUIDType(binary=False),ForeignKey("user.id"))
    lowest_user=relationship("User",back_populates="bid")
    
    