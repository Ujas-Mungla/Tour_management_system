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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

tourss = APIRouter()
db = SessionLocal()

@tourss.post("/create_tours", response_model=TourBase)
def create_tours(tour: TourBase):
    logger.info("Creating a new tour")
    try:
        db_tour = Tour(
            tour_id=str(uuid.uuid4()),
            tour_name=tour.tour_name,
            description=tour.description,
            location=tour.location,
            duration=tour.duration,     
            price=tour.price
        )
        db.add(db_tour)
        db.commit()
        db.refresh(db_tour)
        logger.success(f"Tour created successfully: {db_tour.tour_id}")
        return db_tour
    except Exception as e:
        logger.error(f"Error creating tour: {e}")
        raise HTTPException(status_code=500, detail="Failed to create tour")

@tourss.get("/read_tour", response_model=TourBase)
def read_tour(tour_id: str):
    logger.info(f"Reading tour with id: {tour_id}")
    try:
        db_tour = db.query(Tour).filter(Tour.tour_id == tour_id).first()
        if db_tour is None:
            logger.warning(f"Tour not found: {tour_id}")
            raise HTTPException(status_code=404, detail="Tour not found")
        logger.success(f"Tour retrieved successfully: {db_tour.tour_id}")
        return db_tour
    except Exception as e:
        logger.error(f"Error reading tour: {e}")
        raise HTTPException(status_code=500, detail="Failed to read tour")

@tourss.patch("/update_tour/{tour_id}", response_model=TourBase)
def update_tour(tour_id: str, tour: TourBase):
    logger.info(f"Updating tour with id: {tour_id}")
    try:
        db_tour = db.query(Tour).filter(Tour.tour_id == tour_id).first()
        if db_tour is None:
            logger.warning(f"Tour not found: {tour_id}")
            raise HTTPException(status_code=404, detail="Tour not found")
        for key, value in tour.dict(exclude_unset=True).items():
            setattr(db_tour, key, value)
        db.commit()
        db.refresh(db_tour)
        logger.success(f"Tour updated successfully: {db_tour.tour_id}")
        return db_tour
    except Exception as e:
        logger.error(f"Error updating tour: {e}")
        raise HTTPException(status_code=500, detail="Failed to update tour")

@tourss.delete("/delete_tour")
def delete_tour(tour_id: str):
    logger.info(f"Deleting tour with id: {tour_id}")
    try:
        db_tour = db.query(Tour).filter(Tour.tour_id == tour_id).first()
        if db_tour is None:
            logger.warning(f"Tour not found: {tour_id}")
            raise HTTPException(status_code=404, detail="Tour not found")
        db.delete(db_tour)
        db.commit()
        logger.success(f"Tour deleted successfully: {tour_id}")
        return {"message": "Tour deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting tour: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete tour")
