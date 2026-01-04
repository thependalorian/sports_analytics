"""
API Dependencies
Location: /api/dependencies.py
Purpose: Dependency injection for FastAPI routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
from pathlib import Path

# Use LanceDB instead of SQLAlchemy
from api.lib.lancedb_adapter import LanceDBAdapter, get_lancedb
from api.models.user import User
from api.services.auth_service import AuthService
from utils.logger import get_logger

logger = get_logger(__name__)
security = HTTPBearer()

class Settings:
    """Application settings"""
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/sports_analytics")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    REFRESH_TOKEN_EXPIRE_DAYS = 30
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Namibian Market Settings
    MTC_MOBILE_MONEY_API_KEY = os.getenv("MTC_MOBILE_MONEY_API_KEY", "")
    MTC_MOBILE_MONEY_API_URL = os.getenv("MTC_MOBILE_MONEY_API_URL", "https://api.mtc.na/mobile-money")
    WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")
    WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "https://api.whatsapp.com")
    AFRICAS_TALKING_API_KEY = os.getenv("AFRICAS_TALKING_API_KEY", "")
    AFRICAS_TALKING_API_URL = os.getenv("AFRICAS_TALKING_API_URL", "https://api.africastalking.com")
    
    # File Storage
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", "1073741824"))  # 1GB
    
    # Redis (for caching and Celery)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()

def get_db() -> LanceDBAdapter:
    """
    Database dependency for FastAPI (LanceDB)
    
    Returns:
        LanceDBAdapter instance
    """
    return get_lancedb()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: LanceDBAdapter = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    auth_service = AuthService(db)
    
    try:
        user = await auth_service.verify_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        Active user object
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: LanceDBAdapter = Depends(get_db)
) -> Optional[User]:
    """
    Get optional user (for public endpoints that can be enhanced with auth)
    
    Args:
        credentials: Optional HTTP Bearer token
        db: Database session
        
    Returns:
        User object or None
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        auth_service = AuthService(db)
        return await auth_service.verify_token(token)
    except Exception:
        return None

