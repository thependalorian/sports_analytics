"""
Authentication Schemas
Location: /api/schemas/auth.py
Purpose: Pydantic models for authentication endpoints
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: Optional[str] = None
    organization: Optional[str] = None
    campus: Optional[str] = None

class UserLogin(BaseModel):
    """User login request"""
    username: EmailStr  # Email used as username
    password: str

class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str

class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)

class PasswordChange(BaseModel):
    """Change password request"""
    current_password: str
    new_password: str = Field(..., min_length=8)

