"""
Settings Schemas
Location: /api/schemas/settings.py
Purpose: Pydantic models for settings endpoints
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class UserSettingsResponse(BaseModel):
    """User settings response"""
    notifications: Dict[str, Any]
    data_quality: Dict[str, Any]
    language: str
    timezone: str
    
    class Config:
        from_attributes = True

class UserSettingsUpdate(BaseModel):
    """Update user settings request"""
    notifications: Optional[Dict[str, Any]] = None
    data_quality: Optional[Dict[str, Any]] = None
    language: Optional[str] = None
    timezone: Optional[str] = None

