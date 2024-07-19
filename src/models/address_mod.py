from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, JSON,Text,Float
import uuid
from database.database import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = "address"
    address_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(50), ForeignKey("users.id"), nullable=False)
    tour_id = Column(String(50), ForeignKey("tours.tour_id"), nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    pincode = Column(String(10), nullable=False)
    country = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
   
    # tour = relationship("Tour", back_populates="addresses")
    # user = relationship("User", back_populates="addresses")
