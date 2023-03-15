from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds import template as crud
from app.cruds.response import (
    template_response,
    templates_response,
    slot_response,
)
from app.cruds.auth import get_current_active_user
from app.schemas.template import TemplateCreate, TemplateBulkGenRequest
from app.schemas.users import User
from app.models.models import Template, Slot
from sqlalchemy.future import select
from sqlalchemy import delete

router = APIRouter()


@router.get("/")
async def template_get(db: Session = Depends(get_db)):
    templates = db.execute(select(Template)).scalars().all()
    return templates_response(templates)


@router.get("/{template_id}")
async def template_get_one(template_id: str, db: Session = Depends(get_db)):
    template = db.get(Template, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return jsonable_encoder(template)


@router.post("/")
async def template_post(
    request: TemplateCreate, db: Session = Depends(get_db)
):
    template = crud.post(request, db)
    return template_response(template)


@router.post("/{template_id}/generate")
async def generate_slots_from_template(
    template_id: str,
    request: TemplateBulkGenRequest,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    response = crud.bulk_generate_slots_from_template(
        template_id, request, user, db
    )
    return response


@router.delete("/{template_id}")
async def template_delete(template_id: str, db: Session = Depends(get_db)):
    template = db.get(Template,template_id)
    db.delete(template)
    db.commit()
    return {"id": template.id, "name": template.name}


@router.delete("/{template_id}/slots/{slot_id}")
async def template_delete(
    template_id: str, slot_id: str, db: Session = Depends(get_db)
):
    template = db.get(Template, template_id)
    slot = db.get(Slot, slot_id)
    template.slots.remove(slot)
    db.commit()
    return slot_response(slot)
