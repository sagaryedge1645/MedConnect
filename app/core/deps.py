from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import HTTPAuthorizationCredentials
from app.core.database import SessionLocal
from sqlalchemy.orm import Session

from app.core.security import verify_token
from app.models.pharmacy import Pharmacy
from app.models.users import Users



security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = verify_token(token, "access")

    if payload.get("role") != "user":
        raise HTTPException(403, "Access denied")

    if not payload:
        raise HTTPException(401, "Invalid or expired token")

    user = db.query(Users).filter(Users.id == payload.get("id")).first()

    if not user:
        raise HTTPException(404, "User not found")

    return user


def get_current_pharmacy(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token,"access")

    if payload.get("role") != "pharmacy":
       raise HTTPException(403, "Access denied")

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == payload.get("id")).first()

    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")

    return pharmacy