from sqlalchemy import Column, String, DateTime
from app.core.database import Base
import uuid
from datetime import datetime

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    user_id = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "user" or "pharmacy"
    
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)