from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, JSON,Text,Float
import uuid
from database.database import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship



class TourGuider(Base):
    __tablename__ = "tour_guider"
    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    tour_id = Column(String(50), ForeignKey("tours.tour_id"), nullable=True)
    # tour = relationship("Tour", back_populates="guides")
    




