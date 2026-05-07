from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import  get_current_pharmacy, get_db
from app.core.enums import OrderStatus
from app.models.orders import Order
from app.models.pharmacy import Pharmacy


router = APIRouter()

@router.put("/status/{order_id}")
def update_order_status(
    order_id: str,
    status: OrderStatus,
    db: Session = Depends(get_db),
    current_pharmacy: Pharmacy = Depends(get_current_pharmacy)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(404, "Order not found")

    # ✅ only pharmacy who owns order
    if order.pharmacy_id != current_pharmacy.id:
        raise HTTPException(403, "Not allowed")

    # ✅ validate status
    allowed_status = ["ACCEPTED", "DISPATCHED", "DELIVERED", "CANCELLED"]

    if status not in allowed_status:
        raise HTTPException(400, "Invalid status")

    order.status = status.value
    db.commit()

    return {"message": f"Order {status}"}