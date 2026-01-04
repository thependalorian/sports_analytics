"""
Team Schemas
Location: /api/schemas/team.py
Purpose: Pydantic models for team endpoints
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class TeamCreate(BaseModel):
    """Create team request"""
    name: str
    sport: str
    competition: Optional[str] = None
    location: Optional[str] = None
    stadium: Optional[str] = None
    founded: Optional[int] = None

class TeamUpdate(BaseModel):
    """Update team request"""
    name: Optional[str] = None
    competition: Optional[str] = None
    location: Optional[str] = None
    stadium: Optional[str] = None
    logo_url: Optional[str] = None

class TeamResponse(BaseModel):
    """Team response"""
    id: UUID
    name: str
    sport: str
    competition: Optional[str]
    location: Optional[str]
    stadium: Optional[str]
    logo_url: Optional[str]
    founded: Optional[int]
    championships: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TeamListResponse(BaseModel):
    """Team list response"""
    teams: List[TeamResponse]
    total: int
    page: int
    limit: int

