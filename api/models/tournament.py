"""
Tournament Models
Location: /api/models/tournament.py
Purpose: Tournament and TournamentParticipant database models
"""

from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Tournament(BaseModel):
    """Tournament model"""
    __tablename__ = 'tournaments'
    
    name = Column(String(255), nullable=False)
    sport_id = Column(String(50), ForeignKey('sports.id'), nullable=False, index=True)
    organizer = Column(String(255))  # 'MTC', 'NFA', 'UNAM', etc.
    format = Column(String(50))  # 'knockout', 'round_robin', 'league'
    teams_count = Column(Integer)
    prize_money = Column(Numeric(12, 2))
    currency = Column(String(10), default='NAD')
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    venue = Column(String(255))
    status = Column(String(50), default='upcoming', index=True)  # 'upcoming', 'ongoing', 'completed'
    bracket = Column(JSONB)  # Tournament bracket structure
    
    # Relationships
    sport = relationship("Sport")
    participants = relationship("TournamentParticipant", back_populates="tournament", cascade="all, delete-orphan")

class TournamentParticipant(BaseModel):
    """Tournament participant model"""
    __tablename__ = 'tournament_participants'
    
    tournament_id = Column(UUID(as_uuid=True), ForeignKey('tournaments.id', ondelete='CASCADE'), nullable=False, index=True)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'), nullable=False, index=True)
    seed = Column(Integer)
    status = Column(String(50), default='active')  # 'active', 'eliminated', 'winner'
    
    __table_args__ = (
        UniqueConstraint('tournament_id', 'team_id', name='uq_tournament_team'),
    )
    
    # Relationships
    tournament = relationship("Tournament", back_populates="participants")
    team = relationship("Team", back_populates="tournament_participants")

