"""
Notification Schemas (Namibian Market)
Location: /api/schemas/notification.py
Purpose: Pydantic models for notification endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class NotificationSend(BaseModel):
    """Send notification request"""
    phone_number: Optional[str] = Field(None, description="Required for WhatsApp/SMS")
    email: Optional[str] = Field(None, description="Required for email")
    message: str
    template_id: Optional[str] = None

class NotificationResponse(BaseModel):
    """Notification response"""
    id: UUID
    user_id: UUID
    type: str  # 'whatsapp', 'sms', 'email', 'push'
    phone_number: Optional[str]
    email: Optional[str]
    message: str
    template_id: Optional[str]
    status: str
    message_id: Optional[str]
    error_message: Optional[str]
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationListResponse(BaseModel):
    """Notification list response"""
    notifications: list[NotificationResponse]
    total: int
    page: int
    limit: int

