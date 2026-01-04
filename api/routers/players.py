"""
Players Router
Location: /api/routers/players.py
Purpose: Player endpoints (CRUD, profile, statistics)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.player_service import PlayerService
from api.schemas.player import (
    PlayerCreate,
    PlayerUpdate,
    PlayerResponse,
    PlayerListResponse,
    PlayerStatisticsResponse
)

router = APIRouter()

@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_data: PlayerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new player"""
    service = PlayerService(db)
    player = service.create_player(player_data)
    return player

@router.get("", response_model=PlayerListResponse)
async def list_players(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sport: Optional[str] = None,
    team: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """List players with filters"""
    service = PlayerService(db)
    result = service.list_players(
        page=page,
        limit=limit,
        sport=sport,
        team=team,
        search=search,
        sort_by=sort_by,
        order=order
    )
    return PlayerListResponse(**result)

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: UUID,
    db: Session = Depends(get_db)
):
    """Get player by ID"""
    service = PlayerService(db)
    player = service.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.get("/{player_id}/profile")
async def get_player_profile(
    player_id: UUID,
    db: Session = Depends(get_db)
):
    """Get player profile with career stats"""
    service = PlayerService(db)
    profile = service.get_player_profile(player_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Player not found")
    return profile

@router.put("/{player_id}", response_model=PlayerResponse)
async def update_player(
    player_id: UUID,
    player_data: PlayerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update player"""
    service = PlayerService(db)
    player = service.update_player(player_id, player_data)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

