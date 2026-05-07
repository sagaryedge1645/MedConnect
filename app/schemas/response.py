from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class MedicineItem(BaseModel):
    name: str
    price: float
    available: bool
    image_url : Optional[str]= None  
    brand : Optional[str] = None
    expiry_date : Optional[date] = None
    model_config = ConfigDict(from_attributes=True)

class CreateResponse(BaseModel):
    request_id : str
    items:List[MedicineItem]


class ResponseOut(BaseModel):
    id: str
    request_id: str
    pharmacy_id: str
    items: List[MedicineItem]
    model_config = ConfigDict(from_attributes=True)