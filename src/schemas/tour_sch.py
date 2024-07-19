from pydantic import BaseModel,EmailStr,constr,Json,Field
from typing import List,Optional
from datetime import datetime,date


class TourBase(BaseModel):
    tour_name: str
    description: str
    location: str
    duration: int
    price: float


