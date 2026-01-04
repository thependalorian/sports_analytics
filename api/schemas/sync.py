"""
Sync Schemas (Offline-First)
Location: /api/schemas/sync.py
Purpose: Pydantic models for sync endpoints
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class SyncRequest(BaseModel):
    """Sync request"""
    last_sync: datetime
    device_id: str

class SyncResponse(BaseModel):
    """Sync response"""
    matches: Optional[List[Dict[str, Any]]] = None
    players: Optional[List[Dict[str, Any]]] = None
    teams: Optional[List[Dict[str, Any]]] = None
    deleted: Optional[List[str]] = None
    sync_timestamp: datetime

class SyncUploadItem(BaseModel):
    """Sync upload item"""
    type: str  # 'match', 'player', 'team', etc.
    action: str  # 'create', 'update', 'delete'
    data: Dict[str, Any]
    timestamp: datetime

class SyncUploadRequest(BaseModel):
    """Sync upload request"""
    device_id: str
    data: List[SyncUploadItem]

class SyncUploadResponse(BaseModel):
    """Sync upload response"""
    synced: int
    failed: int
    conflicts: List[Dict[str, Any]]
    sync_timestamp: datetime

