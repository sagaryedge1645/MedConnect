from datetime import datetime
from fastapi import Depends, HTTPException,APIRouter
from app.core.deps import get_db
from app.core.security import create_access_token, verify_token
from app.models.refresh_token import RefreshToken
from app.schemas.common_response import APIResponse
from sqlalchemy.orm import Session



router = APIRouter()

@router.post("/refresh", response_model=APIResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):

    payload = verify_token(refresh_token, "refresh")

    if not payload:
        raise HTTPException(401, "Invalid refresh token")

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not db_token:
        raise HTTPException(401, "Token not found")

    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(401, "Token expired")

    new_access_token = create_access_token({
        "id": payload["id"],
        "role": payload["role"]
    })

    return APIResponse(
        success=True,
        message="Token refreshed",
        data={
            "access_token": new_access_token
        }
    )