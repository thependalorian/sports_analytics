"""
User Schemas
Location: /api/schemas/user.py
Purpose: Pydantic models for user endpoints
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class UserProfileResponse(BaseModel):
    """User profile response"""
    id: UUID
    email: str
    full_name: Optional[str]
    organization: Optional[str]
    campus: Optional[str]
    phone_number: Optional[str]
    avatar_url: Optional[str]
    language: str
    timezone: str
    subscription_plan: str
    subscription_expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    """Update user profile request"""
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    organization: Optional[str] = None
    campus: Optional[str] = None
    language: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None

class PasswordChange(BaseModel):
    """Change password request"""
    current_password: str
    new_password: str

