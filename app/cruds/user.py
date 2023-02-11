from fastapi import FastAPI
from app.models.users import User
from app.models.slot import Task
from app.schemas.users import UserBase
from app.cruds.auth import get_password_hash
from sqlalchemy.orm import Session

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
            "bidder":user.bidder,
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
    items=db.query(User).all()
    response_users=[{"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "point":user.point,
            "is_active":user.is_active} for user in items]
    return response_users

def user_get(name:str,db:Session):
    item=db.query(User).filter(User.name==name).first()
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
    db.query(User).filter(User.name==name).delete()
    db.commit()
    return name


def add_user_exp_task(exp_task_ids:list[str],user:User,db:Session):
    user=db.query(User).get(user.id)
    for task_id in exp_task_ids:
        task=db.query(Task).get(task_id)
        user.exp_task.append(task)
    db.commit()
    return user_response(user)