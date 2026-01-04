"""
Match Model
Location: /api/models/match.py
Purpose: Match database model (multi-sport support)
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Match(BaseModel):
    """Match model"""
    __tablename__ = 'matches'
    
    name = Column(String(255), nullable=False)
    sport_id = Column(String(50), ForeignKey('sports.id'), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    team1_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    team2_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    team1_name = Column(String(255))  # Fallback if team not in database
    team2_name = Column(String(255))
    competition = Column(String(255), index=True)  # 'Debmarine Namibia Premiership', 'MTC Maris Cup', etc.
    venue = Column(String(255))  # 'Sam Nujoma Stadium', 'Dr Hage Geingob Stadium', etc.
    video_path = Column(Text)
    video_url = Column(Text)
    status = Column(String(50), default='uploaded', index=True)  # 'uploaded', 'processing', 'completed', 'failed'
    processing_progress = Column(Integer, default=0)
    processing_error = Column(Text)
    score_team1 = Column(Integer)
    score_team2 = Column(Integer)
    score_details = Column(JSONB)  # For complex scoring (sets, periods, etc.)
    extra_data = Column(JSONB)  # Sport-specific metadata (renamed from 'metadata' - reserved in SQLAlchemy)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    
    # Relationships
    sport = relationship("Sport")
    team1 = relationship("Team", foreign_keys=[team1_id], back_populates="matches_team1")
    team2 = relationship("Team", foreign_keys=[team2_id], back_populates="matches_team2")
    creator = relationship("User", foreign_keys=[created_by], back_populates="matches")
    player_statistics = relationship("PlayerStatistics", back_populates="match", cascade="all, delete-orphan")
    passes = relationship("Pass", back_populates="match", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="match", cascade="all, delete-orphan")
    scouting_reports = relationship("ScoutingReport", back_populates="match")

