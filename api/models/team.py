"""
Team Models
Location: /api/models/team.py
Purpose: Team and TeamPlayer database models
"""

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Date, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.base import BaseModel

class Team(BaseModel):
    """Team model"""
    __tablename__ = 'teams'
    
    name = Column(String(255), nullable=False)
    sport_id = Column(String(50), ForeignKey('sports.id'), nullable=False, index=True)
    competition = Column(String(255), index=True)  # 'Debmarine Namibia Premiership', 'MTC Maris Cup', etc.
    location = Column(String(255))  # City/town
    stadium = Column(String(255))
    logo_url = Column(Text)
    founded = Column(Integer)
    championships = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('name', 'sport_id', 'competition', name='uq_team_name_sport_competition'),
    )
    
    # Relationships
    matches_team1 = relationship("Match", foreign_keys="Match.team1_id", back_populates="team1")
    matches_team2 = relationship("Match", foreign_keys="Match.team2_id", back_populates="team2")
    team_players = relationship("TeamPlayer", back_populates="team", cascade="all, delete-orphan")
    tournament_participants = relationship("TournamentParticipant", back_populates="team")
    campus_teams = relationship("CampusTeam", back_populates="team")

class TeamPlayer(BaseModel):
    """Team-Player relationship model"""
    __tablename__ = 'team_players'
    
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id', ondelete='CASCADE'), nullable=False, index=True)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    jersey_number = Column(Integer)
    position = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)
    
    __table_args__ = (
        UniqueConstraint('team_id', 'player_id', 'start_date', name='uq_team_player_start_date'),
    )
    
    # Relationships
    team = relationship("Team", back_populates="team_players")
    player = relationship("Player", back_populates="team_players")

