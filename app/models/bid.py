from sqlalchemy import String,ForeignKey
from typing import Optional
from sqlalchemy.orm import relationship,mapped_column,Mapped
from app.database import Base
from uuid import uuid4,UUID
from .timestamp import TimestampMixin
from datetime import datetime
from app.models.slot import Slot
from app.models.users import User

class Bid(Base,TimestampMixin):
    __tablename__="bid"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(20))
    open_time:Mapped[datetime]
    close_time:Mapped[datetime]
    slot_id:Mapped[UUID]=mapped_column(ForeignKey("slot.id",ondelete="CASCADE"))
    slot:Mapped["Slot"]=relationship(back_populates="bid")
    start_point:Mapped[int]=mapped_column(default=0)
    buyout_point:Mapped[int]=mapped_column(default=0)
    is_complete:Mapped[bool]=mapped_column(default=False)
    bidder:Mapped[Optional[list["Bidder"]]]=relationship(back_populates="bid",cascade="all")
    
    
class Bidder(Base):
    __tablename__="bidder"
    bid_id:Mapped[UUID]=mapped_column(ForeignKey("bid.id",ondelete="CASCADE"),primary_key=True)
    bid:Mapped["Bid"]=relationship(back_populates="bidder")
    user_id:Mapped[UUID]=mapped_column(ForeignKey("user.id",ondelete="CASCADE"),primary_key=True)
    user:Mapped["User"]=relationship(back_populates="bid")
    point:Mapped[int]=mapped_column(default=0)