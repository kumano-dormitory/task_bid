from fastapi import APIRouter, Depends,HTTPException,status
from typing import Union, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds import task as crud
from app.cruds import auth
from app.schemas.task import TaskCreate, TaskList, TaskUpdate
from app.schemas.users import User
from app.models.models import Task
from app.cruds.response import task_response
router = APIRouter()


@router.get("/")
async def task_get(name: str | None = None, db: Session = Depends(get_db)):
    if name:
        task = crud.task_get(name, db)
        return task
    tasks = crud.all(db)
    return tasks


@router.post("/")
async def task_post(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_active_user),
):
    if task.buyout_point>task.start_point:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    if auth.check_authority(current_user, method="POST", url="/tasks/"):
        task = crud.post(task, current_user, db)
        return task


@router.patch("/{task_id}")
async def task_patch(
    task_id: str, task: TaskUpdate, db: Session = Depends(get_db)
):
    
    task = crud.patch(task, task_id, db)
    return task

@router.delete('/{task_id}')
async def task_delete(
    task_id:str,db:Session=Depends(get_db)
):
    task=db.get(Task,task_id)
    db.delete(task)
    db.commit()
    return task_response