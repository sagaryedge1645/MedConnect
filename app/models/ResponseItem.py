from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class ResponseItem(Base):
    __tablename__ = "response_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    response_id = Column(String, ForeignKey("responses.id"), index=True)
    name = Column(String)
    price = Column(Float)
    available = Column(Boolean)
    brand = Column(String)
    image_url = Column(String)
    expiry_date = Column(Date)
    class Config:
        from_attributes = True
    response = relationship("Response", back_populates="items")