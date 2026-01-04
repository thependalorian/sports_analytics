"""
User Models
Location: /api/models/user.py
Purpose: User, UserSession, and UserSettings database models
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class User(BaseModel):
    """User model"""
    __tablename__ = 'users'
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone_number = Column(String(20))
    organization = Column(String(255), index=True)  # 'UNAM', 'MTC', 'NFA', etc.
    campus = Column(String(100), index=True)  # For UNAM: 'Windhoek Main', 'Oshakati', etc.
    avatar_url = Column(Text)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255))
    language = Column(String(10), default='en')  # 'en', 'af', 'osh'
    timezone = Column(String(50), default='Africa/Windhoek')
    subscription_plan = Column(String(50), default='free')  # 'free', 'university', 'pro', 'enterprise'
    subscription_expires_at = Column(DateTime)
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    matches = relationship("Match", back_populates="creator", foreign_keys="Match.created_by")
    scouting_reports = relationship("ScoutingReport", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class UserSession(BaseModel):
    """User session model (for JWT refresh tokens)"""
    __tablename__ = 'user_sessions'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    refresh_token = Column(String(500), unique=True, nullable=False, index=True)
    device_info = Column(JSONB)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    expires_at = Column(DateTime, nullable=False, index=True)
    revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="sessions")

class UserSettings(BaseModel):
    """User settings model"""
    __tablename__ = 'user_settings'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    notifications = Column(JSONB, default={})  # Notification preferences
    data_quality = Column(JSONB, default={})  # Image/video quality settings
    language = Column(String(10), default='en')
    timezone = Column(String(50), default='Africa/Windhoek')
    preferences = Column(JSONB, default={})  # Other user preferences
    
    # Relationships
    user = relationship("User", back_populates="settings")

