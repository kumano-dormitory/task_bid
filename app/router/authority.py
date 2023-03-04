from fastapi import APIRouter
from app.models.models import Authority,Method,User
from sqlalchemy.orm import Session
from fastapi import Depends
from app.cruds.auth import get_current_active_user,check_authority,authority_post
from app.database import get_db
from sqlalchemy.future import select
from app.schemas.authority import AuthorityRequest                                   

router=APIRouter()

@router.get("/")
async def authority_list(user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    return db.execute(select(Authority)).scalars().all()

@router.post("/")
async def authority_post(request:AuthorityRequest,user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    if check_authority(user,'POST','/authority/') | user.name=="恒川平":
        response=authority_post(request,user,db)
        return response
