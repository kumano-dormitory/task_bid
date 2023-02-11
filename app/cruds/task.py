from fastapi import FastAPI
from app.models.authority import Authority
from app.models.slot import Task,TaskTag
from app.schemas.task import TaskCreate,TaskUpdate
from app.schemas.users import User
from sqlalchemy.orm import Session

def task_all(db:Session):
    items=db.query(Task).all()
    return items


def task_get(name:str,db:Session):
    item=db.query(Task).filter(Task.name==name).first()
    return item


def task_post(task:TaskCreate,current_user:User,db:Session):
    task=Task(creater=current_user, **task.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def task_delete(name:str,db:Session):
    db.query(Task).filter(Task.name==name).delete()
    db.commit()
    return name


def task_patch(request:TaskUpdate,task_id:str,db:Session):
    task=db.query(Task).get(task_id)
    task.update({
        Task.name:request.name if request.name else task.name,
        Task.detail:request.detail if request.detail else task.detail,
        Task.max_woker_num:request.max_woker_num if request.max_woker_num else task.max_woker_num,
        Task.min_woker_num:request.min_woker_num if request.min_woker_num else task.min_woker_num,
        Task.exp_woker_num:request.exp_woker_num if request.exp_woker_num else task.exp_woker_num,
    })
    db.commit()
    return task


def task_add_authority(request:list[str],task_id:str,db:Session):
    task=db.query(Task).get(task_id)
    new_authority=[]
    for authority_id in request:
        authority=db.query(Authority).get(authority_id)
        new_authority.append(authority)
    task.authority=list(set(new_authority))
    db.commit()
    return task


def task_add_tag(request:list[str],task_id:str,db:Session):
    task=db.query(Task).get(task_id)
    new_tag=[]
    for tag_id in request:
        tag=db.query(TaskTag).get(tag_id)
        new_tag.append(tag)
    task.tag=list(set(new_tag))
    db.commit()
    return task

    