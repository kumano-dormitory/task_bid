from fastapi import APIRouter

router=APIRouter()

@router.get("/users")
async def user_list():
    pass


@router.get("/users/{user_id}")
async def user_one():
    pass


@router.put("/users/{user_id}")
async def update_user():
    pass