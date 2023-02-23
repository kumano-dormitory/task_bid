from fastapi import FastAPI
from app.models.models import User
from app.models.models import Task
from app.schemas.users import UserBase
from app.cruds.auth import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import delete

def user_response(user:User):
    response_user={"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "achivement":user.achivement,
            "exp_task":user.exp_task,
            "slots":user.slots,
            "create_slot":user.create_slot,
            "create_task":user.create_task,
            "point":user.point,
            "bid":user.bid,
            "is_active":user.is_active}
    return response_user

def creater_response(user:User):
    response_user={"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,}
    return response_user

def users_response(users:list[User]):
    response_users=[{"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "point":user.point,
            "is_active":user.is_active} for user in users]
    return response_users

def user_all(db:Session):
    items=db.scalars(select(User)).all()
    response_users=[{"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "point":user.point,
            "is_active":user.is_active} for user in items]
    return response_users

def user_get(name:str,db:Session):
    item=db.scalars(select(User).filter_by(name=name).limit(1)).first()
    response_user=user_response(item)
    return response_user


def user_register(user:UserBase,db:Session):
    user.password=get_password_hash(user.password)
    item = User(**user.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    response_user=user_response(item)
    return response_user

def user_delete(name:str,db:Session):
    db.execute(delete(User).where(User.name==name))
    db.commit()
    return name


def add_user_exp_task(request,user:User,db:Session):
    user=db.get(User,user.id)
    for task_id in request.exp_task:
        task=db.get(Task,task_id)
        user.exp_task.append(task)
    db.commit()
    return user_response(user)