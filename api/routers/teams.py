"""
Teams Router
Location: /api/routers/teams.py
Purpose: Team endpoints (CRUD, profile, standings)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.team_service import TeamService
from api.schemas.team import TeamCreate, TeamUpdate, TeamResponse, TeamListResponse

router = APIRouter()

@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
async def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new team"""
    service = TeamService(db)
    team = service.create_team(team_data)
    return team

@router.get("", response_model=TeamListResponse)
async def list_teams(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sport: Optional[str] = None,
    competition: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """List teams with filters"""
    service = TeamService(db)
    result = service.list_teams(
        page=page,
        limit=limit,
        sport=sport,
        competition=competition,
        search=search,
        sort_by=sort_by,
        order=order
    )
    return TeamListResponse(**result)

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: UUID,
    db: Session = Depends(get_db)
):
    """Get team by ID"""
    service = TeamService(db)
    team = service.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.get("/{team_id}/profile")
async def get_team_profile(
    team_id: UUID,
    db: Session = Depends(get_db)
):
    """Get team profile with squad and season stats"""
    service = TeamService(db)
    profile = service.get_team_profile(team_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Team not found")
    return profile

@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: UUID,
    team_data: TeamUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update team"""
    service = TeamService(db)
    team = service.update_team(team_id, team_data)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

