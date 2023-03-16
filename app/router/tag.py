from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.models.models import TaskTag,User
from sqlalchemy.future import select
from app.database import get_db
from app.cruds.auth import check_authority,get_current_active_user
router=APIRouter()

@router.get("/")
async def tag_get(db:Session=Depends(get_db)):
    tasktag=db.execute(select(TaskTag)).scalars().all()
    return tasktag

@router.post("/")
async def tag_post(tagname:str,user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    if check_authority(user,"POST","/tags/"):
        tag=TaskTag(name=tagname)
        db.add(tag)
        db.commit()
        return tag
    