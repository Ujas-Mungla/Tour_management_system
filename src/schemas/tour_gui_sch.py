from pydantic import BaseModel,EmailStr,constr,Json,Field
from typing import List,Optional
from datetime import datetime,date
from src.models.tours_mod import Tour


class tour_guider_base(BaseModel):
    name : str
    email  : str
    phone : str


class tour_patch(BaseModel):
    tour_id :str