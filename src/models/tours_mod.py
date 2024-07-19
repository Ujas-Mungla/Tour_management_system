from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, JSON,Text,Float
import uuid
from database.database import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship


class Tour(Base):
    __tablename__ = "tours"
    tour_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    tour_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    location = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)  # Duration in hours
    price = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # bookings = relationship('Booking', back_populates='tour')
    # addresses = relationship("Address", order_by="Address.id", back_populates="tour")
    # guides = relationship("TourGuider", back_populates="tour")



    