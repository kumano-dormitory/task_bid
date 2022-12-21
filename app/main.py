from typing import Union
from fastapi import FastAPI
from router import achivement,authority,slot, user
app = FastAPI()

app.include_router(achivement.router)
app.include_router(authority.router)
app.include_router(slot.router)
app.include_router(user.router)