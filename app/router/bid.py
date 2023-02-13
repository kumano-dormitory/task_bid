from fastapi import APIRouter,Depends
from app.schemas.bid import BidRequest
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds.auth import get_current_active_user
import app.cruds.bid as crud
router=APIRouter()

@router.get("/")
async def bid_get(name:str|None=None,db:Session=Depends(get_db)):
    if name:
        bid=crud.bid_get(name,db)
        return bid
    bids=crud.bid_all(db)
    return bids
    
@router.post("/")
async def bid_post(bid:BidRequest,db:Session=Depends(get_db),user=Depends(get_current_active_user)):
    response=crud.bid_post(bid,db,user)
    return response


@router.post("/{bid_id}/tender")
async def bid_tender(bid_id:str,request,current_user=Depends(get_current_active_user),db:Session=Depends(get_db)):
    bid=crud.bid_tender(bid_id,request,current_user,db)
    return bid