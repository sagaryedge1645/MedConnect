from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.pharmacy import Pharmacy
from app.models.request_item import RequestItem
from app.models.users import Users
from app.models.request import Request

from app.schemas.common_response import APIResponse
from app.schemas.request import CreateRequest, NearByPharmacy, RequestResponse

from app.core.deps import get_current_user, get_db
from app.services.distance import calculate_distance

router = APIRouter()


@router.post("/request")
def create_request(
    data: CreateRequest,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    if not data.medicines and not data.prescription_image:
        raise HTTPException(
            status_code=400,
            detail="Provide medicines or prescription image"
        )

    pharmacies = db.query(Pharmacy).filter(Pharmacy.is_active == True , Pharmacy.is_verified == True).all()

    nearByPharmacies = []
    nearby_ids = []

    for p in pharmacies:
        print("Pharmacies",p.name)
        distance = calculate_distance(
            data.latitude,
            data.longitude,
            p.latitude,
            p.longitude
        )

        if distance <= 2:
            nearByPharmacies.append(
                NearByPharmacy(
                    id=p.id,
                    name=p.name,
                    distance=round(distance, 2)
                )
            )
            nearby_ids.append(p.id)

    try:
        
        new_request = Request(
            user_id=current_user.id,
            prescription_image=data.prescription_image,
            latitude=data.latitude,
            longitude=data.longitude,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )

        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        if data.medicines:
            for med in data.medicines:
                item = RequestItem(
                    request_id=new_request.id,
                    name=med
                )
                db.add(item)   

        db.commit()

        
        medicines = [item.name for item in new_request.items]

        response_data = RequestResponse(
            request_id=new_request.id,
            nearby_pharmacies=nearByPharmacies,
            medicines=medicines,  
            prescription_image=new_request.prescription_image,
            expires_at=new_request.expires_at
        )

        return APIResponse(
            success=True,
            message="Request created successfully",
            data=response_data
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
 
    