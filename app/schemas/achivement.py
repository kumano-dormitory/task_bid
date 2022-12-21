from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class Achivement(BaseModel):
    id:UUID
    term:int
    name:str
    