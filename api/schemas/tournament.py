"""
Tournament Schemas
Location: /api/schemas/tournament.py
Purpose: Pydantic models for tournament endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal

class TournamentCreate(BaseModel):
    """Create tournament request"""
    name: str
    sport: str
    organizer: Optional[str] = None
    format: str = "knockout"  # 'knockout', 'round_robin', 'league'
    teams_count: Optional[int] = None
    prize_money: Optional[Decimal] = None
    currency: str = "NAD"
    start_date: date
    end_date: date
    venue: Optional[str] = None

class TournamentUpdate(BaseModel):
    """Update tournament request"""
    name: Optional[str] = None
    status: Optional[str] = None
    bracket: Optional[Dict[str, Any]] = None

class TournamentResponse(BaseModel):
    """Tournament response"""
    id: UUID
    name: str
    sport: str
    organizer: Optional[str]
    format: str
    teams_count: Optional[int]
    prize_money: Optional[Decimal]
    currency: str
    start_date: date
    end_date: date
    venue: Optional[str]
    status: str
    bracket: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TournamentListResponse(BaseModel):
    """Tournament list response"""
    tournaments: List[TournamentResponse]
    total: int
    page: int
    limit: int

class TournamentStandingsResponse(BaseModel):
    """Tournament standings response"""
    tournament_id: UUID
    standings: List[Dict[str, Any]]

