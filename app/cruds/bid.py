import datetime
from fastapi import FastAPI,HTTPException,status
from app.models.models import User
from app.schemas.bid import BidRequest
from app.models.models import Bid,Bidder,Slot
from sqlalchemy.orm import Session
from app.cruds.response import bids_response,bid_response,bidder_response
from app.cruds.slot import slot_response
import app.cruds.message as message
from sqlalchemy.future import select



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


def bid_post_personal(bid:BidRequest,db:Session,user:User):
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
    user.point-=bid.buyout_point
    db.commit()
    db.refresh(bid)
    return bid_response(bid)



def bid_all(db:Session):
    items=db.scalars(select(Bid)).all()
    respone_bids=[{
        "id":bid.id,
        "name":bid.name,
        "close_time":bid.close_time,
        "start_point":bid.start_point, 
    } for bid in items]
    return respone_bids


def bid_user_bidable(user:User,db:Session):
    opening_bids=db.execute(select(Bid).filter(Bid.open_time<datetime.datetime.now(),Bid.close_time>datetime.datetime.now())).scalars().all()
    return bids_response(opening_bids)


    
def bid_get(name:str,db:Session):
    item=db.scalars(select(Bid).filter_by(name=name).limit(1)).first()
    respone_slot=bid_response(item)
    return respone_slot

def bid_lack(user:User,db:Session):
    bids=db.execute(select(Bid).filter(Bid.is_complete)).scalars().all()
    
    lack_exp_bids=[]
    lack_bids=[]
    for bid in bids:
        slot=bid.slot
        assignees=slot.assignees
        task=slot.task
        exp_assignees=[exp_assignee for exp_assignee in assignees if task in assignees.exp_task]
        if task.exp_woker_num>len(exp_assignees):
            lack_exp_bids.append(bid)
            continue
        elif task.min_woker_num > len(assignees):
            lack_bids.append(bid)
            continue
        
    return {"lack_bids":bids_response(lack_bids),"lack_exp_bids":bids_response(lack_exp_bids)}



def bid_tender(bid_id:str,tender_point:int,user,db:Session):
    
    bid=db.get(Bid,bid_id)
    task=bid.slot.task
    if bid.is_complete:
        slot=bid.slot
        if task in user.exp_task:
            if len(slot.assignees)>=task.min_woker_num:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            bidder=Bidder(point=tender_point)
            bidder.user=user
            bid.bidder.append(bidder)
            slot.assignees.append(user)
            db.commit()
            return bidder_response(bidder)
        else:
            inexp_assignees=[user for user in slot.assignees if task not in user.exp_task]
            if len(inexp_assignees)>=task.min_woker_num-task.exp_woker_num:
                raise  HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            bidder=Bidder(point=tender_point)
            bidder.user=user
            bid.bidder.append(bidder)
            slot.assignees.append(user)
            db.commit()
            return bidder_response(bidder)
    
    if task in user.exp_task:
        bidder=Bidder(point=tender_point)
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
    bid=db.get(Bid,bid_id)
    bid.is_complete=True
    db.commit()
    slot=bid.slot
    task=slot.task
    bidders=db.execute(select(Bidder).filter(Bidder.bid_id==bid_id)
                           .order_by(Bidder.point)).scalars().all()
    exp_bidders=[]
    inexp_bidders=[]
    for bidder in bidders:
        if task in bidder.user.exp_task:
            exp_bidders.append(bidder)
        else:
            inexp_bidders.append(bidder)
    exp_bidders_len=len(exp_bidders)
    not_exp_bidders_len=len(inexp_bidders)
    blank_len=task.min_woker_num-task.exp_woker_num
    
    if blank_len > not_exp_bidders_len+max((exp_bidders_len-task.exp_woker_num,0)):
        message.alert_shortage()
        for exp_bidder in exp_bidders:
            slot.assignees.append(exp_bidder)
        for not_exp in inexp_bidders:
            slot.assignees.append(not_exp)
        db.commit()
        return slot_response(slot)
        
    if exp_bidders_len<task.exp_woker_num:
        message.alert_exp_shortage()
        for exp_bidder in exp_bidders:
            slot.assignees.append(exp_bidder.user)
        for index in range(min((task.max_woker_num-task.exp_woker_num,not_exp_bidders_len))):
                slot.assignees.append(inexp_bidders[index].user)
        db.commit()
        return slot_response(slot)
        
    else:
        for index in range(task.exp_woker_num):
            slot.assignees.append(exp_bidders[index].user)
            
        if not_exp_bidders_len==0:
            for index in range(task.exp_woker_num,task.min_woker_num):
                slot.assignees.append(exp_bidders[index].user)
            db.commit()
            return slot_response(slot)
        elif 1<= not_exp_bidders_len and not_exp_bidders_len < blank_len:
            for index in range(not_exp_bidders_len):
                slot.assignees.append(inexp_bidders[index].user)
            for index in range(task.exp_woker_num,task.exp_woker_num+blank_len-not_exp_bidders_len):
                slot.assignees.append(exp_bidders[index].user)
            db.commit()
            return slot_response(slot)
        else:
            for index in range(min((task.max_woker_num-task.exp_woker_num,not_exp_bidders_len))):
                slot.assignees.append(inexp_bidders[index].user)
            db.commit()
            return slot_response(slot)
        
def bid_cancel():
    pass
        
                
        
        
            
            
            