"""
Analytics Router
Location: /api/routers/analytics.py
Purpose: Match analytics endpoints (stats, passes, events, possession)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.database import get_db
from api.models.match import Match
from api.models.player import PlayerStatistics
from api.models.pass_model import Pass
from api.models.event import Event
from sqlalchemy import func, and_

router = APIRouter()

@router.get("/matches/{match_id}/analytics/stats")
async def get_match_stats(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    """Get match statistics"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Get quick stats
    from api.services.match_service import MatchService
    service = MatchService(db)
    stats = service.get_match_quick_stats(match_id)
    
    return stats or {}

@router.get("/matches/{match_id}/analytics/passes")
async def get_match_passes(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    """Get pass data for match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    passes = db.query(Pass).filter(Pass.match_id == match_id).all()
    
    return {
        "passes": [
            {
                "id": str(p.id),
                "from_player": p.from_jersey,
                "to_player": p.to_jersey,
                "frame": p.frame,
                "timestamp": p.timestamp,
                "distance_m": p.distance_m,
                "successful": p.successful
            }
            for p in passes
        ],
        "total": len(passes)
    }

@router.get("/matches/{match_id}/analytics/events")
async def get_match_events(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    """Get event data for match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    events = db.query(Event).filter(Event.match_id == match_id).all()
    
    return {
        "events": [
            {
                "id": str(e.id),
                "player": e.jersey_number,
                "event_type": e.event_type,
                "frame": e.frame,
                "timestamp": e.timestamp,
                "position": {"x": e.position_x, "y": e.position_y}
            }
            for e in events
        ],
        "total": len(events)
    }

@router.get("/matches/{match_id}/analytics/possession")
async def get_match_possession(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    """Get possession data for match"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Calculate possession by team
    team1_possession = db.query(func.avg(PlayerStatistics.possession_pct)).filter(
        and_(
            PlayerStatistics.match_id == match_id,
            PlayerStatistics.team == 1
        )
    ).scalar() or 0
    
    team2_possession = db.query(func.avg(PlayerStatistics.possession_pct)).filter(
        and_(
            PlayerStatistics.match_id == match_id,
            PlayerStatistics.team == 2
        )
    ).scalar() or 0
    
    return {
        "team1": round(team1_possession, 1),
        "team2": round(team2_possession, 1),
        "total": round(team1_possession + team2_possession, 1)
    }

