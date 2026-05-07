from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.schemas.common_response import APIResponse
from app.schemas.pharmacy import CreatePharmacy, PharmacyResponse
from app.models.pharmacy import Pharmacy
from app.core.deps import get_db

router = APIRouter()

@router.post("/register")
def register(data:CreatePharmacy,db:Session = Depends(get_db)):
    pharmacy = Pharmacy(**data.dict(),is_active=True,
        is_verified=False,verification_status="PENDING")
    db.add(pharmacy)
    db.commit()
    db.refresh(pharmacy)
    
    return APIResponse(
        success=True,
        message="Registration successful",
        data=PharmacyResponse.from_orm(pharmacy)
    )
