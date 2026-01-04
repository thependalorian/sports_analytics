"""
Notification Model
Location: /api/models/notification.py
Purpose: Notification database model (Namibian market: WhatsApp, SMS)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Notification(BaseModel):
    """Notification model"""
    __tablename__ = 'notifications'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # 'whatsapp', 'sms', 'email', 'push'
    phone_number = Column(String(20))  # For WhatsApp/SMS
    email = Column(String(255))  # For email
    message = Column(Text, nullable=False)
    template_id = Column(String(100))  # For WhatsApp templates
    status = Column(String(50), default='pending', index=True)  # 'pending', 'sent', 'failed', 'delivered'
    message_id = Column(String(255))  # External message ID
    error_message = Column(Text)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="notifications")

