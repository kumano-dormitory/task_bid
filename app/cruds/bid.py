import datetime
from fastapi import FastAPI, HTTPException, status
from app.models.models import User
from app.schemas.bid import BidRequest
from app.models.models import Bid, Bidder, Slot
from sqlalchemy.orm import Session
from app.cruds.response import (
    bids_response,
    bid_response,
    bidder_response,
    bids_response_for_user,
)
from app.cruds.slot import slot_response
import app.cruds.message as message
from sqlalchemy.future import select


def getbyid(bid_id: str, user: User, db: Session):
    bid = db.get(Bid, bid_id)
    bidder = db.scalars(
        select(Bidder)
        .filter(Bidder.user_id == user.id, Bidder.bid_id == bid_id)
        .limit(1)
    ).first()
    response = bid_response(bid)
    if bidder == None:
        response["user_bidpoint"] = "notyet"
        return response
    bid["user_bidpoint"] = bidder.point
    return response


def post(bid: BidRequest, db: Session, user: User):
    new_bid = Bid(
        name=bid.name,
        open_time=datetime.datetime(
            bid.open_time.year,
            bid.open_time.month,
            bid.open_time.day,
            bid.open_time.hour,
            bid.open_time.minute,
        ),
        close_time=datetime.datetime(
            bid.close_time.year,
            bid.close_time.month,
            bid.close_time.day,
            bid.close_time.hour,
            bid.close_time.minute,
        ),
        slot_id=bid.slot_id,
    )
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)
    return bid_response(new_bid)


def post_personal(bid: BidRequest, db: Session, user: User):
    new_bid = Bid(
        name=bid.name,
        open_time=datetime.datetime(
            bid.open_time.year,
            bid.open_time.month,
            bid.open_time.day,
            bid.open_time.hour,
            bid.open_time.minute,
        ),
        close_time=datetime.datetime(
            bid.close_time.year,
            bid.close_time.month,
            bid.close_time.day,
            bid.close_time.hour,
            bid.close_time.minute,
        ),
        slot_id=bid.slot_id,
    )
    db.add(new_bid)
    user.point -= new_bid.slot.task.buyout_point
    db.commit()
    db.refresh(new_bid)
    return bid_response(new_bid)


def all(db: Session):
    items = db.scalars(select(Bid)).all()
    respone_bids = [
        {
            "id": bid.id,
            "name": bid.name,
            "close_time": bid.close_time,
            "start_point": bid.slot.task.start_point,
        }
        for bid in items
    ]
    return respone_bids


def user_bidable(user: User, db: Session):
    opening_bids = (
        db.execute(
            select(Bid).filter(
                Bid.open_time<datetime.datetime.now(),
                Bid.close_time > datetime.datetime.now(),
            )
        )
        .scalars()
        .all()
    )
    all_bid=db.scalars(select(Bid)).all()
    return bids_response_for_user(opening_bids, user, db)


def get(name: str, db: Session):
    item = db.scalars(select(Bid).filter_by(name=name).limit(1)).first()
    respone_slot = bid_response(item)
    return respone_slot


def lack(user: User, db: Session):
    bids = db.execute(select(Bid).filter(Bid.is_complete)).scalars().all()
    lack_exp_bids = []
    lack_bids = []
    for bid in bids:
        slot = bid.slot
        assignees = slot.assignees
        task = slot.task
        exp_assignees = [
            exp_assignee
            for exp_assignee in assignees
            if task in exp_assignee.exp_task
        ]
        if task.min_woker_num > len(assignees):
            lack_bids.append(bid)
        if task.exp_woker_num > len(exp_assignees):
            lack_exp_bids.append(bid)
            continue

    return {
        "lack_bids": bids_response_for_user(lack_bids,user,db),
        "lack_exp_bids": bids_response_for_user(lack_exp_bids,user,db),
    }


def tender(bid_id: str, tender_point: int, user, db: Session):
    bid = db.get(Bid, bid_id)
    task = bid.slot.task
    exist_bidder = db.scalars(
        select(Bidder)
        .filter(Bidder.user_id == user.id, Bidder.bid_id == bid_id)
        .limit(1)
    ).first()
    if task in user.exp_task:
        if exist_bidder:  
            exist_bidder.point=tender_point
            db.commit()
            return bidder_response(exist_bidder)
        bidder = Bidder(point=tender_point)
        bidder.user = user
        bid.bidder.append(bidder)
        db.commit()
        return bidder_response(bidder)
    if exist_bidder:
        return bidder_response(exist_bidder)        
    bidder = Bidder(point=task.buyout_point)
    bidder.user = user
    bid.bidder.append(bidder)
    db.commit()
    return bidder_response(bidder)


def tenderlack(bid_id: str, user: User, db: Session):
    bid = db.get(Bid, bid_id)
    task = bid.slot.task
    slot = bid.slot
    bidder = bid.bidder
    if task in user.exp_task:
        if len(slot.assignees) >= task.min_woker_num:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

        bidder = Bidder(point=task.buyout_point - 1)
        bidder.user = user
        bid.bidder.append(bidder)
        slot.assignees.append(user)
        db.commit()
        return bidder_response(bidder)
    else:
        inexp_assignees = [
            user for user in slot.assignees if task not in user.exp_task
        ]
        if len(inexp_assignees) >= task.min_woker_num - task.exp_woker_num:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
        bidder = Bidder(point=task.buyout_point - 1)
        bidder.user = user
        bid.bidder.append(bidder)
        slot.assignees.append(user)
        db.commit()
        return bidder_response(bidder)


def close(bid_id: str, db: Session):
    bid = db.get(Bid, bid_id)
    if bid.is_complete:
        return None
    bid.is_complete = True
    db.commit()
    slot = bid.slot
    task = slot.task
    bidders = (
        db.execute(
            select(Bidder)
            .filter(Bidder.bid_id == bid_id)
            .order_by(Bidder.point)
        )
        .scalars()
        .all()
    )
    exp_bidders = []
    inexp_bidders = []
    for bidder in bidders:
        if task in bidder.user.exp_task:
            exp_bidders.append(bidder)
        else:
            inexp_bidders.append(bidder)
    exp_bidders_len = len(exp_bidders)
    not_exp_bidders_len = len(inexp_bidders)
    blank_len = task.min_woker_num - task.exp_woker_num

    if blank_len > not_exp_bidders_len + max(
        (exp_bidders_len - task.exp_woker_num, 0)
    ):
        message.alert_shortage(slot)
        for exp_bidder in exp_bidders:
            slot.assignees.append(exp_bidder.user)
        for not_exp in inexp_bidders:
            slot.assignees.append(not_exp.user)
        db.commit()
        return slot_response(slot)

    if exp_bidders_len < task.exp_woker_num:
        message.alert_exp_shortage(slot)
        for exp_bidder in exp_bidders:
            slot.assignees.append(exp_bidder.user)
        for index in range(
            min((task.max_woker_num - task.exp_woker_num, not_exp_bidders_len))
        ):
            slot.assignees.append(inexp_bidders[index].user)
        db.commit()
        return slot_response(slot)

    else:
        for index in range(task.exp_woker_num):
            slot.assignees.append(exp_bidders[index].user)

        if not_exp_bidders_len == 0:
            for index in range(task.exp_woker_num, task.min_woker_num):
                slot.assignees.append(exp_bidders[index].user)
            db.commit()
            return slot_response(slot)
        elif 1 <= not_exp_bidders_len and not_exp_bidders_len < blank_len:
            for index in range(not_exp_bidders_len):
                slot.assignees.append(inexp_bidders[index].user)
            for index in range(
                task.exp_woker_num,
                task.exp_woker_num + blank_len - not_exp_bidders_len,
            ):
                slot.assignees.append(exp_bidders[index].user)
            db.commit()
            return slot_response(slot)
        else:
            for index in range(
                min(
                    (
                        task.max_woker_num - task.exp_woker_num,
                        not_exp_bidders_len,
                    )
                )
            ):
                slot.assignees.append(inexp_bidders[index].user)
            db.commit()
            return slot_response(slot)


def assignee_convert(
    user_id: str, bid_id: str, request_user: User, db: Session
):
    bid = db.get(Bid, bid_id)
    slot = bid.slot
    cancel_user = db.get(User, user_id)
    if not cancel_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    bidder = db.scalars(
        select(Bidder)
        .filter(Bidder.bid_id == bid_id, Bidder.user_id == user_id)
        .limit(1)
    ).first()
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not bidder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not bidder.is_canceled:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"bidder.is_canceled is{bidder.is_canceled}",
        )
    bidder.user = request_user
    bidder.is_canceled = False
    slot.assignees.remove(cancel_user)
    slot.assignees.append(request_user)
    db.commit()
    return bidder_response(bidder)



def close_all_bid(db: Session):
    bids = (
        db.execute(
            select(Bid).filter(Bid.close_time < datetime.datetime.now())
        )
        .scalars()
        .all()
    )

    closed_bid_id_list = []
    for bid in bids:
        response = close(bid.id, db)
        if response != None:
            closed_bid_id_list.append(response["id"])
    return closed_bid_id_list
