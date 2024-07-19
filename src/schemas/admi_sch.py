from pydantic import BaseModel,EmailStr,constr,Json,Field
from typing import List,Optional
from datetime import datetime,date

class AdminBase(BaseModel):
    user_name: str
    password:str


class AdminBasePatch(BaseModel):
    user_name: Optional[str] = None
    password: Optional[str] = None
