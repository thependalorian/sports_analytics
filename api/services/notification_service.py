"""
Notification Service (Namibian Market)
Location: /api/services/notification_service.py
Purpose: Business logic for notification operations (WhatsApp, SMS, Email)
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime
import httpx

from api.models.notification import Notification
from api.schemas.notification import NotificationSend
import os
# Avoid circular import - get settings directly
from utils.logger import get_logger
import os

logger = get_logger(__name__)

class NotificationService:
    """Notification service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def send_whatsapp(self, notification_data: NotificationSend, user_id: UUID) -> Notification:
        """Send WhatsApp notification"""
        notification = Notification(
            user_id=user_id,
            type='whatsapp',
            phone_number=notification_data.phone_number,
            message=notification_data.message,
            template_id=notification_data.template_id,
            status='pending'
        )
        
        self.db.add(notification)
        self.db.commit()
        
        # Send via WhatsApp Business API
        try:
            message_id = self._send_whatsapp_message(notification)
            notification.message_id = message_id
            notification.status = 'sent'
            notification.sent_at = datetime.utcnow()
        except Exception as e:
            logger.error(f"WhatsApp send failed: {e}")
            notification.status = 'failed'
            notification.error_message = str(e)
        
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def send_sms(self, notification_data: NotificationSend, user_id: UUID) -> Notification:
        """Send SMS notification"""
        notification = Notification(
            user_id=user_id,
            type='sms',
            phone_number=notification_data.phone_number,
            message=notification_data.message,
            status='pending'
        )
        
        self.db.add(notification)
        self.db.commit()
        
        # Send via Africa's Talking SMS API
        try:
            message_id = self._send_sms_message(notification)
            notification.message_id = message_id
            notification.status = 'sent'
            notification.sent_at = datetime.utcnow()
        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            notification.status = 'failed'
            notification.error_message = str(e)
        
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def _send_whatsapp_message(self, notification: Notification) -> str:
        """Send WhatsApp message via WhatsApp Business API (Twilio)"""
        import httpx
        from twilio.rest import Client as TwilioClient
        
        logger.info(f"Sending WhatsApp to {notification.phone_number}")
        
        # Use Twilio WhatsApp Business API
        twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        twilio_whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")
        
        if not twilio_account_sid or not twilio_auth_token:
            logger.warning("Twilio credentials not configured, using test mode")
            return f"WA_MSG_TEST_{uuid4().hex[:12]}"
        
        try:
            client = TwilioClient(twilio_account_sid, twilio_auth_token)
            
            message = client.messages.create(
                body=notification.message,
                from_=twilio_whatsapp_from,
                to=f"whatsapp:{notification.phone_number}"
            )
            
            logger.info(f"WhatsApp message sent: {message.sid}")
            return message.sid
        except Exception as e:
            logger.error(f"Twilio WhatsApp send failed: {e}")
            # Fallback to HTTP API if Twilio SDK fails
            try:
                api_url = os.getenv('WHATSAPP_API_URL', 'https://api.whatsapp.com')
                api_key = os.getenv('WHATSAPP_API_KEY', '')
                
                if api_url and api_key:
                    with httpx.Client(timeout=30.0) as client:
                        response = client.post(
                            f"{api_url}/messages",
                            headers={"Authorization": f"Bearer {api_key}"},
                            json={
                                "to": notification.phone_number,
                                "message": notification.message,
                                "template_id": notification.template_id
                            }
                        )
                        response.raise_for_status()
                        result = response.json()
                        return result.get("message_id", f"WA_MSG_{uuid4().hex[:12]}")
            except Exception as e2:
                logger.error(f"WhatsApp HTTP API also failed: {e2}")
                raise e
    
    def _send_sms_message(self, notification: Notification) -> str:
        """Send SMS message via Africa's Talking API"""
        import httpx
        
        logger.info(f"Sending SMS to {notification.phone_number}")
        
        # Africa's Talking SMS API
        api_key = os.getenv('AFRICAS_TALKING_API_KEY', '')
        api_username = os.getenv("AFRICAS_TALKING_USERNAME", "")
        api_url = os.getenv('AFRICAS_TALKING_API_URL', 'https://api.africastalking.com/version1/messaging')
        
        if not api_key or not api_username:
            logger.warning("Africa's Talking credentials not configured, using test mode")
            return f"SMS_TEST_{uuid4().hex[:12]}"
        
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    api_url,
                    headers={
                        "apiKey": api_key,
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json"
                    },
                    data={
                        "username": api_username,
                        "to": notification.phone_number,
                        "message": notification.message,
                        "from": os.getenv("SMS_SENDER_ID", "SportsVision")
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                # Africa's Talking returns SMSMessageData with Recipients
                sms_message_data = result.get("SMSMessageData", {})
                recipients = sms_message_data.get("Recipients", [])
                if recipients:
                    message_id = recipients[0].get("messageId")
                    return message_id or f"SMS_{uuid4().hex[:12]}"
                return f"SMS_{uuid4().hex[:12]}"
        except httpx.HTTPError as e:
            logger.error(f"Africa's Talking SMS API error: {e}")
            raise
        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            raise
    
    def list_notifications(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
        type: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List notifications for user"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        # Apply filters
        if type:
            query = query.filter(Notification.type == type)
        if status:
            query = query.filter(Notification.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        notifications = query.order_by(desc(Notification.created_at)).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "notifications": notifications,
            "total": total,
            "page": page,
            "limit": limit
        }

