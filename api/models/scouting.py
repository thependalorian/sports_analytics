"""
Scouting Model
Location: /api/models/scouting.py
Purpose: ScoutingReport database model
"""

from sqlalchemy import Column, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class ScoutingReport(BaseModel):
    """Scouting report model"""
    __tablename__ = 'scouting_reports'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id'), index=True)
    title = Column(String(255), nullable=False)
    notes = Column(Text)
    rating = Column(Float)  # 0.0 to 10.0
    strengths = Column(ARRAY(Text))
    weaknesses = Column(ARRAY(Text))
    recommendation = Column(Text)
    is_public = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="scouting_reports")
    player = relationship("Player", back_populates="scouting_reports")
    match = relationship("Match", back_populates="scouting_reports")

