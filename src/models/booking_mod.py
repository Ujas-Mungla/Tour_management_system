from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, JSON,Text,Float
import uuid
from database.database import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship



class Booking(Base):
    __tablename__ = "booking"
    booking_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    tour_id = Column(String(50), ForeignKey("tours.tour_id"), nullable=False)
    booking_date = Column(DateTime, default=datetime.now, nullable=False)
    number_of_people = Column(String(200), nullable=False)
    total_price_per_person = Column(String(200), nullable=False)
    booking_status = Column(String(50), default="Confirm")
    total_price=Column(String(200),nullable=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)





