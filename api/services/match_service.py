"""
Match Service
Location: /api/services/match_service.py
Purpose: Business logic for match operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from api.models.match import Match
from api.models.player import PlayerStatistics
from api.models.pass_model import Pass
from api.models.event import Event
from api.schemas.match import MatchCreate, MatchUpdate
from utils.logger import get_logger

logger = get_logger(__name__)

class MatchService:
    """Match service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_match(self, match_data: MatchCreate, user_id: UUID) -> Match:
        """Create a new match"""
        match = Match(
            name=match_data.name,
            sport_id=match_data.sport,
            date=match_data.date,
            team1_id=match_data.team1_id,
            team2_id=match_data.team2_id,
            team1_name=match_data.team1_name,
            team2_name=match_data.team2_name,
            competition=match_data.competition,
            venue=match_data.venue,
            status='uploaded',
            created_by=user_id
        )
        
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        
        logger.info(f"Match created: {match.id} - {match.name}")
        return match
    
    def get_match(self, match_id: UUID) -> Optional[Match]:
        """Get match by ID"""
        return self.db.query(Match).filter(
            and_(Match.id == match_id, Match.deleted_at.is_(None))
        ).first()
    
    def list_matches(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        sport: Optional[str] = None,
        team: Optional[str] = None,
        competition: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """List matches with filters"""
        query = self.db.query(Match).filter(Match.deleted_at.is_(None))
        
        # Apply filters
        if status:
            query = query.filter(Match.status == status)
        if sport:
            query = query.filter(Match.sport_id == sport)
        if team:
            query = query.filter(
                or_(
                    Match.team1_name.ilike(f"%{team}%"),
                    Match.team2_name.ilike(f"%{team}%")
                )
            )
        if competition:
            query = query.filter(Match.competition == competition)
        if date_from:
            query = query.filter(Match.date >= date_from)
        if date_to:
            query = query.filter(Match.date <= date_to)
        if search:
            query = query.filter(Match.name.ilike(f"%{search}%"))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        matches = query.order_by(desc(Match.date)).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "matches": matches,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    
    def update_match(self, match_id: UUID, match_data: MatchUpdate) -> Optional[Match]:
        """Update match"""
        match = self.get_match(match_id)
        if not match:
            return None
        
        # Update fields
        if match_data.name is not None:
            match.name = match_data.name
        if match_data.date is not None:
            match.date = match_data.date
        if match_data.venue is not None:
            match.venue = match_data.venue
        if match_data.score_team1 is not None:
            match.score_team1 = match_data.score_team1
        if match_data.score_team2 is not None:
            match.score_team2 = match_data.score_team2
        if match_data.score_details is not None:
            match.score_details = match_data.score_details
        
        self.db.commit()
        self.db.refresh(match)
        
        logger.info(f"Match updated: {match.id}")
        return match
    
    def delete_match(self, match_id: UUID) -> bool:
        """Soft delete match"""
        match = self.get_match(match_id)
        if not match:
            return False
        
        match.deleted_at = datetime.utcnow()
        self.db.commit()
        
        logger.info(f"Match deleted: {match.id}")
        return True
    
    def get_match_status(self, match_id: UUID) -> Optional[Dict[str, Any]]:
        """Get match processing status"""
        match = self.get_match(match_id)
        if not match:
            return None
        
        # Define processing steps
        processing_steps = {
            'uploaded': {'step': 'Video Upload', 'progress': 10},
            'processing': {'step': 'Video Analysis', 'progress': 50},
            'analyzing': {'step': 'Data Analysis', 'progress': 75},
            'completed': {'step': 'Complete', 'progress': 100},
            'failed': {'step': 'Failed', 'progress': 0}
        }
        
        current_step_info = processing_steps.get(match.status, {'step': 'Unknown', 'progress': 0})
        current_step = current_step_info['step']
        
        # Estimate time remaining based on status and progress
        estimated_time_remaining = None
        if match.status == 'processing':
            # Estimate: 60 seconds per 1% progress remaining
            remaining_progress = 100 - match.processing_progress
            estimated_time_remaining = remaining_progress * 60  # seconds
        elif match.status == 'analyzing':
            # Estimate: 30 seconds per 1% progress remaining
            remaining_progress = 100 - match.processing_progress
            estimated_time_remaining = remaining_progress * 30  # seconds
        
        return {
            "status": match.status,
            "progress": match.processing_progress,
            "current_step": current_step,
            "estimated_time_remaining": int(estimated_time_remaining) if estimated_time_remaining else None
        }
    
    def get_match_quick_stats(self, match_id: UUID) -> Optional[Dict[str, Any]]:
        """Get quick statistics for match"""
        match = self.get_match(match_id)
        if not match:
            return None
        
        # Get total passes
        total_passes = self.db.query(func.count(Pass.id)).filter(
            Pass.match_id == match_id
        ).scalar() or 0
        
        # Get possession stats
        team1_possession = self.db.query(func.avg(PlayerStatistics.possession_pct)).filter(
            and_(
                PlayerStatistics.match_id == match_id,
                PlayerStatistics.team == 1
            )
        ).scalar() or 0
        
        team2_possession = self.db.query(func.avg(PlayerStatistics.possession_pct)).filter(
            and_(
                PlayerStatistics.match_id == match_id,
                PlayerStatistics.team == 2
            )
        ).scalar() or 0
        
        # Get total distance
        team1_distance = self.db.query(func.sum(PlayerStatistics.total_distance_m)).filter(
            and_(
                PlayerStatistics.match_id == match_id,
                PlayerStatistics.team == 1
            )
        ).scalar() or 0
        
        team2_distance = self.db.query(func.sum(PlayerStatistics.total_distance_m)).filter(
            and_(
                PlayerStatistics.match_id == match_id,
                PlayerStatistics.team == 2
            )
        ).scalar() or 0
        
        return {
            "total_passes": total_passes,
            "possession_team1": round(team1_possession, 1),
            "possession_team2": round(team2_possession, 1),
            "total_distance_team1": round((team1_distance or 0) / 1000, 1),  # Convert to km
            "total_distance_team2": round((team2_distance or 0) / 1000, 1)
        }

