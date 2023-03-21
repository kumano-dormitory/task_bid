import app.cruds.user as crud
from fastapi import APIRouter, Depends, status, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
import app.cruds.message as message
import app.cruds.slot as crud

router=APIRouter()

@router.post('/today')
async def today_slots(db:Session=Depends(get_db)):
    message.today_slots(db)
    return