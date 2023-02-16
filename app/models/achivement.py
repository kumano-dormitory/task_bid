from sqlalchemy import String
from app.database import Base
from typing import Optional
from sqlalchemy.orm import relationship,mapped_column,Mapped
from uuid import uuid4,UUID
from .timestamp import TimestampMixin
from .users import achivement_table
from app.models.users import User


class Achivement(Base,TimestampMixin):
    __tablename__="achivement"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    term:Mapped[int]
    name:Mapped[str]=mapped_column(String(20))
    user:Mapped[Optional[list["User"]]]=relationship(secondary=achivement_table, back_populates="achivement")