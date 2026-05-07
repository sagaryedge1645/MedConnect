from sqlalchemy import Boolean, Column ,String, Float
from app.core.database import Base
import uuid
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    phone = Column(String,nullable=False,unique=True, index= True)
    name = Column(String, nullable=True)       
    latitude = Column(Float, nullable=True)     
    longitude = Column(Float, nullable=True) 
    is_profile_complete = Column(Boolean, default=False)
    requests = relationship("Request", back_populates="user")
    orders = relationship("Order", back_populates="user")
