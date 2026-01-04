"""
Password Reset Model
Location: /api/models/password_reset.py
Purpose: Password reset token model
Date: 2026-01-04
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.base import BaseModel
from datetime import datetime, timedelta

class PasswordResetToken(BaseModel):
    """Password reset token model"""
    __tablename__ = 'password_reset_tokens'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    used = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    def is_valid(self) -> bool:
        """Check if token is valid and not expired"""
        return (
            self.expires_at > datetime.utcnow() and
            not self.used
        )

