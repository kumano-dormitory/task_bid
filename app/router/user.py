import app.cruds.user as crud
from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users import UserBase,UserDisplay,AddUserTask
from app.router.auth import Token
from app.cruds.auth import oauth2_scheme,get_current_active_user
from typing import Union
router=APIRouter()


@router.get("/",response_model=UserDisplay | list[UserDisplay])
async def user_get_by_name(name:str|None = None,db:Session=Depends(get_db)):
    if name:
        user=crud.user_get(name,db)
        return user
    users=crud.user_all(db)
    return users


@router.get("/{user_id}",response_model=UserDisplay)
async def user_one(user_id,db:Session=Depends(get_db),token:Token=Depends(oauth2_scheme)):
    user=db.get(User,user_id)
    return user


@router.get("/me")
async def user_self(current_user:User=Depends(get_current_active_user)):
    return crud.user_response(current_user)


@router.delete("/",status_code=200)
async def user_delete(name:str,db:Session=Depends(get_db)):
    crud.user_delete(name,db)
    return {"name":name}


@router.patch("/task")
async def add_user_exp_task(request:AddUserTask,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)):
    user=crud.add_user_exp_task(request,user,db)
    return user


