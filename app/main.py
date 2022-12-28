from typing import Union
from fastapi import FastAPI
from .router import achivement,authority,bid, slot, user,auth
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(achivement.router,prefix="/achivements")
app.include_router(authority.router,prefix="/authority")
app.include_router(bid.router,prefix="/bid")
app.include_router(slot.router,prefix="/slots")
app.include_router(user.router,prefix="/users")
app.include_router(auth.router,prefix="")