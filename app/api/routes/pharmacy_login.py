from fastapi import Depends,APIRouter, HTTPException
from app.core.deps import get_db
from app.core.security import create_access_token, create_refresh_token
from app.models.pharmacy import Pharmacy
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas.common_response import APIResponse


router = APIRouter()

@router.post("/login", response_model=APIResponse)
def login_pharmacy(phone: str, db: Session = Depends(get_db)):

    pharmacy = db.query(Pharmacy).filter(Pharmacy.phone == phone).first()

    if not pharmacy:
        raise HTTPException(404, "Pharmacy not found")

    access_token = create_access_token({
        "id": pharmacy.id,
        "role": "pharmacy"
    })

    refresh_token = create_refresh_token({
        "id": pharmacy.id,
        "role": "pharmacy"
    })

    db_token = RefreshToken(
        user_id=pharmacy.id,
        role="pharmacy",
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(db_token)
    db.commit()

    return APIResponse(
        success=True,
        message="Login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )