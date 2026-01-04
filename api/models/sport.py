"""
Sport Model
Location: /api/models/sport.py
Purpose: Sport configuration model (multi-sport support)
"""

from sqlalchemy import Column, String, Boolean, Float, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from api.models.base import BaseModel

class Sport(BaseModel):
    """Sport model"""
    __tablename__ = 'sports'
    
    id = Column(String(50), primary_key=True)  # 'football', 'basketball', etc.
    name = Column(String(100), nullable=False)
    icon = Column(String(50))  # Emoji or icon identifier
    field_type = Column(String(50))  # 'rectangular', 'court', 'pitch', 'track'
    field_width = Column(Float)
    field_height = Column(Float)
    field_unit = Column(String(10))  # 'meters', 'yards'
    max_players = Column(Integer)
    config = Column(JSONB)  # Full SportConfig JSON
    is_active = Column(Boolean, default=True)

