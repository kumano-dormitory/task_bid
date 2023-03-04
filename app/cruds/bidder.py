from app.models.models import Bidder
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.future import select


def bidder_get(bid_id,user_id,db:Session):
    if bid_id and user_id:
        bidder=[jsonable_encoder(bidder) for bidder in db.scalars(select(Bidder).filter_by(bid_id=bid_id).filter_by(user_id=user_id)).one()]
    elif bid_id:
        bidder=[jsonable_encoder(bidder) for bidder in db.scalars(select(Bidder).filter_by(bid_id=bid_id)).all()]
    elif user_id:
        bidder=[jsonable_encoder(bidder) for bidder in db.scalars(select(Bidder).filter_by(user_id=user_id)).all()]
    else :
        bidder=[jsonable_encoder(bidder) for bidder in db.scalars(select(Bidder)).all()]
    return bidder

