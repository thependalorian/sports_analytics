"""
User Router
Location: /api/routers/user.py
Purpose: User profile endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.schemas.user import UserProfileResponse, UserProfileUpdate, PasswordChange
from api.services.auth_service import AuthService

router = APIRouter()

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return current_user

@router.get("/me/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get user profile (alias for /me)"""
    return current_user

@router.put("/me/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.phone_number is not None:
        current_user.phone_number = profile_data.phone_number
    if profile_data.organization is not None:
        current_user.organization = profile_data.organization
    if profile_data.campus is not None:
        current_user.campus = profile_data.campus
    if profile_data.language is not None:
        current_user.language = profile_data.language
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password"""
    auth_service = AuthService(db)
    
    if not auth_service.verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    current_user.password_hash = auth_service.hash_password(password_data.new_password)
    db.commit()

@router.get("/me/unam-campus")
async def get_unam_campus(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get UNAM campus information for user"""
    from api.models.unam import UNAMCampus, CampusTeam
    from sqlalchemy import func
    
    if not current_user.campus:
        raise HTTPException(status_code=404, detail="User not associated with UNAM campus")
    
    # Get campus details
    campus = db.query(UNAMCampus).filter(
        UNAMCampus.id == current_user.campus.lower().replace(" ", "_")
    ).first()
    
    if not campus:
        # Try to find by name
        campus = db.query(UNAMCampus).filter(
            UNAMCampus.name.ilike(f"%{current_user.campus}%")
        ).first()
    
    if not campus:
        return {
            "campus_name": current_user.campus,
            "message": "Campus details not found in database"
        }
    
    # Get campus teams count
    teams_count = db.query(func.count(CampusTeam.id)).filter(
        CampusTeam.campus_id == campus.id,
        CampusTeam.is_active == True
    ).scalar() or 0
    
    return {
        "campus_id": campus.id,
        "campus_name": campus.name,
        "location": campus.location,
        "region": campus.region,
        "is_active": campus.is_active,
        "teams_count": teams_count
    }

