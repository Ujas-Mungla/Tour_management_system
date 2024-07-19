from pydantic import BaseModel,EmailStr,constr,Json,Field
from typing import List,Optional
from datetime import datetime,date

class AddressBase(BaseModel):
    user_id: str
    tour_id: str
    address: str
    city: str
    state: str
    pincode: str
    country: str


class AddrPatch(BaseModel):
    user_id :Optional [str] =None
    tour_id:Optional[ str ] =None
    address:Optional[ str ] =None
    city:Optional[ str ] =None
    state:Optional[ str ] =None
    pincode:Optional[ str ] =None
    country: Optional[str] =None         