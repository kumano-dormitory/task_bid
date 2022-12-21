from fastapi import APIRouter

router=APIRouter()

@router.get("/slots")
async def slot_list():
    pass


@router.get("/slots/{user_id}")
async def slot_one():
    pass


@router.put("/slots/{user_id}")
async def update_slot():
    pass


@router.post("/slots")
async def create_slot():
    pass