from fastapi import APIRouter

router=APIRouter()

@router.get("/authority")
async def authority_list():
    pass

@router.put("/users/{user_id}")
async def update_user():
    pass