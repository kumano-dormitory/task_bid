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
    open_time=Column(DateTime)
    close_time=Column(DateTime)
    slot_id=Column(UUIDType(binary=False),ForeignKey("slot.id",ondelete="CASCADE"))
    slot=relationship("Slot",back_populates="bid")
    start_point=Column(Integer,default=0)
    buyout_point=Column(Integer,default=0)
    is_complete=Column(Boolean,default=False)
    bidder=relationship("Bidder",back_populates="bid")
    
    
class Bidder(Base):
    __tablename__="bidder"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    bid_id=Column(ForeignKey("bid.id"),primary_key=True)
    bid=relationship("Bid",back_populates="bidder")
    user_id=Column(ForeignKey("user.id"),primary_key=True)
    user=relationship("User",back_populates="bid")
    point=Column(Integer,default=0)