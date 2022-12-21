from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

class Authority(BaseModel):
    id:UUID
    name:str