from fastapi import Depends,APIRouter
from app.core.deps import get_db
from app.models.refresh_token import RefreshToken
from app.schemas.common_response import APIResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/logout", response_model=APIResponse)
def logout(refresh_token: str, db: Session = Depends(get_db)):

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if db_token:
        db.delete(db_token)
        db.commit()

    return APIResponse(
        success=True,
        message="Logged out successfully",
        data=None
    )