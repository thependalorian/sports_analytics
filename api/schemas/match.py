"""
Match Schemas
Location: /api/schemas/match.py
Purpose: Pydantic models for match endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class MatchCreate(BaseModel):
    """Create match request"""
    name: str
    sport: str = "football"  # Sport ID
    date: datetime
    team1_name: str
    team2_name: str
    team1_id: Optional[UUID] = None
    team2_id: Optional[UUID] = None
    competition: Optional[str] = None
    venue: Optional[str] = None

class MatchUpdate(BaseModel):
    """Update match request"""
    name: Optional[str] = None
    date: Optional[datetime] = None
    venue: Optional[str] = None
    score_team1: Optional[int] = None
    score_team2: Optional[int] = None
    score_details: Optional[Dict[str, Any]] = None

class MatchResponse(BaseModel):
    """Match response"""
    id: UUID
    name: str
    sport: str
    date: datetime
    team1_name: Optional[str]
    team2_name: Optional[str]
    team1_id: Optional[UUID]
    team2_id: Optional[UUID]
    competition: Optional[str]
    venue: Optional[str]
    video_path: Optional[str]
    video_url: Optional[str]
    status: str
    processing_progress: int
    score_team1: Optional[int]
    score_team2: Optional[int]
    score_details: Optional[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MatchListResponse(BaseModel):
    """Match list response"""
    matches: list[MatchResponse]
    total: int
    page: int
    limit: int
    pages: int

class MatchStatusResponse(BaseModel):
    """Match processing status response"""
    status: str
    progress: int
    current_step: Optional[str] = None
    estimated_time_remaining: Optional[int] = None

