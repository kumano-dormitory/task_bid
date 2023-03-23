import app.cruds.user as crud
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.models import User, Bidder, Bid, Slot
from app.schemas.users import UserBase, UserDisplay
from app.schemas.slot import SlotUpdate, SlotRequest, SlotCancelRequest, SlotDeleteRequest
from app.router.auth import Token
from app.cruds.auth import oauth2_scheme, get_current_active_user
import app.cruds.slot as crud
from typing import Union
from sqlalchemy.future import select
from app.cruds.response import slot_response
router = APIRouter()


@router.get("/")
async def slot_list(
    name: str | None = None,
    end: bool | None = None,
    db: Session = Depends(get_db),
):
    if name:
        slot = crud.get(name, db)
        return slot
    if end:
        slot = crud.slot_finished(db)
    slots = crud.all(db)
    return slots


@router.get('/{slot_id}')
async def slot_get(slot_id:str,db:Session=Depends(get_db)):
    slot=db.get(Slot,slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return slot_response(slot)



@router.post("/")
async def slot_post(
    slot: SlotRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    response = crud.post(slot, db, user)
    return response




@router.post("/{slot_id}/cancel")
async def slot_cancel(
    slot_id: str,
    request: SlotCancelRequest,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    slot = crud.cancel(slot_id, user, request.premire_point, db)
    return slot


@router.post("/{slot_id}/reassign")
async def slot_reassign(
    slot_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    slot = crud.reassign(slot_id, user.id, db)
    return crud.slot_response(slot)


@router.post("/{slot_id}/complete")
async def slot_complete(
    slot_id: str,    
    done:bool=True,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    response = crud.complete(slot_id,done,user, db)
    return response

@router.patch('/{slot_id}')
async def slot_patch(
    slot_id:str,request:SlotUpdate,db:Session=Depends(get_db)
):
    slot=crud.patch(request,slot_id,db)
    return slot

@router.delete('/')
async def vain_slots_delete(prune:bool|None=None,expired:bool|None=None,db:Session=Depends(get_db)):
    if prune:
        prune_slots=crud.delete_prune_slots(db)
        return prune_slots
    elif expired:
        expired_slots=crud.delete_expired_slots(db)
        return expired_slots
    prune_slots=crud.delete_prune_slots(db)
    expired_slots=crud.delete_expired_slots(db)
    return prune_slots+expired_slots

@router.delete("/bulk")
async def slot_bulk_delete(request: SlotDeleteRequest, db: Session=Depends(get_db)):
    crud.bulk_delete(request.slots_id, db)
    return {"msg":"Successfully deleted."}
