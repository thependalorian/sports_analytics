"""
Settings Router
Location: /api/routers/settings.py
Purpose: User settings endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User, UserSettings
from api.schemas.settings import UserSettingsResponse, UserSettingsUpdate

router = APIRouter()

@router.get("/user", response_model=UserSettingsResponse)
async def get_user_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user settings"""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        # Create default settings
        settings = UserSettings(
            user_id=current_user.id,
            notifications={},
            data_quality={},
            language=current_user.language,
            timezone=current_user.timezone
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/user", response_model=UserSettingsResponse)
async def update_user_settings(
    settings_data: UserSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user settings"""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    
    if settings_data.notifications is not None:
        settings.notifications = settings_data.notifications
    if settings_data.data_quality is not None:
        settings.data_quality = settings_data.data_quality
    if settings_data.language is not None:
        settings.language = settings_data.language
        current_user.language = settings_data.language
    if settings_data.timezone is not None:
        settings.timezone = settings_data.timezone
        current_user.timezone = settings_data.timezone
    
    db.commit()
    db.refresh(settings)
    return settings

@router.get("/user/preferences")
async def get_user_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        return {"preferences": {}}
    return {"preferences": settings.preferences or {}}

@router.get("/user/notifications")
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification preferences"""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        return {"notifications": {}}
    return {"notifications": settings.notifications or {}}

@router.get("/user/data-quality")
async def get_data_quality_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get data quality settings"""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        return {"data_quality": {}}
    return {"data_quality": settings.data_quality or {}}

