from sqlalchemy import Column, String, Float, DateTime,ForeignKey
from app.core.database import Base
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from app.core.enums import OrderStatus

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String, ForeignKey("requests.id"), index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True)
    pharmacy_id = Column(String, ForeignKey("pharmacies.id"), index=True)
    total_price = Column(Float, nullable=False)

    status = Column(String, default=OrderStatus.PLACED.value)  # PLACED, CONFIRMED, DELIVERED

    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("Users", back_populates="orders")
    pharmacy = relationship("Pharmacy", back_populates="orders")