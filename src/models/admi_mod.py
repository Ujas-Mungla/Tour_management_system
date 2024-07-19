from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, JSON,Text
import uuid
from database.database import Base
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship


class Admin(Base):
    __tablename__ = "admin" 
    id=Column(String(50),primary_key=True,default=str(uuid.uuid4()))
    user_name= Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)



