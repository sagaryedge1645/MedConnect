from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.models.orders import Order
from app.models.users import Users


router = APIRouter()

@router.get("/{order_id}")
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(404, "Order not found")

    if order.user_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    return {
        "order_id": order.id,
        "status": order.status,
        "total_price": order.total_price
    }