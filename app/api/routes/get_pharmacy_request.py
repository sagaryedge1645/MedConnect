from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.pharmacy import Pharmacy


router = APIRouter()

@router.get("/pending")
def get_pending_pharmacies(db: Session = Depends(get_db)):

    pharmacies = db.query(Pharmacy).filter(
        Pharmacy.verification_status == "PENDING"
    ).all()

    return {
        "pending_pharmacies": pharmacies
    }