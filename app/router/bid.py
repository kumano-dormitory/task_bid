from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.bid import BidRequest, TenderRequest, BidConvertRequest
from app.models.models import User
from app.models.models import Bid, Bidder
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds.auth import get_current_active_user
import app.cruds.bid as crud
import app.cruds.slot as crudslot
from app.cruds import auth
from sqlalchemy.future import select
import datetime

router = APIRouter()


@router.get("/")
async def bid_get(
    name: str | None = None,
    lack: bool | None = None,
    lack_exp: bool | None = None,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if name:
        bid = crud.get(name, db)
        return bid
    if lack:
        response = crud.lack(user, db)
        return response["lack_bids"]
    if lack_exp:
        response = crud.lack(user, db)
        return response["lack_exp_bids"]
    bids = crud.user_bidable(user, db)
    return bids


@router.get("/{bid_id}")
async def bid_getbyid(
    bid_id: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    bid = crud.getbyid(bid_id, user, db)
    return bid


@router.post("/")
async def bid_post(
    bid: BidRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    response = crud.post(bid, db, user)
    return response


@router.post("/personal")
async def bid_post_personal(
    bid: BidRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
):
    response = crud.post_personal(bid, db, user)
    return response


@router.post("/{bid_id}/tender")
async def bid_tender(
    bid_id: str,
    request: TenderRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    bid = db.get(Bid, bid_id)
    if bid.is_complete:
        raise HTTPException(status_code=status.HTTP_410_GONE)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    if (bid.open_time > datetime.datetime.now()) | (
        bid.close_time < datetime.datetime.now()
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="この仕事は参加申請時間外です"
        )
    if (
        request.tender_point
        < bid.slot.task.buyout_point | request.tender_point
        > bid.slot.task.start_point
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    response = crud.tender(bid_id, request.tender_point, current_user, db)
    return response


@router.post("/{bid_id}/tenderlack")
async def bid_tenderlack(
    bid_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    bid = db.get(Bid, bid_id)
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not bid.is_complete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if bid.slot.end_time < datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="この仕事は参加申請時間外です"
        )
    response = crud.tenderlack(bid_id, current_user, db)
    return response


@router.post("/{bid_id}/close")
async def bid_close(bid_id: str, db: Session = Depends(get_db)):
    slot = crud.close(bid_id, db)
    return slot


@router.patch("/{bid_id}/convert")
async def slot_convet(
    bid_id: str,
    request: BidConvertRequest,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    response = crud.assignee_convert(request.user_id, bid_id, user, db)
    return response
