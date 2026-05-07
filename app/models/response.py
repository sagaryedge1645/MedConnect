from sqlalchemy import JSON, Column,String,DateTime,ForeignKey
from app.core.database import Base
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship

class Response(Base):
    __tablename__ = "responses"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    request_id = Column(String, ForeignKey("requests.id"), nullable=False, index=True)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    request = relationship("Request", back_populates="responses")
    pharmacy = relationship("Pharmacy", back_populates="responses")
    items = relationship("ResponseItem", back_populates="response")
