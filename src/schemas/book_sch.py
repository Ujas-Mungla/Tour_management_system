from pydantic import BaseModel,EmailStr,constr,Json,Field
from typing import List,Optional
from datetime import datetime,date


class bookingbase(BaseModel):
    user_id : str
    tour_id : str
    booking_date: date
    number_of_people:str
    total_price_per_person:str
    


    



