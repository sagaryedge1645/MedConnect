from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.pharmacy import Pharmacy
from app.core.enums import PharmacyStatus

router = APIRouter()


@router.put("/verify/{pharmacy_id}")
def verify_pharmacy(
    pharmacy_id: str,
    action:PharmacyStatus,  
    db: Session = Depends(get_db)
):

    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

    if not pharmacy:
        raise HTTPException(404, "Not found")
    
    if action == PharmacyStatus.PENDING:
        pharmacy.is_verified = False
        pharmacy.verification_status = "PENDING"

    if action == PharmacyStatus.APPPROVED:
        pharmacy.is_verified = True
        pharmacy.verification_status = "APPROVED"

    elif action == PharmacyStatus.REJECTED:
        pharmacy.is_verified = False
        pharmacy.verification_status = "REJECTED"

    else:
        raise HTTPException(400, "Invalid action")

    db.commit()

    return {"message": f"Pharmacy {action}d successfully"}
