import datetime
from fastapi import FastAPI,HTTPException,status
from app.models.models import User
from app.schemas.slot import SlotRequest
from app.models.models import Slot,Bidder,Bid
from sqlalchemy.orm import Session
from app.cruds.user import creater_response,users_response,user_response
from sqlalchemy.future import select

def slot_response(slot:Slot):
    response={
        "id":slot.id,
        "name":slot.name,
        "start_time":{
            "year":slot.start_time.year,
            "month":slot.start_time.month,
            "day":slot.start_time.day,
            "hour":slot.start_time.hour,
            "minute":slot.start_time.minute,
        },
        "end_time":{
            "year":slot.end_time.year,
            "month":slot.end_time.month,
            "day":slot.end_time.day,
            "hour":slot.end_time.hour,
            "minute":slot.end_time.minute,
        },
        "assignees":users_response(slot.assignees),
        "creater":creater_response(slot.creater),
        "task":slot.task,
        "bid":slot.bid,
        "template":slot.template
        
    }
    return response


def slot_all(db:Session):
    items=db.scalars(select(Slot)).all()
    respone_slots=[{
        "id":slot.id,
        "name":slot.name,
        "creater":slot.creater.name,
        "task":slot.task.name,
    } for slot in items]
    return respone_slots

def slot_get(name:str,db:Session):
    item=db.scalars(select(Slot).filter_by(name=name).limit(1)).first()
    respone_slot=slot_response(item)
    return respone_slot


def slot_post(slot:SlotRequest,db:Session,user:User):
    slot=Slot(name=slot.name,
              start_time=datetime.datetime(slot.start_time.year,
                                           slot.start_time.month,
                                           slot.start_time.day,
                                           slot.start_time.hour,
                                           slot.start_time.minute),
              end_time=datetime.datetime(slot.end_time.year,
                                           slot.end_time.month,
                                           slot.end_time.day,
                                           slot.end_time.hour,
                                           slot.end_time.minute),
              task_id=slot.task,
              creater_id=user.id)
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot_response(slot)

def slot_cancel(slot_id:str,user_id:str,db:Session):
    slot=db.get(Slot,slot_id)
    bid=slot.bid
    if bid is None:
        raise HTTPException(
            status_code =status.HTTP_405_METHOD_NOT_ALLOWED
        )
    bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid.id,Bidder.user_id==user_id).limit(1)).first()
    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    bidder.is_canceled=True
    db.commit()
    user=db.get(User,user_id)
    slot.assignees.remove(user)
    db.commit()
    return slot


def slot_reassign(slot_id:str,user_id:str,db:Session):
    slot=db.get(Slot,slot_id)
    bid=slot.bid
    if bid is None:
        raise HTTPException(
            status_code =status.HTTP_405_METHOD_NOT_ALLOWED
        )
    bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid.id,Bidder.user_id==user_id).limit(1)).first()
    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    bidder.is_canceled=False
    db.commit()
    user=db.get(User,user_id)
    slot.assignees.append(user)
    db.commit()
    return slot

    
def slot_complete(slot_id:str,user:User,db:Session):
    slot=db.get(Slot,slot_id)
    if slot.start_time > datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    slots = user.slots
    if slot not in slots:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    bid=slot.bid
    bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid.id,Bidder.user_id==user.id).limit(1)).first()
    slot.assignees.remove(user)
    user.exp_task.append(slot.task)
    user.point+=bidder.point
    db.commit()
    return user_response(user)