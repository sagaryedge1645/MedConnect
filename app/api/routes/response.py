from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.ResponseItem import ResponseItem
from app.models.pharmacy import Pharmacy
from app.models.refresh_token import RefreshToken
from app.models.request import Request
from app.schemas.common_response import APIResponse
from app.schemas.response import CreateResponse, ResponseOut
from app.models.response import  Response 
from app.core.deps import get_current_pharmacy, get_db
from datetime import datetime


router = APIRouter()

@router.post("/response")
def create_response(
    data: CreateResponse,
    db: Session = Depends(get_db),
    current_pharmacy: Pharmacy = Depends(get_current_pharmacy)
):

    req = db.query(Request).filter(Request.id == data.request_id).first()
    if not req:
        raise HTTPException(404, "Request does not exist")


    if datetime.utcnow() > req.expires_at:
        raise HTTPException(400, "Request expired")

    if not current_pharmacy.is_active:
        raise HTTPException(400, "Pharmacy inactive")

    existing = db.query(Response).filter(
        Response.request_id == data.request_id,
        Response.pharmacy_id == current_pharmacy.id
    ).first()

    if existing:
        raise HTTPException(400, "Already responded")


    response = Response(
    request_id=data.request_id,
    pharmacy_id=current_pharmacy.id,
    )

    db.add(response)
    db.commit()
    db.refresh(response)

    for item in data.items:
      db_item = ResponseItem(
        response_id=response.id,
        name=item.name,
        price=item.price,
        available=item.available,
        brand=item.brand,
        expiry_date=item.expiry_date
    )
      db.add(db_item)

    db.commit()
    db.refresh(response)  # ✅ important for items relationship

    return APIResponse(
    success=True,
    message="Response sent successfully",
    data=ResponseOut.from_orm(response)
)
    