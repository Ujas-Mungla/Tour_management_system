from fastapi import FastAPI, HTTPException, APIRouter, Depends, Security
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
import logging
from database.database import SessionLocal
from src.schemas.tour_sch import TourBase 
from logs.log_config import logger
from src.models.tours_mod import Tour
import uuid
from src.schemas.book_sch import bookingbase
from src.models.booking_mod import Booking
from src.models.user_mod import User
from src.models.tour_guider import TourGuider
from src.schemas.tour_gui_sch import tour_guider_base, tour_patch

db = SessionLocal()
tour_guider = APIRouter()

@tour_guider.post("/create_tour_guider", response_model=tour_guider_base)
def book_tickets(t_guider: tour_guider_base):
    logger.info("Creating a new tour guider")
    try:
        new_tour_guider = TourGuider(
            name=t_guider.name,
            email=t_guider.email,
            phone=t_guider.phone,
        )
        db.add(new_tour_guider)
        db.commit()
        logger.success(f"Tour guider {new_tour_guider.id} created successfully")
        return new_tour_guider
    except Exception as e:
        logger.error(f"Error creating tour guider: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@tour_guider.get("/get_tour_guider_details", response_model=tour_guider_base)
def get_booking_details(tour_guider_id: str):
    logger.info(f"Fetching details for tour guider ID: {tour_guider_id}")
    db_tour_guider = db.query(TourGuider).filter(TourGuider.id == tour_guider_id, TourGuider.is_active == False, TourGuider.is_deleted == True).first()
    if db_tour_guider is None:
        logger.warning(f"Tour guider ID: {tour_guider_id} not found")
        raise HTTPException(status_code=404, detail="Tour guider not found")
    logger.success(f"Details fetched for tour guider ID: {tour_guider_id}")
    return db_tour_guider

@tour_guider.get("/get_all_tour_guider_details/", response_model=List[tour_guider_base])
def all_booking_details():
    logger.info("Fetching all tour guider details")
    db_tour_guider = db.query(TourGuider).filter(TourGuider.is_active == False, TourGuider.is_deleted == True).all()
    if not db_tour_guider:
        logger.warning("No tour guiders found")
        raise HTTPException(status_code=404, detail="Tour guiders not found")
    logger.success(f"{len(db_tour_guider)} tour guiders found Successfully!!!")
    return db_tour_guider

@tour_guider.put("/update_tour_guider_details")
def update_tour_guider_details(t_guider: tour_guider_base, tour_guider_id: str):
    logger.info(f"Updating details for tour guider ID: {tour_guider_id}")
    db_tour_guider = db.query(TourGuider).filter(TourGuider.id == tour_guider_id, TourGuider.is_active == False, TourGuider.is_deleted == True).first()
    if db_tour_guider is None:
        logger.warning(f"Tour guider ID: {tour_guider_id} not found")
        raise HTTPException(status_code=404, detail="Tour Guider Not Found")
    db_tour_guider.name = t_guider.name
    db_tour_guider.email = t_guider.email
    db_tour_guider.phone = t_guider.phone
    db.commit()
    db.refresh(db_tour_guider)
    logger.success(f"Tour guider ID: {tour_guider_id} updated successfully")
    return {"message": "Your detail changed successfully!"}

@tour_guider.patch("/update_tour_guider_patch_details", response_model=tour_patch)
def update_address(tour_guider_id: str, ad: tour_patch):
    logger.info(f"Patching details for tour guider ID: {tour_guider_id}")
    db_tour_guider = db.query(TourGuider).filter(TourGuider.id == tour_guider_id).first()
    if db_tour_guider is None:
        logger.warning(f"Tour guider ID: {tour_guider_id} not found")
        raise HTTPException(status_code=404, detail="Tour guider not found")
    for key, value in ad.dict(exclude_unset=True).items():
        setattr(db_tour_guider, key, value)
    db_tour_guider.is_active = True
    db_tour_guider.is_deleted = False
    db.commit()
    db.refresh(db_tour_guider)
    logger.success(f"Tour guider ID: {tour_guider_id} patched successfully")
    return db_tour_guider

@tour_guider.delete("/delete_tour_guider")
def delete_tour_guider(tour_guider_id: str):
    logger.info(f"Deleting tour guider ID: {tour_guider_id}")
    db_tour_guider = db.query(TourGuider).filter(TourGuider.id == tour_guider_id).first()
    if db_tour_guider is None:
        logger.warning(f"Tour guider ID: {tour_guider_id} not found")
        raise HTTPException(status_code=404, detail="Tour guider not found")
    db.delete(db_tour_guider)
    db.commit()
    logger.success(f"Tour guider ID: {tour_guider_id} deleted successfully")
    return {"message": "Tour guider deleted successfully"}
