"""
Authentication Service
Location: /api/services/auth_service.py
Purpose: Authentication and authorization business logic
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
from uuid import uuid4, UUID

from api.models.user import User, UserSession
import os
# Avoid circular import - get settings directly
from utils.logger import get_logger

logger = get_logger(__name__)

class AuthService:
    """Authentication service"""
    
    def __init__(self, db: Session):
        self.db = db
        # Get settings directly to avoid circular import
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_access_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        if expires_delta is None:
            expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        
        expire = datetime.utcnow() + expires_delta
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create refresh token"""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": str(uuid4())
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    async def verify_token(self, token: str) -> Optional[User]:
        """Verify JWT token and return user"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            
            if not user_id:
                return None
            
            user = self.db.query(User).filter(
                and_(User.id == user_id, User.deleted_at.is_(None))
            ).first()
            
            return user
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    def register_user(
        self,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        organization: Optional[str] = None,
        campus: Optional[str] = None
    ) -> User:
        """Register new user"""
        # Check if user exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create user
        user = User(
            email=email,
            password_hash=self.hash_password(password),
            full_name=full_name,
            organization=organization,
            campus=campus,
            is_verified=False,
            is_active=True
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        logger.info(f"User registered: {user.email}")
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.db.query(User).filter(
            and_(User.email == email, User.deleted_at.is_(None))
        ).first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def create_session(self, user_id: str, device_info: Optional[dict] = None, 
                      ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> UserSession:
        """Create user session with refresh token"""
        """Create user session with refresh token"""
        refresh_token = self.create_refresh_token(user_id)
        expires_at = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        session = UserSession(
            user_id=user_id,
            refresh_token=refresh_token,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def revoke_session(self, refresh_token: str) -> bool:
        """Revoke user session"""
        session = self.db.query(UserSession).filter(
            UserSession.refresh_token == refresh_token
        ).first()
        
        if not session:
            return False
        
        session.revoked = True
        session.revoked_at = datetime.utcnow()
        self.db.commit()
        
        return True

