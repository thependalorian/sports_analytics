"""
Player Models
Location: /api/models/player.py
Purpose: Player and PlayerStatistics database models
"""

from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Player(BaseModel):
    """Player model (universal, multi-sport)"""
    __tablename__ = 'players'
    
    name = Column(String(255), nullable=False, index=True)
    sport_id = Column(String(50), ForeignKey('sports.id'), nullable=False, index=True)
    jersey_number = Column(Integer)
    date_of_birth = Column(Date)
    nationality = Column(String(100), default='Namibian', index=True)
    height_cm = Column(Integer)
    weight_kg = Column(Float)
    position = Column(String(50))
    photo_url = Column(Text)
    extra_data = Column(JSONB)  # Sport-specific player data (renamed from 'metadata' - reserved in SQLAlchemy)
    
    # Relationships
    sport = relationship("Sport")
    team_players = relationship("TeamPlayer", back_populates="player")
    player_statistics = relationship("PlayerStatistics", back_populates="player", cascade="all, delete-orphan")
    passes_from = relationship("Pass", foreign_keys="Pass.from_player_id", back_populates="from_player")
    passes_to = relationship("Pass", foreign_keys="Pass.to_player_id", back_populates="to_player")
    events = relationship("Event", back_populates="player")
    scouting_reports = relationship("ScoutingReport", back_populates="player")

class PlayerStatistics(BaseModel):
    """Player statistics per match"""
    __tablename__ = 'player_statistics'
    
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    match_id = Column(UUID(as_uuid=True), ForeignKey('matches.id', ondelete='CASCADE'), nullable=False, index=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), index=True)
    track_id = Column(Integer)
    team = Column(Integer)  # 1 or 2 (for match context)
    total_distance_m = Column(Float)
    avg_speed_kmh = Column(Float)
    max_speed_kmh = Column(Float)
    passes_made = Column(Integer, default=0)
    passes_received = Column(Integer, default=0)
    successful_passes = Column(Integer, default=0)
    pass_accuracy_pct = Column(Float)
    possession_time_sec = Column(Float)
    possession_pct = Column(Float)
    sprints = Column(Integer, default=0)
    stats = Column(JSONB)  # Sport-specific statistics
    
    __table_args__ = (
        {'extend_existing': True},
    )
    
    # Relationships
    player = relationship("Player", back_populates="player_statistics")
    match = relationship("Match", back_populates="player_statistics")
    team_rel = relationship("Team", foreign_keys=[team_id])

