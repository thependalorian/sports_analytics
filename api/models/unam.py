"""
UNAM Models
Location: /api/models/unam.py
Purpose: UNAM campus models (13 campuses)
"""

from sqlalchemy import Column, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class UNAMCampus(BaseModel):
    """UNAM campus model"""
    __tablename__ = 'unam_campuses'
    
    id = Column(String(50), primary_key=True)  # 'windhoek_main', 'oshakati', etc.
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    region = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    campus_teams = relationship("CampusTeam", back_populates="campus", cascade="all, delete-orphan")

class CampusTeam(BaseModel):
    """Campus-team relationship model"""
    __tablename__ = 'campus_teams'
    
    campus_id = Column(String(50), ForeignKey('unam_campuses.id', ondelete='CASCADE'), nullable=False, index=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False, index=True)
    sport_id = Column(String(50), ForeignKey('sports.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('campus_id', 'team_id', 'sport_id', name='uq_campus_team_sport'),
    )
    
    # Relationships
    campus = relationship("UNAMCampus", back_populates="campus_teams")
    team = relationship("Team", back_populates="campus_teams")
    sport = relationship("Sport")

