"""
Authentication Router
Location: /api/routers/auth.py
Purpose: Authentication endpoints (login, register, refresh, logout)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from api.database import get_db
from api.dependencies import get_current_user, get_settings, security
from api.models.user import User
from api.services.auth_service import AuthService
from api.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChange
)
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()
settings = get_settings()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register new user"""
    auth_service = AuthService(db)
    
    try:
        user = auth_service.register_user(
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            organization=user_data.organization,
            campus=user_data.campus
        )
        
        # Create session
        session = auth_service.create_session(str(user.id))
        
        # Generate tokens
        access_token = auth_service.create_access_token(str(user.id))
        refresh_token = session.refresh_token
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user"""
    auth_service = AuthService(db)
    
    user = auth_service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create session
    session = auth_service.create_session(str(user.id))
    
    # Generate tokens
    access_token = auth_service.create_access_token(str(user.id))
    refresh_token = session.refresh_token
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user={
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name
        }
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    auth_service = AuthService(db)
    
    # Verify refresh token
    try:
        payload = jwt.decode(refresh_data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Generate new access token
        access_token = auth_service.create_access_token(user_id)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_data.refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user={"id": user_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Logout user (revoke refresh token)"""
    auth_service = AuthService(db)
    
    success = auth_service.revoke_session(refresh_data.refresh_token)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return {"message": "Logged out successfully"}

@router.post("/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    from api.models.user import User
    from api.models.password_reset import PasswordResetToken
    from api.lib.email_service import EmailService, generate_reset_token, hash_reset_token
    from datetime import datetime, timedelta
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        # Don't reveal if user exists (security best practice)
        return {"message": "If the email exists, a password reset link has been sent"}
    
    # Generate reset token
    reset_token = generate_reset_token()
    token_hash = hash_reset_token(reset_token)
    
    # Create or update reset token
    existing_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used == False
    ).first()
    
    if existing_token:
        existing_token.token_hash = token_hash
        existing_token.expires_at = datetime.utcnow() + timedelta(hours=1)
    else:
        reset_token_record = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        db.add(reset_token_record)
    
    db.commit()
    
    # Send email
    email_service = EmailService()
    email_sent = email_service.send_password_reset_email(user.email, reset_token)
    
    if not email_sent:
        logger.error(f"Failed to send password reset email to {user.email}")
        return {"message": "Error sending email. Please try again later."}
    
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    request: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """Reset password with token"""
    from api.models.user import User
    from api.models.password_reset import PasswordResetToken
    from api.services.auth_service import AuthService
    from api.lib.email_service import hash_reset_token
    
    # Hash the provided token
    token_hash = hash_reset_token(request.token)
    
    # Find valid reset token
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()
    
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Get user
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    auth_service = AuthService(db)
    user.password_hash = auth_service.hash_password(request.new_password)
    
    # Mark token as used
    reset_token.used = True
    
    db.commit()
    
    logger.info(f"Password reset successful for user {user.email}")
    return {"message": "Password reset successfully"}

@router.post("/change-password")
async def change_password(
    request: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change password"""
    auth_service = AuthService(db)
    
    # Verify current password
    if not auth_service.verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.password_hash = auth_service.hash_password(request.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}

