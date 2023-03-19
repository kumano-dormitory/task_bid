from fastapi import FastAPI, status, HTTPException
from app.models.models import Authority
from app.models.models import Task, TaskTag
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.users import User
from sqlalchemy import update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.future import select
from app.cruds.response import task_response, tasks_response


def all(db: Session):
    items = (
        db.scalars(select(Task).options(joinedload(Task.creater)))
        .unique()
        .all()
    )
    return tasks_response(items)


async def task_get(name: str, db: Session):
    item = db.scalars(select(Task).filter_by(name=name).limit(1)).first()
    return item


def post(task: TaskCreate, current_user: User, db: Session):
    task = Task(creater=current_user, **task.dict())
    db.add(task)
    db.commit()
    return task_response(task)


def delete(name: str, db: Session):
    db.scalars(select(Task).filter_by(name=name)).delete()
    db.commit()
    return name


def patch(request: TaskUpdate, task_id: str, db: Session):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No note with this id: {task_id} found",
        )
    start_point=task.start_point if not request.start_point else request.start_point
    buyout_point=task.buyout_point if not request.buyout_point else request.buyout_point
    if buyout_point > start_point:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    db.execute(
        update(Task)
        .where(Task.id == task_id)
        .values(
            name=request.name if request.name else task.name,
            detail=request.detail if request.detail else task.detail,
            max_woker_num=request.max_woker_num
            if request.max_woker_num
            else task.max_woker_num,
            min_woker_num=request.min_woker_num
            if request.min_woker_num
            else task.min_woker_num,
            exp_woker_num=request.exp_woker_num
            if request.exp_woker_num
            else task.exp_woker_num,
            start_point=request.start_point
            if request.start_point
            else task.start_point,
            buyout_point=request.buyout_point
            if request.buyout_point
            else task.buyout_point,
        )
        .execution_options(synchronize_session="evaluate")
    )
    db.commit()
    return task_response(task)


def add_authority(request: list[str], task_id: str, db: Session):
    task = db.get(Task, task_id)
    new_authority = []
    for authority_id in request:
        authority = db.get(Authority, authority_id)
        new_authority.append(authority)
    task.authority = list(set(new_authority))
    db.commit()
    return task


def add_tag(request: list[str], task_id: str, db: Session):
    task = db.get(Task, task_id)
    new_tag = []
    for tag_id in request:
        tag = db.get(TaskTag, tag_id)
        new_tag.append(tag)
    task.tag = list(set(new_tag))
    db.commit()
    return task
