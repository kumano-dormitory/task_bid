from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.models.models import TaskTag
from sqlalchemy.future import select
from app.database import get_db
router=APIRouter()

@router.get("/")
async def tag_get(db:Session=Depends(get_db)):
    tasktag=db.execute(select(TaskTag)).scalars().all()
    return tasktag

@router.post("/")
async def tag_post(tagname:str,db:Session=Depends(get_db)):
    tag=TaskTag(name=tagname)
    db.add(tag)
    db.commit()
    return tag
    