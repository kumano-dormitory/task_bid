import datetime
from fastapi import FastAPI
from app.models.users import User
from app.schemas.bid import BidRequest
from app.models.bid import Bid,Bidder
from sqlalchemy.orm import Session
from app.cruds.user import creater_response,users_response
from app.cruds.bidder import bidder_response
import app.cruds.message as message

def bid_response(bid:Bid):
    response={
        "id":bid.id,
        "name":bid.name,
        "open_time":{
            "year":bid.open_time.year,
            "month":bid.open_time.month,
            "day":bid.open_time.day,
            "hour":bid.open_time.hour,
            "minute":bid.open_time.minute,
        },
        "close_time":{
            "year":bid.close_time.year,
            "month":bid.close_time.month,
            "day":bid.close_time.day,
            "hour":bid.close_time.hour,
            "minute":bid.close_time.minute,
        },
        "slot":{
            "id":bid.slot_id,
            "name":bid.slot.name,
        },
        "start_point":bid.start_point,
        "buyout_point":bid.buyout_point,
        "is_complete":bid.is_complete,
        "bidder":bid.bidder
    }
    return response    


def bid_post(bid:BidRequest,db:Session,user:User):
    bid=Bid(name=bid.name,
              open_time=datetime.datetime(bid.open_time.year,
                                           bid.open_time.month,
                                           bid.open_time.day,
                                           bid.open_time.hour,
                                           bid.open_time.minute),
              close_time=datetime.datetime(bid.close_time.year,
                                           bid.close_time.month,
                                           bid.close_time.day,
                                           bid.close_time.hour,
                                           bid.close_time.minute),
              start_point=bid.start_point,
              buyout_point=bid.buyout_point,
              slot_id=bid.slot)
    db.add(bid)
    db.commit()
    db.refresh(bid)
    return bid_response(bid)


def bid_all(db:Session):
    items=db.query(Bid).all()
    respone_bids=[{
        "id":bid.id,
        "name":bid.name,
        "close_time":bid.close_time,
        "start_point":bid.start_point, 
    } for bid in items]
    return respone_bids


def bid_get(name:str,db:Session):
    item=db.query(Bid).filter(Bid.name==name).first()
    respone_slot=bid_response(item)
    return respone_slot


def bid_tender(bid_id:str,request,user,db:Session):
    bid=db.query(Bid).get(bid_id)
    task=bid.slot.task
    if task in user.exp_task:
        bidder=Bidder(point=request.tender_point)
        bidder.user=user
        bid.bidder.append(bidder)
        db.commit()
        return bidder_response(bidder)
    bidder=Bidder(point=bid.buyout_point)
    bidder.user=user
    bid.bidder.append(bidder)
    db.commit()
    return bidder_response(bidder)


def bid_close(bid_id:str,db:Session):
    bid=db.query(Bid).get(bid_id)
    slot=bid.slot
    task=slot.task
    bidders=bid.bidder
    exp_bidders=[bidder for bidder in bidders if task in bidder.user.exp_task ]
    if len(exp_bidders)<task.exp_woker_num:
        message.alert_exp_shortage()
        for exp_bidder in exp_bidders:
            slot.assignees.append(exp_bidder.user)
    pass
            