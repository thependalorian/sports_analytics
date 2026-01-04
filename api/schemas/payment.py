"""
Payment Schemas (Namibian Market)
Location: /api/schemas/payment.py
Purpose: Pydantic models for payment endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class PaymentInitiate(BaseModel):
    """Initiate payment request"""
    amount: Decimal = Field(..., gt=0, description="Payment amount")
    currency: str = "NAD"
    payment_method: str = Field(..., description="mtc_mobile_money, bank_windhoek, or card")
    phone_number: Optional[str] = Field(None, description="Required for MTC Mobile Money")
    description: Optional[str] = None
    return_url: Optional[str] = None

class PaymentResponse(BaseModel):
    """Payment response"""
    id: UUID
    payment_id: str
    amount: Decimal
    currency: str
    payment_method: str
    phone_number: Optional[str]
    status: str
    transaction_id: Optional[str]
    description: Optional[str]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PaymentListResponse(BaseModel):
    """Payment list response"""
    payments: list[PaymentResponse]
    total: int
    page: int
    limit: int

