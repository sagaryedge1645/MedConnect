from sqlalchemy import Column, String, Float, Boolean
from app.core.database import Base
import uuid
from sqlalchemy.orm import relationship
from app.core.enums import PharmacyStatus


class Pharmacy(Base):
    __tablename__ = "pharmacies"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    name = Column(String,nullable=False)
    phone = Column(String,nullable=False,unique=True,index=True)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False,)
    is_active = Column(Boolean, default=True)
    license_number = Column(String, unique=True, nullable=False)
    license_document = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String, default=PharmacyStatus.PENDING.value)
    responses = relationship("Response", back_populates="pharmacy")
    orders = relationship("Order", back_populates="pharmacy")