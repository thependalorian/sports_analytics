"""
Sync Models
Location: /api/models/sync.py
Purpose: Offline sync models (sync_queue, sync_history)
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class SyncQueue(BaseModel):
    """Offline sync queue model"""
    __tablename__ = 'sync_queue'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    device_id = Column(String(255), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # 'match', 'player', 'team', etc.
    entity_id = Column(UUID(as_uuid=True))
    action = Column(String(50), nullable=False)  # 'create', 'update', 'delete'
    data = Column(JSONB, nullable=False)
    priority = Column(Integer, default=0)  # Higher = more important
    status = Column(String(50), default='pending', index=True)  # 'pending', 'synced', 'failed', 'conflict'
    conflict_resolution = Column(String(50))  # 'server_wins', 'client_wins', 'merge'
    error_message = Column(Text)
    synced_at = Column(DateTime)
    
    # Relationships
    user = relationship("User")

class SyncHistory(BaseModel):
    """Sync history model"""
    __tablename__ = 'sync_history'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    device_id = Column(String(255), nullable=False, index=True)
    last_sync_at = Column(DateTime, nullable=False)
    entities_synced = Column(Integer, default=0)
    conflicts_resolved = Column(Integer, default=0)
    errors = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User")

