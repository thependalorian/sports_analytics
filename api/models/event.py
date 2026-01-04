"""
Event Model
Location: /api/models/event.py
Purpose: Event database model (universal event types)
"""

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Event(BaseModel):
    """Event model"""
    __tablename__ = 'events'
    
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id', ondelete='CASCADE'), nullable=False, index=True)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id'), index=True)
    jersey_number = Column(Integer)
    team = Column(Integer)  # 1 or 2
    event_type = Column(String(50), nullable=False, index=True)  # 'sprint', 'cluster', 'shot', 'goal', 'foul', etc.
    frame = Column(Integer, nullable=False)
    timestamp = Column(Float)  # Seconds into match
    position_x = Column(Float)
    position_y = Column(Float)
    extra_data = Column(JSONB)  # Event-specific data (renamed from 'metadata' - reserved in SQLAlchemy)
    
    # Relationships
    match = relationship("Match", back_populates="events")
    player = relationship("Player", back_populates="events")

