from sqlalchemy import Column, ForeignKey ,String,Float,DateTime,JSON
from app.core.database import Base
import uuid
from datetime import datetime,timedelta
from sqlalchemy.orm import relationship

class Request(Base):
    __tablename__ = "requests"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False,index=True)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False)
    prescription_image = Column(String,nullable=True)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime,default=datetime.utcnow)
    expires_at = Column(DateTime,default=lambda : datetime.utcnow() + timedelta(minutes=30))

    user = relationship("Users", back_populates="requests")
    items = relationship("RequestItem", back_populates="request",cascade="all, delete")
    responses = relationship("Response", back_populates="request",cascade="all, delete")
