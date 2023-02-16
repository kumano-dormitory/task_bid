from app.models.bid import Bidder
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
def bidder_response(bidder:Bidder):
    response={
        "bid_id":bidder.bid_id,
        "user_id":bidder.user_id,
        "point":bidder.point
    }
    return response

def bidder_get(bid_id,user_id,db:Session):
    if bid_id and user_id:
        bidder=[jsonable_encoder(bidder) for bidder in db.query(Bidder).filter(Bidder.bid_id==bid_id).filter(Bidder.user_id==user_id).all()]
    elif bid_id:
        bidder=[jsonable_encoder(bidder) for bidder in db.query(Bidder).filter(Bidder.bid_id==bid_id).all()]
    elif user_id:
        bidder=[jsonable_encoder(bidder) for bidder in db.query(Bidder).filter(Bidder.user_id==user_id).all()]
    else :bidder=[jsonable_encoder(bidder) for bidder in db.query(Bidder).all()]
    return bidder