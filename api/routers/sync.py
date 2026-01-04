"""
Sync Router (Offline-First)
Location: /api/routers/sync.py
Purpose: Offline sync endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.sync_service import SyncService
from api.schemas.sync import SyncRequest, SyncResponse, SyncUploadRequest, SyncUploadResponse

router = APIRouter()

@router.post("/matches", response_model=SyncResponse)
async def sync_matches(
    sync_request: SyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync matches (delta updates)"""
    service = SyncService(db)
    result = service.sync_matches(sync_request, current_user.id)
    return result

@router.post("/players", response_model=SyncResponse)
async def sync_players(
    sync_request: SyncRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync players (delta updates)"""
    service = SyncService(db)
    result = service.sync_players(sync_request, current_user.id)
    return result

@router.post("/upload", response_model=SyncUploadResponse)
async def upload_offline_data(
    upload_request: SyncUploadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload offline data with conflict resolution"""
    service = SyncService(db)
    result = service.upload_offline_data(upload_request, current_user.id)
    return result

