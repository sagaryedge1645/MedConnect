from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import create_access_token, create_refresh_token
from app.models.otp import OTP
from datetime import datetime, timedelta

from app.models.pharmacy import Pharmacy
from app.models.refresh_token import RefreshToken
from app.models.users import Users

router = APIRouter()


@router.post("/verify-otp")
def verify_otp(phone: str, otp: str, role: str, db: Session = Depends(get_db)):

    record = db.query(OTP).filter(
        OTP.phone == phone
    ).order_by(OTP.created_at.desc()).first()

    if not record:
        raise HTTPException(400, "OTP not found")

    if record.expires_at < datetime.utcnow():
        raise HTTPException(400, "OTP expired")

    if record.is_used:
        raise HTTPException(400, "OTP already used")

    if record.otp != otp:
        record.attempts += 1
        db.commit()

        if record.attempts >= 3:
            raise HTTPException(403, "Too many attempts")

        raise HTTPException(400, "Invalid OTP")

    record.is_used = True
    db.commit()


    if role == "user":
        entity = db.query(Users).filter(Users.phone == phone).first()

        if not entity:
            entity = Users(
              phone=phone, 
             is_profile_complete=False
            )
            db.add(entity)
            db.commit()
            db.refresh(entity)

    elif role == "pharmacy":
        entity = db.query(Pharmacy).filter(Pharmacy.phone == phone).first()

        if not entity:
            raise HTTPException(404, "Pharmacy not registered")

        if not entity.is_verified:
            raise HTTPException(403, "Pharmacy not verified")
        

    else:
        raise HTTPException(400, "Invalid role")

    access_token = create_access_token({
        "id": entity.id,
        "role": role
    })

    refresh_token = create_refresh_token({
        "id": entity.id,
        "role": role
    })

    db_token = RefreshToken(
        user_id=entity.id,
        role=role,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }