"""
Pass Model
Location: /api/models/pass_model.py
Purpose: Pass database model (note: 'pass' is a Python keyword, so using 'pass_model')
"""

from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Pass(BaseModel):
    """Pass model"""
    __tablename__ = 'passes'
    
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id', ondelete='CASCADE'), nullable=False, index=True)
    from_player_id = Column(UUID(as_uuid=True), ForeignKey('players.id'), index=True)
    to_player_id = Column(UUID(as_uuid=True), ForeignKey('players.id'), index=True)
    from_jersey = Column(Integer)
    to_jersey = Column(Integer)
    frame = Column(Integer, nullable=False)
    timestamp = Column(Float)  # Seconds into match
    distance_m = Column(Float)
    successful = Column(Boolean, default=True)
    from_team = Column(Integer)  # 1 or 2
    to_team = Column(Integer)
    position_x = Column(Float)  # Field coordinates
    position_y = Column(Float)
    extra_data = Column(JSONB)  # Additional pass data (renamed from 'metadata' - reserved in SQLAlchemy)
    
    # Relationships
    match = relationship("Match", back_populates="passes")
    from_player = relationship("Player", foreign_keys=[from_player_id], back_populates="passes_from")
    to_player = relationship("Player", foreign_keys=[to_player_id], back_populates="passes_to")

