import cruds.user as crud
from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from schemas.users import UserBase
router=APIRouter()

@router.get("/")
async def user_list(db:Session=Depends(get_db)):
    return crud.user_all(db=db)

@router.post("/")
async def user_post(user:UserBase,db:Session=Depends(get_db)):
    return crud.user_post(user,db)

@router.get("/users/{user_id}")
async def user_one():
    pass

@router.put("/users/{user_id}")
async def update_user():
    pass