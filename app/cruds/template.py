from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.schemas.template import TemplateCreate
from app.models.models import Slot, Template, User, Bid
from app.schemas.template import TemplateGenRequest
import datetime


def template_post(request: TemplateCreate, db: Session):
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
    template_id: str, request: TemplateGenRequest, user: User, db: Session
):
    template = db.get(Template, template_id)
    slots = template.slots
    latest_slot = db.scalars(
        select(Slot)
        .join(Slot.template)
        .filter(Template.id == template_id)
        .order_by(desc(Slot.start_time))
        .limit(1)
    ).first()
    time_error = datetime.datetime(
        request.first_day.year, request.first_day.month, request.first_day.day
    ) - datetime.datetime(
        latest_slot.start_time.year,
        latest_slot.start_time.month,
        latest_slot.start_time.day,
    )
    close_day = latest_slot.start_time - datetime.timedelta(days=2)
    new_bids = []
    for slot in slots:
        generated_slot = Slot(
            name=slot.name,
            start_time=slot.start_time + time_error,
            end_time=slot.end_time + time_error,
            task_id=slot.task,
            creater_id=user.id,
        )
        db.add(generated_slot)
        generated_bid = Bid(
            name=f"{generated_slot.start_time.month}月{generated_slot.start_time.day}日{slot.name}",
            open_time=datetime.datetime.now(),
            close_time=close_day,
            start_point=request.start_point,
            buyout_point=request.buyout_point,
            slot_id=generated_slot.id,
        )
        db.add(generated_bid)
        new_bids.append({"id": generated_bid.id, "name": generated_bid.name})
    db.commit()
    return new_bids
