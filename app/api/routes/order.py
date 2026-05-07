from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.enums import OrderStatus
from app.models.orders import Order
from app.models.request import Request
from app.models.response import Response
from app.models.users import Users
from app.schemas.order import CreateOrder, OrderOut
from app.schemas.common_response import APIResponse
from app.core.deps import get_current_user, get_db
from app.models.ResponseItem import ResponseItem
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.post("/", response_model=APIResponse)
def create_order(data: CreateOrder, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):

    request = db.query(Request).filter(Request.id == data.request_id).first()
    if not request:
        raise HTTPException(404, "Request not found")
    
    if request.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")


    response = db.query(Response).filter(
        Response.request_id == data.request_id,
        Response.pharmacy_id == data.pharmacy_id
    ).options(
        joinedload(Response.items)
    ).first()
    if not response:
        raise HTTPException(404, "Pharmacy response not found")


    # calculate total price
    total_price = sum(item.price for item in response.items if item.available)

    if total_price == 0:
        raise HTTPException(status_code=400, detail="No available items")
    
    existing_order = db.query(Order).filter(
        Order.request_id == data.request_id,
        Order.user_id == current_user.id
    ).first()

    if existing_order:
        raise HTTPException(status_code=400, detail="Order already placed")


    order = Order(
        request_id=data.request_id,
        user_id=current_user.id,
        pharmacy_id=data.pharmacy_id,
        total_price=total_price,
        status=OrderStatus.PLACED.value 
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return APIResponse(
        success=True,
        message="Order placed successfully",
        data=OrderOut.from_orm(order)
    )