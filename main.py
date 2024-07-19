from fastapi import FastAPI, APIRouter
from src.routers.admin import adminn
from src.routers.user import user
from src.routers.user import Otp
from src.routers.tour import tourss
from src.routers.booking import bk1
from src.routers.address import addr
from src.routers.tour_guider import tour_guider
from src.routers.payment import pwdd



app = FastAPI()



app.include_router(adminn)
app.include_router(user)
app.include_router(Otp)
app.include_router(tourss)
app.include_router(bk1)
app.include_router(addr)
app.include_router(tour_guider)
app.include_router(pwdd)
