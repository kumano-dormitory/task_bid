from fastapi import APIRouter,Depends
from typing import Union,Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds import task as crud
from app.cruds import auth
from app.schemas.task import Task,TaskCreate,TaskList,TaskUpdate
from app.schemas.users import User
router=APIRouter()

@router.get("/")
async def task_get(name:Union[str,None]=None,db:Session=Depends(get_db)):
    if name:
        task=await crud.task_get(name,db)
        return task
    tasks=await crud.task_all(db)
    return tasks





@router.post("/",response_model=Task | None)
async def task_post(task:TaskCreate,db:Session=Depends(get_db),current_user:User=Depends(auth.get_current_active_user)):
    task=crud.task_post(task,current_user,db)
    return task


@router.patch("/{task_id}")
async def task_patch(task_id:str,task:TaskUpdate,db:Session=Depends(get_db)):
    task=crud.task_patch(task,task_id,db)
    return task