from fastapi import FastAPI
from models import User
from schemas.users import UserBase

from sqlalchemy.orm import Session

def user_all(db:Session):
    items=db.query(User).all()
    return items

def user_post(user:UserBase,db:Session):
    item = User(**user.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item