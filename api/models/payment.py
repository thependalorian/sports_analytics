"""
Payment Model
Location: /api/models/payment.py
Purpose: Payment database model (Namibian market: MTC Mobile Money, Bank Windhoek)
"""

from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Payment(BaseModel):
    """Payment model"""
    __tablename__ = 'payments'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    payment_id = Column(String(255), unique=True, nullable=False, index=True)  # External payment ID
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default='NAD')
    payment_method = Column(String(50), nullable=False, index=True)  # 'mtc_mobile_money', 'bank_windhoek', 'card'
    phone_number = Column(String(20))  # For MTC Mobile Money
    status = Column(String(50), default='pending', index=True)  # 'pending', 'completed', 'failed', 'refunded'
    transaction_id = Column(String(255))  # External transaction ID
    description = Column(Text)
    return_url = Column(Text)
    extra_data = Column(JSONB)  # Payment metadata (renamed from 'metadata' - reserved in SQLAlchemy)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="payments")

