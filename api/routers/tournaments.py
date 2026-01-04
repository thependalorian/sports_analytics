"""
Tournaments Router
Location: /api/routers/tournaments.py
Purpose: Tournament endpoints (CRUD, bracket, standings)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.tournament_service import TournamentService
from api.schemas.tournament import (
    TournamentCreate,
    TournamentUpdate,
    TournamentResponse,
    TournamentListResponse,
    TournamentStandingsResponse
)

router = APIRouter()

@router.post("", response_model=TournamentResponse, status_code=status.HTTP_201_CREATED)
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new tournament"""
    service = TournamentService(db)
    tournament = service.create_tournament(tournament_data)
    return tournament

@router.get("", response_model=TournamentListResponse)
async def list_tournaments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sport: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List tournaments with filters"""
    service = TournamentService(db)
    result = service.list_tournaments(
        page=page,
        limit=limit,
        sport=sport,
        status=status,
        search=search
    )
    return TournamentListResponse(**result)

@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: UUID,
    db: Session = Depends(get_db)
):
    """Get tournament by ID"""
    service = TournamentService(db)
    tournament = service.get_tournament(tournament_id)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@router.get("/{tournament_id}/standings", response_model=TournamentStandingsResponse)
async def get_tournament_standings(
    tournament_id: UUID,
    db: Session = Depends(get_db)
):
    """Get tournament standings"""
    service = TournamentService(db)
    standings = service.get_tournament_standings(tournament_id)
    if not standings:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return standings

@router.put("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: UUID,
    tournament_data: TournamentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update tournament"""
    service = TournamentService(db)
    tournament = service.update_tournament(tournament_id, tournament_data)
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

