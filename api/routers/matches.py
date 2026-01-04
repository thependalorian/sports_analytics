"""
Matches Router
Location: /api/routers/matches.py
Purpose: Match endpoints (CRUD, status, analytics)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.match_service import MatchService
from api.schemas.match import MatchCreate, MatchUpdate, MatchResponse, MatchListResponse, MatchStatusResponse

router = APIRouter()

@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_data: MatchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new match"""
    service = MatchService(db)
    match = service.create_match(match_data, current_user.id)
    return match

@router.get("", response_model=MatchListResponse)
async def list_matches(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    sport: Optional[str] = None,
    team: Optional[str] = None,
    competition: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List matches with filters"""
    service = MatchService(db)
    result = service.list_matches(
        page=page,
        limit=limit,
        status=status,
        sport=sport,
        team=team,
        competition=competition,
        date_from=date_from,
        date_to=date_to,
        search=search
    )
    return MatchListResponse(**result)

@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    """Get match by ID"""
    service = MatchService(db)
    match = service.get_match(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: UUID,
    match_data: MatchUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update match"""
    service = MatchService(db)
    match = service.update_match(match_id, match_data)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_match(
    match_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete match"""
    service = MatchService(db)
    success = service.delete_match(match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")

@router.get("/{match_id}/status", response_model=MatchStatusResponse)
async def get_match_status(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    """Get match processing status"""
    service = MatchService(db)
    status_data = service.get_match_status(match_id)
    if not status_data:
        raise HTTPException(status_code=404, detail="Match not found")
    return status_data

