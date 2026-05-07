from fastapi import APIRouter ,Depends
from sqlalchemy.orm import Session
from app.schemas.common_response import APIResponse
from app.schemas.user import  UpdateProfile
from app.models.users import Users
from app.core.deps import get_current_user, get_db

router = APIRouter()


@router.put("/update-profile")
def update_profile(
    data: UpdateProfile,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
): 
    
    current_user.name = data.name
    current_user.latitude = data.latitude
    current_user.longitude = data.longitude
    current_user.is_profile_complete = True

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated"}