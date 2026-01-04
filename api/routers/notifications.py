"""
Notifications Router (Namibian Market)
Location: /api/routers/notifications.py
Purpose: Notification endpoints (WhatsApp, SMS, Email)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.notification_service import NotificationService
from api.schemas.notification import NotificationSend, NotificationResponse, NotificationListResponse

router = APIRouter()

@router.post("/whatsapp/send", response_model=NotificationResponse)
async def send_whatsapp(
    notification_data: NotificationSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send WhatsApp notification"""
    service = NotificationService(db)
    notification = service.send_whatsapp(notification_data, current_user.id)
    return notification

@router.post("/sms/send", response_model=NotificationResponse)
async def send_sms(
    notification_data: NotificationSend,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send SMS notification"""
    service = NotificationService(db)
    notification = service.send_sms(notification_data, current_user.id)
    return notification

@router.get("", response_model=NotificationListResponse)
async def list_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    type: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List notifications for user"""
    service = NotificationService(db)
    result = service.list_notifications(
        user_id=current_user.id,
        page=page,
        limit=limit,
        type=type,
        status=status
    )
    return NotificationListResponse(**result)

