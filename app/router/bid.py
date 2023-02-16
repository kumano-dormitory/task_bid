from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.bid import BidRequest,TenderRequest
from app.models.models import User
from app.models.models import Bid
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
async def bid_post(bid:BidRequest,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)):
    response=crud.bid_post(bid,db,user)
    return response


@router.post("/{bid_id}/tender")
async def bid_tender(bid_id:str,request:TenderRequest,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    bid=db.query(Bid).get(bid_id)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    response=crud.bid_tender(bid_id,request,current_user,db)
    return response

@router.post("/{bid_id}/close")
async def bid_close(bid_id:str,db:Session=Depends(get_db)):
    user=crud.bid_close(bid_id,db)
    return user