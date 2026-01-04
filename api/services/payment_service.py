"""
Payment Service (Namibian Market)
Location: /api/services/payment_service.py
Purpose: Business logic for payment operations (MTC Mobile Money, Bank Windhoek, etc.)
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from decimal import Decimal
import httpx
import os

from api.models.payment import Payment
from api.schemas.payment import PaymentInitiate
import os
# Avoid circular import - get settings directly
from utils.logger import get_logger

logger = get_logger(__name__)

class PaymentService:
    """Payment service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def initiate_payment(self, payment_data: PaymentInitiate, user_id: UUID) -> Dict[str, Any]:
        """Initiate payment (MTC Mobile Money, Bank Windhoek, etc.)"""
        payment_id = f"payment_{uuid4().hex[:12]}"
        
        # Create payment record
        payment = Payment(
            user_id=user_id,
            payment_id=payment_id,
            amount=payment_data.amount,
            currency=payment_data.currency,
            payment_method=payment_data.payment_method,
            phone_number=payment_data.phone_number,
            description=payment_data.description,
            return_url=payment_data.return_url,
            status='pending'
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        # Initiate payment with provider
        if payment_data.payment_method == "mtc_mobile_money":
            payment_url = self._initiate_mtc_payment(payment)
        elif payment_data.payment_method == "bank_windhoek":
            payment_url = self._initiate_bank_windhoek_payment(payment)
        else:
            payment_url = None
        
        return {
            "payment_id": payment_id,
            "status": payment.status,
            "payment_url": payment_url,
            "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
    
    def _initiate_mtc_payment(self, payment: Payment) -> Optional[str]:
        """Initiate MTC Mobile Money payment"""
        try:
            import httpx
            
            logger.info(f"Initiating MTC Mobile Money payment: {payment.payment_id}")
            
            # MTC Mobile Money API integration
            api_url = os.getenv('MTC_MOBILE_MONEY_API_URL', 'https://api.mtc.na/mobile-money')
            api_key = os.getenv('MTC_MOBILE_MONEY_API_KEY', '')
            
            if not api_key:
                logger.warning("MTC Mobile Money API key not configured, using test mode")
                # Store payment in database for manual processing
                payment.metadata = {
                    "mode": "test",
                    "amount": float(payment.amount),
                    "phone": payment.phone_number
                }
                self.db.commit()
                return f"https://app.sportsvision.na/payment/{payment.payment_id}"
            
            # Real API call to MTC Mobile Money
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{api_url}/payments/initiate",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "amount": float(payment.amount),
                        "currency": payment.currency,
                        "phone_number": payment.phone_number,
                        "reference": payment.payment_id,
                        "description": payment.description or "Sports Vision Payment",
                        "callback_url": f"{os.getenv('API_URL', 'https://api.sportsvision.na')}/api/v1/webhooks/payments/mtc"
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                payment_url = result.get("payment_url")
                transaction_id = result.get("transaction_id")
                
                if transaction_id:
                    payment.transaction_id = transaction_id
                    payment.metadata = result.get("metadata", {})
                    self.db.commit()
                
                return payment_url
        except httpx.HTTPError as e:
            logger.error(f"MTC payment API error: {e}")
            payment.status = 'failed'
            payment.metadata = {"error": str(e), "error_type": "http_error"}
            self.db.commit()
            return None
        except Exception as e:
            logger.error(f"MTC payment initiation failed: {e}")
            payment.status = 'failed'
            payment.metadata = {"error": str(e)}
            self.db.commit()
            return None
    
    def _initiate_bank_windhoek_payment(self, payment: Payment) -> Optional[str]:
        """Initiate Bank Windhoek payment"""
        try:
            import httpx
            
            logger.info(f"Initiating Bank Windhoek payment: {payment.payment_id}")
            
            # Bank Windhoek API integration
            api_url = os.getenv("BANK_WINDHOEK_API_URL", "https://api.bankwindhoek.na")
            api_key = os.getenv("BANK_WINDHOEK_API_KEY", "")
            
            if not api_key:
                logger.warning("Bank Windhoek API key not configured, using test mode")
                payment.metadata = {"mode": "test", "amount": float(payment.amount)}
                self.db.commit()
                return f"https://app.sportsvision.na/payment/{payment.payment_id}"
            
            # Real API call to Bank Windhoek
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{api_url}/payments/initiate",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "amount": float(payment.amount),
                        "currency": payment.currency,
                        "reference": payment.payment_id,
                        "description": payment.description or "Sports Vision Payment",
                        "return_url": payment.return_url or f"{os.getenv('FRONTEND_URL', 'https://app.sportsvision.na')}/payment/success"
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                payment_url = result.get("payment_url")
                transaction_id = result.get("transaction_id")
                
                if transaction_id:
                    payment.transaction_id = transaction_id
                    payment.metadata = result.get("metadata", {})
                    self.db.commit()
                
                return payment_url
        except httpx.HTTPError as e:
            logger.error(f"Bank Windhoek payment API error: {e}")
            payment.status = 'failed'
            payment.metadata = {"error": str(e), "error_type": "http_error"}
            self.db.commit()
            return None
        except Exception as e:
            logger.error(f"Bank Windhoek payment initiation failed: {e}")
            payment.status = 'failed'
            payment.metadata = {"error": str(e)}
            self.db.commit()
            return None
    
    def get_payment(self, payment_id: str) -> Optional[Payment]:
        """Get payment by payment_id"""
        return self.db.query(Payment).filter(Payment.payment_id == payment_id).first()
    
    def check_payment_status(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Check payment status with provider"""
        import httpx
        
        payment = self.get_payment(payment_id)
        if not payment:
            return None
        
        # Poll payment provider for status
        try:
            if payment.payment_method == "mtc_mobile_money" and payment.transaction_id:
                api_url = os.getenv('MTC_MOBILE_MONEY_API_URL', 'https://api.mtc.na/mobile-money')
                api_key = os.getenv('MTC_MOBILE_MONEY_API_KEY', '')
                
                if api_key:
                    with httpx.Client(timeout=10.0) as client:
                        response = client.get(
                            f"{api_url}/payments/{payment.transaction_id}/status",
                            headers={"Authorization": f"Bearer {api_key}"}
                        )
                        if response.status_code == 200:
                            result = response.json()
                            new_status = result.get("status")
                            
                            # Update payment status if changed
                            if new_status and new_status != payment.status:
                                payment.status = new_status
                                if new_status == "completed":
                                    payment.completed_at = datetime.utcnow()
                                self.db.commit()
            
            elif payment.payment_method == "bank_windhoek" and payment.transaction_id:
                api_url = os.getenv("BANK_WINDHOEK_API_URL", "https://api.bankwindhoek.na")
                api_key = os.getenv("BANK_WINDHOEK_API_KEY", "")
                
                if api_key:
                    with httpx.Client(timeout=10.0) as client:
                        response = client.get(
                            f"{api_url}/payments/{payment.transaction_id}/status",
                            headers={"Authorization": f"Bearer {api_key}"}
                        )
                        if response.status_code == 200:
                            result = response.json()
                            new_status = result.get("status")
                            
                            if new_status and new_status != payment.status:
                                payment.status = new_status
                                if new_status == "completed":
                                    payment.completed_at = datetime.utcnow()
                                self.db.commit()
        except Exception as e:
            logger.error(f"Error checking payment status: {e}")
            # Continue with current status
        
        return {
            "payment_id": payment.payment_id,
            "status": payment.status,
            "amount": float(payment.amount),
            "currency": payment.currency,
            "payment_method": payment.payment_method,
            "transaction_id": payment.transaction_id,
            "completed_at": payment.completed_at.isoformat() if payment.completed_at else None
        }
    
    def list_payments(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """List payments for user"""
        query = self.db.query(Payment).filter(Payment.user_id == user_id)
        
        # Apply filters
        if status:
            query = query.filter(Payment.status == status)
        if date_from:
            query = query.filter(Payment.created_at >= date_from)
        if date_to:
            query = query.filter(Payment.created_at <= date_to)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        payments = query.order_by(desc(Payment.created_at)).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "payments": payments,
            "total": total,
            "page": page,
            "limit": limit
        }

