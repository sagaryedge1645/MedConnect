from pydantic import BaseModel

class CreatePharmacy(BaseModel):
    name:str
    phone:str
    latitude:float
    longitude:float
    license_number: str 

class PharmacyResponse(BaseModel):
    id:str
    name:str
    phone:str
    latitude:float
    longitude:float
    license_number: str 
    class Config:
        from_attributes = True
