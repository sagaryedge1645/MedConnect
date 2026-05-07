from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class RequestItem(Base):
    __tablename__ = "request_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String,ForeignKey("requests.id"))
    name = Column(String, nullable=False)
    request = relationship("Request", back_populates="items")