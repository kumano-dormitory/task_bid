from fastapi import FastAPI ,status,HTTPException
from app.models.authority import Authority
from app.models.slot import Task,TaskTag
from app.schemas.task import TaskCreate,TaskUpdate
from app.schemas.users import User
from sqlalchemy.orm import Session

async def task_all(db:Session):
    items=await db.query(Task).all()
    return items


async def task_get(name:str,db:Session):
    item=db.query(Task).filter(Task.name==name).first()
    return item

def task_response(task:Task):
    response_task={
        "id":task.id,
        "name":task.name,
        "detail":task.detail,
        "max_worker_num":task.max_woker_num,
        "min_worker_num":task.min_woker_num,
        "exp_worker_num":task.exp_woker_num,
        "creater_id":task.creater_id,
        "creater":task.creater.name
    }
    return response_task


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
    task=db.query(Task).filter(Task.id==task_id)
    old_task=task.first()
    if not old_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {task_id} found')
    task.update({
        Task.name:request.name if request.name else old_task.name,
        Task.detail:request.detail if request.detail else old_task.detail,
        Task.max_woker_num:request.max_woker_num if request.max_woker_num else old_task.max_woker_num,
        Task.min_woker_num:request.min_woker_num if request.min_woker_num else old_task.min_woker_num,
        Task.exp_woker_num:request.exp_woker_num if request.exp_woker_num else old_task.exp_woker_num,
    })
    db.commit()
    return task_response(task.first())


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

    