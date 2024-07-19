from pydantic import BaseModel,EmailStr,constr,Json,Field
from typing import List,Optional
from datetime import datetime,date

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    first_name:str
    last_name:str
    password: str



class Users(BaseModel):
   
    first_name :str
    last_name :str
    username :str
    email :str
    mobile_no :str  
    password :str   
    city :str

class UserUpdate(BaseModel):
    username:str
    password:str

class UsersPatch(BaseModel):
    first_name :Optional[str]=None
    last_name :Optional[str]=None
    username :Optional[str]=None
    email :Optional[str]=None
    mobile_no :Optional[str]=None
    city :Optional[str]=None

