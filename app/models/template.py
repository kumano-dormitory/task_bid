from sqlalchemy import Column,String,Table,ForeignKey,Date,Text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .timestamp import TimestampMixin
from .slot import template_table


class Template(Base,TimestampMixin):
    __tablename__="template"
    id=Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    name=Column(String(20))
    slots=relationship("Slot",secondary=template_table,back_populates="template")