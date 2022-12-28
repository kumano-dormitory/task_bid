from fastapi import FastAPI
from app.models import User
from app.schemas.users import UserBase

from sqlalchemy.orm import Session

def user_all(db:Session):
    items=db.query(User).all()
    return items

def user_get(db:Session,name:str):
    item=db.query(User).filter(User.name==name).first()
    return item

def user_register(user:UserBase,db:Session):
    item = User(**user.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item