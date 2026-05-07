from fastapi import Depends,APIRouter, HTTPException
from app.core.deps import get_db
from app.core.security import create_access_token, create_refresh_token
from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.users import Users
from app.schemas.common_response import APIResponse

router = APIRouter()

@router.post("/login", response_model=APIResponse)
def login_user(phone: str, db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.phone == phone).first()

    if not user:
        raise HTTPException(404, "User not found")

    access_token = create_access_token({
        "id": user.id,
        "role": "user"
    })

    refresh_token = create_refresh_token({
        "id": user.id,
        "role": "user"
    })

    db_token = RefreshToken(
        user_id=user.id,
         role="user",
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