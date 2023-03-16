from fastapi import HTTPException,status
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.schemas.template import TemplateCreate
from app.models.models import Slot, Template, User, Bid
from app.schemas.template import TemplateGenRequest,TemplateBulkGenRequest

import datetime


def post(request: TemplateCreate, db: Session):
    slots = []
    for slot_id in request.slots:
        slot = db.get(Slot, slot_id)
        if not slot:
            continue
        slots.append(slot)
    template = Template(name=request.name, slots=slots)
    db.add(template)
    db.commit()
    return template


def generate_slots_from_template(
    latest_slot: Slot,
    slots: list[Slot],
    request: TemplateGenRequest,
    user: User,
    db: Session,
):
    time_error = datetime.datetime(
        request.first_day.year, request.first_day.month, request.first_day.day
    ) - datetime.datetime(
        latest_slot.start_time.year,
        latest_slot.start_time.month,
        latest_slot.start_time.day,
    )
    new_bids = []
    for slot in slots:
        generated_slot = Slot(
            name=slot.name,
            start_time=slot.start_time + time_error,
            end_time=slot.end_time + time_error,
            task_id=slot.task.id,
            creater_id=user.id,
        )
        db.add(generated_slot)
        generated_bid = Bid(
            name=f"{generated_slot.start_time.month}月{generated_slot.start_time.day}日{slot.name}",
            open_time=generated_slot.start_time - datetime.timedelta(days=8),
            close_time=generated_slot.start_time - datetime.timedelta(days=2),
            slot=generated_slot,
        )
        db.add(generated_bid)
        new_bids.append({"id": generated_bid.id, "name": generated_bid.name})
    db.commit()
    return new_bids


def bulk_generate_slots_from_template(
    template_id: str, request: TemplateBulkGenRequest, user: User, db: Session
):
    template = db.get(Template, template_id)
    slots = template.slots
    latest_slot = db.scalars(
        select(Slot)
        .join(Slot.template)
        .filter(Template.id == template_id)
        .order_by(Slot.start_time)
        .limit(1)
    ).first()
    if not latest_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="failed to load latest_slot"
        )
    new_bids=[]
    for day in request.first_days:
        one_request=TemplateGenRequest(
            first_day=day,
        )
        new_bid=generate_slots_from_template(latest_slot,slots,one_request,user,db)
        new_bids+=new_bid
    return new_bids