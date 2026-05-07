from datetime import datetime
from typing import List,Optional
from pydantic import BaseModel

class CreateRequest(BaseModel):
    medicines: Optional[List[str]] = None
    latitude: float
    longitude: float
    prescription_image: Optional[str] = None

    
class NearByPharmacy(BaseModel):
    id:str
    name:str
    distance:float

class RequestResponse(BaseModel):
    request_id: str
    nearby_pharmacies: List[NearByPharmacy]
    medicines: Optional[List[str]] = None
    prescription_image: Optional[str] = None
    expires_at: datetime