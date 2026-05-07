from sqlalchemy import Column ,String, DateTime,Boolean,Integer
from app.core.database import Base
from datetime import datetime , timedelta
import uuid

class OTP(Base):
    __tablename__ = "otps"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    phone = Column(String, nullable= False,index= True)
    otp = Column(String,nullable=False)
    expires_at = Column(DateTime)
    is_used = Column(Boolean,default= False)
    attempts = Column(Integer,default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

