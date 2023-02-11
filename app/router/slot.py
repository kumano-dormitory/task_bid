import app.cruds.user as crud
from fastapi import APIRouter,Depends,status
from fastapi.responses import JSONResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.users import UserBase,UserDisplay
from app.schemas.slot import SlotRequest
from app.router.auth import Token
from app.cruds.auth import oauth2_scheme,get_current_active_user
import app.cruds.slot as crud
from typing import Union
router=APIRouter()

@router.get("/")
async def slot_list(name:str|None=None,db:Session=Depends(get_db)):
    if name:
        slot=crud.slot_get(name,db)
        return slot
    slots=crud.slot_all(db)
    return slots
    


@router.get("/slots/{user_id}")
async def slot_one():
    pass


@router.put("/slots/{user_id}")
async def update_slot():
    pass


@router.post("/")
async def slot_post(slot:SlotRequest,db:Session=Depends(get_db),user=Depends(get_current_active_user)):
    response=crud.slot_post(slot,db,user)
    return response