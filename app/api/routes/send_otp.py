from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.otp import OTP
from app.models.users import Users
from app.models.pharmacy import Pharmacy

router = APIRouter()

@router.post("/send-otp")
def send_otp(phone: str, role: str, db: Session = Depends(get_db)):

    if role == "user":
        pass  

    elif role == "pharmacy":
        pharmacy = db.query(Pharmacy).filter(Pharmacy.phone == phone).first()

        if not pharmacy:
            raise HTTPException(404, "Pharmacy not registered")

    else:
        raise HTTPException(400, "Invalid role")
    

    existing = db.query(OTP).filter(
        OTP.phone == phone,
        OTP.expires_at > datetime.utcnow()
    ).first()

    if existing:
        raise HTTPException(429, "OTP already sent. Try after 5 minutes")

 
    otp = str(random.randint(1000, 9999))

    db_otp = OTP(
        phone=phone,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(db_otp)
    db.commit()

    print("OTP:", otp) 

    return {
        "message": "OTP sent successfully"
    }