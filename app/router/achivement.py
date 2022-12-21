from fastapi import APIRouter

router=APIRouter()

@router.get("/achivements")
async def achivement_list():
    pass

