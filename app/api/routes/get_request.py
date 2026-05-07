from datetime import datetime
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_pharmacy, get_db
from app.models.pharmacy import Pharmacy
from app.schemas.common_response import APIResponse
from app.models.request import Request
from app.services.distance import calculate_distance
from sqlalchemy.orm import joinedload


router = APIRouter()

@router.get("/pharmacy",response_model=APIResponse)
def get_request_for_pharmacy(db:Session = Depends(get_db),current_pharmacy :Pharmacy = Depends(get_current_pharmacy)):
  
    requests = db.query(Request).filter(Request.expires_at > datetime.utcnow()).options(joinedload(Request.items)).all()

    nearby_request = []

    for r in requests:
    
        distance = calculate_distance(
            current_pharmacy.latitude,
            current_pharmacy.longitude,
            r.latitude,
            r.longitude
        )

        if distance <= 2 :
            nearby_request.append(
                {
                "request_id": r.id,
               "medicines": [i.name for i in r.items],
                "prescription_image": r.prescription_image,
                "distance": round(distance, 2),
                "expires_at": r.expires_at
            }
            )
    return APIResponse(
        success=True,
        message="Nearby requests fetched",
        data=nearby_request
    )