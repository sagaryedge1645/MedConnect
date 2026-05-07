from pydantic import BaseModel


class UpdateProfile(BaseModel):
    name:str
    phone:str
    latitude:float
    longitude:float

class ProfileResponse(BaseModel):
    id:str
    name:str
    phone:str
    latitude:float
    longitude:float
    
    class Config:
        from_attributes = True