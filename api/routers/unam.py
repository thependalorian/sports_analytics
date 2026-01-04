"""
UNAM Router
Location: /api/routers/unam.py
Purpose: UNAM-specific endpoints (13 campuses)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from uuid import UUID
from datetime import datetime

from api.database import get_db
from api.dependencies import get_current_user
from api.models.user import User
from api.models.unam import UNAMCampus, CampusTeam

router = APIRouter()

@router.get("/campuses")
async def list_campuses(
    db: Session = Depends(get_db)
):
    """List all UNAM campuses"""
    campuses = db.query(UNAMCampus).filter(UNAMCampus.is_active == True).all()
    return {
        "campuses": [
            {
                "id": campus.id,
                "name": campus.name,
                "location": campus.location,
                "region": campus.region
            }
            for campus in campuses
        ]
    }

@router.get("/campuses/{campus_id}/teams")
async def get_campus_teams(
    campus_id: str,
    db: Session = Depends(get_db)
):
    """Get teams for a specific UNAM campus"""
    campus = db.query(UNAMCampus).filter(UNAMCampus.id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    teams = db.query(CampusTeam).filter(
        CampusTeam.campus_id == campus_id,
        CampusTeam.is_active == True
    ).all()
    
    return {
        "campus": {
            "id": campus.id,
            "name": campus.name,
            "location": campus.location
        },
        "teams": [
            {
                "team_id": str(team.team_id),
                "sport": team.sport_id,
                "team_name": team.team.name if team.team else None
            }
            for team in teams
        ]
    }

@router.get("/analytics/multi-campus")
async def get_multi_campus_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get multi-campus analytics (UNAM-specific)"""
    from api.models.unam import UNAMCampus, CampusTeam
    from api.models.team import Team
    from api.models.match import Match
    from sqlalchemy import func, and_
    
    # Get all active campuses
    campuses = db.query(UNAMCampus).filter(UNAMCampus.is_active == True).all()
    
    campus_analytics = []
    total_teams = 0
    total_matches = 0
    
    for campus in campuses:
        # Get teams for this campus
        campus_teams = db.query(CampusTeam).filter(
            CampusTeam.campus_id == campus.id,
            CampusTeam.is_active == True
        ).all()
        
        team_ids = [ct.team_id for ct in campus_teams]
        teams_count = len(team_ids)
        total_teams += teams_count
        
        # Get matches for these teams
        matches_count = 0
        if team_ids:
            matches_count = db.query(func.count(Match.id)).filter(
                and_(
                    or_(Match.team1_id.in_(team_ids), Match.team2_id.in_(team_ids)),
                    Match.deleted_at.is_(None)
                )
            ).scalar() or 0
            total_matches += matches_count
        
        campus_analytics.append({
            "campus_id": campus.id,
            "campus_name": campus.name,
            "location": campus.location,
            "region": campus.region,
            "teams_count": teams_count,
            "matches_count": matches_count,
            "sports": list(set([ct.sport_id for ct in campus_teams]))
        })
    
    return {
        "campuses_analyzed": len(campuses),
        "total_campuses": len(campuses),
        "total_teams": total_teams,
        "total_matches": total_matches,
        "campus_details": campus_analytics,
        "generated_at": datetime.utcnow().isoformat()
    }

