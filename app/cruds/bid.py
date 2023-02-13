import datetime
from fastapi import FastAPI
from app.models.users import User
from app.schemas.bid import BidRequest
from app.models.bid import Bid,Bidder
from sqlalchemy.orm import Session
from app.cruds.user import creater_response,users_response


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
    bidder=Bidder(bid_id=bid.id,user_id=user.id,point=request.tender_point)
    bid.bidder.append(bidder)
    db.commit()
    return bid