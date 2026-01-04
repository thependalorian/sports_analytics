"""
Scouting Schemas
Location: /api/schemas/scouting.py
Purpose: Pydantic models for scouting endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal

class ScoutingReportCreate(BaseModel):
    """Create scouting report request"""
    player_id: UUID
    match_id: Optional[UUID] = None
    title: str
    notes: Optional[str] = None
    rating: Decimal = Field(..., ge=0.0, le=10.0, description="Rating from 0.0 to 10.0")
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendation: Optional[str] = None
    is_public: bool = False

class ScoutingReportUpdate(BaseModel):
    """Update scouting report request"""
    title: Optional[str] = None
    notes: Optional[str] = None
    rating: Optional[Decimal] = Field(None, ge=0.0, le=10.0)
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    recommendation: Optional[str] = None

class ScoutingReportResponse(BaseModel):
    """Scouting report response"""
    id: UUID
    player_id: UUID
    player_name: Optional[str] = None
    match_id: Optional[UUID]
    title: str
    notes: Optional[str]
    rating: Decimal
    strengths: Optional[List[str]]
    weaknesses: Optional[List[str]]
    recommendation: Optional[str]
    is_public: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ScoutingSearchRequest(BaseModel):
    """Scouting search request"""
    sport: Optional[str] = None
    position: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    distance_min: Optional[float] = None
    speed_min: Optional[float] = None
    pass_accuracy_min: Optional[float] = None
    team: Optional[str] = None
    competition: Optional[str] = None

class ScoutingSearchResponse(BaseModel):
    """Scouting search response"""
    players: List[Dict[str, Any]]
    total: int

