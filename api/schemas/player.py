"""
Player Schemas
Location: /api/schemas/player.py
Purpose: Pydantic models for player endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from uuid import UUID

class PlayerCreate(BaseModel):
    """Create player request"""
    name: str
    sport: str
    jersey_number: Optional[int] = None
    date_of_birth: Optional[date] = None
    nationality: str = "Namibian"
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    position: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PlayerUpdate(BaseModel):
    """Update player request"""
    name: Optional[str] = None
    jersey_number: Optional[int] = None
    position: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class PlayerResponse(BaseModel):
    """Player response"""
    id: UUID
    name: str
    sport: str
    jersey_number: Optional[int]
    date_of_birth: Optional[date]
    nationality: str
    height_cm: Optional[int]
    weight_kg: Optional[float]
    position: Optional[str]
    photo_url: Optional[str]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PlayerListResponse(BaseModel):
    """Player list response"""
    players: List[PlayerResponse]
    total: int
    page: int
    limit: int

class PlayerStatisticsResponse(BaseModel):
    """Player statistics response"""
    id: UUID
    player_id: UUID
    match_id: UUID
    team_id: Optional[UUID]
    track_id: Optional[int]
    team: Optional[int]
    total_distance_m: Optional[float]
    avg_speed_kmh: Optional[float]
    max_speed_kmh: Optional[float]
    passes_made: int
    passes_received: int
    successful_passes: int
    pass_accuracy_pct: Optional[float]
    possession_time_sec: Optional[float]
    possession_pct: Optional[float]
    sprints: int
    stats: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

