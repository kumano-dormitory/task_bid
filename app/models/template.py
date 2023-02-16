from sqlalchemy import String
from typing import Optional
from app.database import Base
from sqlalchemy.orm import relationship,mapped_column,Mapped
from uuid import uuid4,UUID
from .timestamp import TimestampMixin
from .slot import template_table
from app.models.slot import Slot


class Template(Base,TimestampMixin):
    __tablename__="template"
    id:Mapped[UUID]=mapped_column(primary_key=True,default=uuid4)
    name:Mapped[str]=mapped_column(String(20))
    slots:Mapped[Optional[list["Slot"]]]=relationship(secondary=template_table,back_populates="template")