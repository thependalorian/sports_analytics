"""
Payments Router (Namibian Market)
Location: /api/routers/payments.py
Purpose: Payment endpoints (MTC Mobile Money, Bank Windhoek)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.payment_service import PaymentService
from api.schemas.payment import PaymentInitiate, PaymentResponse, PaymentListResponse

router = APIRouter()

@router.post("/initiate", response_model=dict)
async def initiate_payment(
    payment_data: PaymentInitiate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate payment (MTC Mobile Money, Bank Windhoek, etc.)"""
    service = PaymentService(db)
    result = service.initiate_payment(payment_data, current_user.id)
    return result

@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payment by payment_id"""
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/{payment_id}/status", response_model=dict)
async def check_payment_status(
    payment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check payment status"""
    service = PaymentService(db)
    status_data = service.check_payment_status(payment_id)
    if not status_data:
        raise HTTPException(status_code=404, detail="Payment not found")
    return status_data

@router.get("", response_model=PaymentListResponse)
async def list_payments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List payments for user"""
    service = PaymentService(db)
    result = service.list_payments(
        user_id=current_user.id,
        page=page,
        limit=limit,
        status=status,
        date_from=date_from,
        date_to=date_to
    )
    return PaymentListResponse(**result)

