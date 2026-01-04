"""
Scouting Service
Location: /api/services/scouting_service.py
Purpose: Business logic for scouting operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List, Dict, Any
from uuid import UUID
from decimal import Decimal

from api.models.scouting import ScoutingReport
from api.models.player import Player, PlayerStatistics
from api.models.team import Team, TeamPlayer
from api.schemas.scouting import ScoutingReportCreate, ScoutingReportUpdate, ScoutingSearchRequest
from utils.logger import get_logger

logger = get_logger(__name__)

class ScoutingService:
    """Scouting service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_report(self, report_data: ScoutingReportCreate, user_id: UUID) -> ScoutingReport:
        """Create a new scouting report"""
        report = ScoutingReport(
            user_id=user_id,
            player_id=report_data.player_id,
            match_id=report_data.match_id,
            title=report_data.title,
            notes=report_data.notes,
            rating=report_data.rating,
            strengths=report_data.strengths or [],
            weaknesses=report_data.weaknesses or [],
            recommendation=report_data.recommendation,
            is_public=report_data.is_public
        )
        
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        
        logger.info(f"Scouting report created: {report.id}")
        return report
    
    def get_report(self, report_id: UUID) -> Optional[ScoutingReport]:
        """Get scouting report by ID"""
        return self.db.query(ScoutingReport).filter(
            and_(ScoutingReport.id == report_id, ScoutingReport.deleted_at.is_(None))
        ).first()
    
    def list_reports(
        self,
        page: int = 1,
        limit: int = 20,
        player_id: Optional[UUID] = None,
        match_id: Optional[UUID] = None,
        rating_min: Optional[float] = None,
        sort_by: Optional[str] = None,
        order: str = "desc"
    ) -> Dict[str, Any]:
        """List scouting reports with filters"""
        query = self.db.query(ScoutingReport).filter(ScoutingReport.deleted_at.is_(None))
        
        # Apply filters
        if player_id:
            query = query.filter(ScoutingReport.player_id == player_id)
        if match_id:
            query = query.filter(ScoutingReport.match_id == match_id)
        if rating_min:
            query = query.filter(ScoutingReport.rating >= rating_min)
        
        # Apply sorting
        if sort_by:
            if sort_by == "rating":
                order_func = desc(ScoutingReport.rating) if order == "desc" else ScoutingReport.rating
            elif sort_by == "created_at":
                order_func = desc(ScoutingReport.created_at) if order == "desc" else ScoutingReport.created_at
            query = query.order_by(order_func)
        else:
            query = query.order_by(desc(ScoutingReport.created_at))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        reports = query.offset((page - 1) * limit).limit(limit).all()
        
        return {
            "reports": reports,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    def search_players(self, search_params: ScoutingSearchRequest) -> Dict[str, Any]:
        """Search players for scouting"""
        query = self.db.query(Player).join(PlayerStatistics).filter(
            Player.deleted_at.is_(None)
        )
        
        # Apply filters
        if search_params.sport:
            query = query.filter(Player.sport_id == search_params.sport)
        if search_params.position:
            query = query.filter(Player.position == search_params.position)
        if search_params.team:
            # Join with teams
            from api.models.team import TeamPlayer
            query = query.join(TeamPlayer).join(Team).filter(
                Team.name.ilike(f"%{search_params.team}%")
            )
        
        # Get aggregated stats
        stats_query = self.db.query(
            PlayerStatistics.player_id,
            func.count(PlayerStatistics.id).label('matches_analyzed'),
            func.avg(PlayerStatistics.total_distance_m).label('avg_distance'),
            func.avg(PlayerStatistics.avg_speed_kmh).label('avg_speed'),
            func.avg(PlayerStatistics.pass_accuracy_pct).label('avg_pass_accuracy')
        ).group_by(PlayerStatistics.player_id)
        
        # Apply stat filters
        if search_params.distance_min:
            stats_query = stats_query.having(func.avg(PlayerStatistics.total_distance_m) >= search_params.distance_min * 1000)
        if search_params.speed_min:
            stats_query = stats_query.having(func.avg(PlayerStatistics.avg_speed_kmh) >= search_params.speed_min)
        if search_params.pass_accuracy_min:
            stats_query = stats_query.having(func.avg(PlayerStatistics.pass_accuracy_pct) >= search_params.pass_accuracy_min)
        
        # Get player IDs matching criteria
        matching_player_ids = [row.player_id for row in stats_query.all()]
        query = query.filter(Player.id.in_(matching_player_ids))
        
        players = query.all()
        
        # Get average scout rating for each player
        for player in players:
            avg_rating = self.db.query(func.avg(ScoutingReport.rating)).filter(
                ScoutingReport.player_id == player.id
            ).scalar()
            player.scout_rating = float(avg_rating) if avg_rating else None
        
        return {
            "players": player_list,
            "total": len(player_list)
        }
    
    def update_report(self, report_id: UUID, report_data: ScoutingReportUpdate) -> Optional[ScoutingReport]:
        """Update scouting report"""
        report = self.get_report(report_id)
        if not report:
            return None
        
        if report_data.title is not None:
            report.title = report_data.title
        if report_data.notes is not None:
            report.notes = report_data.notes
        if report_data.rating is not None:
            report.rating = report_data.rating
        if report_data.strengths is not None:
            report.strengths = report_data.strengths
        if report_data.weaknesses is not None:
            report.weaknesses = report_data.weaknesses
        if report_data.recommendation is not None:
            report.recommendation = report_data.recommendation
        
        self.db.commit()
        self.db.refresh(report)
        
        logger.info(f"Scouting report updated: {report.id}")
        return report

