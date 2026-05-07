from pydantic import BaseModel

class CreateOrder(BaseModel):
    request_id: str
    pharmacy_id: str


class OrderOut(BaseModel):
    id: str
    request_id: str
    user_id: str
    pharmacy_id: str
    total_price: float
    status: str

    class Config:
        from_attributes = True