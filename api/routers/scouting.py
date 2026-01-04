"""
Scouting Router
Location: /api/routers/scouting.py
Purpose: Scouting endpoints (reports, player search)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.services.scouting_service import ScoutingService
from api.schemas.scouting import (
    ScoutingReportCreate,
    ScoutingReportUpdate,
    ScoutingReportResponse,
    ScoutingSearchRequest,
    ScoutingSearchResponse
)

router = APIRouter()

@router.post("/reports", response_model=ScoutingReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ScoutingReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new scouting report"""
    service = ScoutingService(db)
    report = service.create_report(report_data, current_user.id)
    return report

@router.get("/reports", response_model=list[ScoutingReportResponse])
async def list_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    player_id: Optional[UUID] = None,
    match_id: Optional[UUID] = None,
    rating_min: Optional[float] = None,
    sort_by: Optional[str] = None,
    order: str = Query("desc", pattern="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List scouting reports"""
    service = ScoutingService(db)
    result = service.list_reports(
        page=page,
        limit=limit,
        player_id=player_id,
        match_id=match_id,
        rating_min=rating_min,
        sort_by=sort_by,
        order=order
    )
    return result["reports"]

@router.get("/reports/{report_id}", response_model=ScoutingReportResponse)
async def get_report(
    report_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get scouting report by ID"""
    service = ScoutingService(db)
    report = service.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.put("/reports/{report_id}", response_model=ScoutingReportResponse)
async def update_report(
    report_id: UUID,
    report_data: ScoutingReportUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update scouting report"""
    service = ScoutingService(db)
    report = service.update_report(report_id, report_data)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/players/search", response_model=ScoutingSearchResponse)
async def search_players(
    search_params: ScoutingSearchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search players for scouting"""
    service = ScoutingService(db)
    result = service.search_players(search_params)
    return result

