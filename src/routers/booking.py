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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bk1 = APIRouter()
db = SessionLocal()

@bk1.post("/book_tickets", response_model=bookingbase)
def book_tickets(book: bookingbase):
    logger.info(f"Booking tickets for user_id: {book.user_id}, tour_id: {book.tour_id}")
    total_price = str(int(book.number_of_people) * float(book.total_price_per_person))
    new_booking = Booking(
        user_id=book.user_id,
        tour_id=book.tour_id,
        booking_date=book.booking_date,
        number_of_people=book.number_of_people,
        total_price_per_person=book.total_price_per_person,
        total_price=total_price
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    logger.success(f"Booking created successfully with booking_id: {new_booking.booking_id}")
    return new_booking

@bk1.get("/get_booking_details", response_model=bookingbase)
def get_booking_details(booking_id: str):
    logger.info(f"Fetching booking details for booking_id: {booking_id}")
    db_booking = db.query(Booking).filter(Booking.booking_id == booking_id, Booking.is_active == True, Booking.is_deleted == False).first()
    if db_booking is None:
        logger.warning(f"Booking not found for booking_id: {booking_id}")
        raise HTTPException(status_code=404, detail="Details not found")
    return db_booking

@bk1.get("/all_booking_details/", response_model=List[bookingbase])
def all_booking_details():
    logger.info("Fetching all booking details")
    db_booking = db.query(Booking).filter(Booking.is_active == True, Booking.is_deleted == False).all()
    if not db_booking:
        logger.warning("No bookings found")
        raise HTTPException(status_code=404, detail="Booking failed!!!")
    logger.success(f"Fetched {len(db_booking)} bookings")
    return db_booking

@bk1.put("/update_booking_details/", response_model=bookingbase)
def update_booking(booking: bookingbase,booking_id :str):
    logger.info(f"Updating booking details for booking_id: {Booking.booking_id}")
    db_user = db.query(User).filter(User.id == booking.user_id).first()
    if db_user is None:
        logger.warning(f"User not found with user_id: {booking.user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    db_booking = db.query(Booking).filter(Booking.booking_id == Booking.booking_id).first()
    if db_booking is None:
        logger.warning(f"Booking not found with booking_id: {Booking.booking_id}")
        raise HTTPException(status_code=404, detail="Booking not found")

    db_booking.user_id = booking.user_id
    db_booking.tour_id = booking.tour_id
    db_booking.booking_date = booking.booking_date
    db_booking.number_of_people = booking.number_of_people
    db_booking.total_price_per_person = booking.total_price_per_person
    db_booking.total_price = str(int(booking.number_of_people) * float(booking.total_price_per_person))

    db.commit()
    db.refresh(db_booking)
    logger.success(f"Booking with booking_id: {Booking.booking_id} updated successfully")
    return db_booking

@bk1.delete("/cancel_booking/")
def cancel_booking(booking_id: str):
    logger.info(f"Cancelling booking with booking_id: {booking_id}")
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if not booking:
        logger.warning(f"Booking not found with booking_id: {booking_id}")
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.booking_status = "cancelled"
    db.delete(booking)
    db.commit()
    logger.success(f"Booking with booking_id: {booking_id} cancelled successfully")
    return f"Your order cancelled successfully!!!"
