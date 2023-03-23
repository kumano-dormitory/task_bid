import datetime
from fastapi import FastAPI, HTTPException, status
from app.models.models import User
from app.schemas.slot import SlotRequest, SlotUpdate
from app.models.models import Slot, Bidder, Task, Bid
from sqlalchemy.orm import Session
from app.cruds.response import (
    slots_response,
    slot_response,
    user_response,
    bidder_response,
)
from sqlalchemy.future import select
from app.cruds.bidder import bidder_get
from sqlalchemy import delete, update


def all(db: Session):
    items = db.scalars(select(Slot)).all()

    return slots_response(items)


def slot_finished(db: Session):
    item = (
        db.execute(
            select(Slot).filter(Slot.end_time < datetime.datetime.now())
        )
        .scalars()
        .all()
    )
    return slots_response(item)


def get(name: str, db: Session):
    item = db.scalars(select(Slot).filter_by(name=name).limit(1)).first()
    respone_slot = slot_response(item)
    return respone_slot


def post(slot: SlotRequest, db: Session, user: User):
    task = db.get(Task, slot.task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    slot = Slot(
        name=slot.name,
        start_time=datetime.datetime(
            slot.start_time.year,
            slot.start_time.month,
            slot.start_time.day,
            slot.start_time.hour,
            slot.start_time.minute,
        ),
        end_time=datetime.datetime(
            slot.end_time.year,
            slot.end_time.month,
            slot.end_time.day,
            slot.end_time.hour,
            slot.end_time.minute,
        ),
        task_id=slot.task_id,
        creater_id=user.id,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot_response(slot)


def patch(request: SlotUpdate, slot_id: str, db: Session):
    slot = db.get(Slot, slot_id)
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No note with this id: {slot_id} found",
        )
    task = db.get(Task, request.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    db.execute(
        update(Slot)
        .where(Slot.id == slot_id)
        .values(
            name=request.name if request.name else slot.name,
        )
        .execution_options(synchronize_session="evaluate")
    )
    slot.start_time = datetime.datetime(
        request.start_time.year,
        request.start_time.month,
        request.start_time.day,
        request.start_time.hour,
        request.start_time.minute,
    )
    slot.end_time = datetime.datetime(
        request.end_time.year,
        request.end_time.month,
        request.end_time.day,
        request.end_time.hour,
        request.end_time.minute,
    )
    slot.task = task
    db.commit()
    return slot_response(slot)


def cancel(slot_id: str, user: User, premire_point: int, db: Session):
    slot = db.get(Slot, slot_id)
    bid = slot.bid
    if bid is None:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    bidder = db.scalars(
        select(Bidder)
        .filter(Bidder.bid_id == bid.id, Bidder.user_id == user.id)
        .limit(1)
    ).first()
    if not bidder:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if bidder.is_canceled:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    bidder.is_canceled = True
    bidder.point += premire_point
    user.point -= premire_point
    db.commit()
    return slot_response(slot)


def reassign(slot_id: str, user_id: str, db: Session):
    slot = db.get(Slot, slot_id)
    bid = slot.bid
    if bid is None:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    bidder = db.scalars(
        select(Bidder)
        .filter(Bidder.bid_id == bid.id, Bidder.user_id == user_id)
        .limit(1)
    ).first()
    if not bidder:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    bidder.is_canceled = False
    db.commit()
    user = db.get(User, user_id)
    slot.assignees.append(user)
    db.commit()
    return slot


def complete(slot_id: str,done:bool, user: User, db: Session):
    slot = db.get(Slot, slot_id)
    if slot.start_time > datetime.datetime.now():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    slots = user.slots
    if slot not in slots:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    bid = slot.bid
    bidder = db.scalars(
        select(Bidder)
        .filter(Bidder.bid_id == bid.id, Bidder.user_id == user.id)
        .limit(1)
    ).first()
    slot.assignees.remove(user)
    if done:
        user.exp_task.append(slot.task)
        user.point += bidder.point
    db.commit()
    return user_response(user)



def bulk_delete(slots_id: list[str], db: Session):
    for slot_id in slots_id:
        slot = db.get(Slot, slot_id)
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"id:{slot_id} is not found",
            )
        if slot.template:
            continue
        db.delete(slot)
    db.commit()
    return


def delete_prune_slots(db: Session):
    prune_slots = []
    slots = db.scalars(select(Slot)).all()
    for slot in slots:
        if slot.template == [] and slot.bid == None:
            prune_slots.append({"id": slot.id, "name": slot.name})
            db.delete(slot)
    db.commit()
    return prune_slots


def delete_expired_slots(db: Session):
    slots = db.scalars(select(Slot)).all()
    expired_slots = []
    for slot in slots:
        if (
            slot.end_time < datetime.datetime.now()
            and slot.assignees == []
            and slot.template == []
        ):
            expired_slots.append({"id": slot.id, "name": slot.name})
            db.delete(slot)
    db.commit()
    return expired_slots
