import datetime
from fastapi import FastAPI
from app.models.users import User
from app.schemas.slot import SlotRequest
from app.models.slot import Slot
from sqlalchemy.orm import Session
from app.cruds.user import creater_response,users_response


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
    items=db.query(Slot).all()
    respone_slots=[{
        "id":slot.id,
        "name":slot.name,
        "creater":slot.creater.name,
        "task":slot.task.name,
    } for slot in items]
    return respone_slots

def slot_get(name:str,db:Session):
    item=db.query(Slot).filter(Slot.name==name).first()
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



    