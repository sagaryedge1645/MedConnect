from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.models.ResponseItem import ResponseItem
from app.models.users import Users
from app.services.distance import calculate_distance
from app.schemas.common_response import APIResponse
from app.models.request import Request
from app.models.pharmacy import Pharmacy
from  app.models.response import Response
from sqlalchemy.orm import joinedload


router = APIRouter()

@router.get("/{request_id}", response_model=APIResponse)
def get_responses(
    request_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):

    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    responses = db.query(Response).filter(
    Response.request_id == request_id).options(joinedload(Response.pharmacy),joinedload(Response.items)).all()

    result = []

    for res in responses:
        pharmacy = res.pharmacy
        items = res.items
        total_price = sum(item.price for item in items if item.available)

        distance = calculate_distance(
            request.latitude,
            request.longitude,
            pharmacy.latitude,
            pharmacy.longitude
        )

        result.append({
            "pharmacy_id": pharmacy.id,
            "pharmacy_name": pharmacy.name,
            "distance": round(distance, 2),
            "total_price": total_price,
            "items": [
                {
                    "name": item.name,
                    "price": item.price,
                    "available": item.available,
                    "image_url": item.image_url,
                    "brand": item.brand,
                    "expiry_date": item.expiry_date
                }
                for item in items
            ]
        })

    result = sorted(result, key=lambda x: x["total_price"])

    return APIResponse(
        success=True,
        message="Responses fetched successfully",
        data=result
    )
