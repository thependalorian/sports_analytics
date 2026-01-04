"""
Team Service
Location: /api/services/team_service.py
Purpose: Business logic for team operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List, Dict, Any
from uuid import UUID

from api.models.team import Team, TeamPlayer
from api.models.match import Match
from api.models.player import Player, PlayerStatistics
from api.schemas.team import TeamCreate, TeamUpdate
from utils.logger import get_logger

logger = get_logger(__name__)

class TeamService:
    """Team service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_team(self, team_data: TeamCreate) -> Team:
        """Create a new team"""
        team = Team(
            name=team_data.name,
            sport_id=team_data.sport,
            competition=team_data.competition,
            location=team_data.location,
            stadium=team_data.stadium,
            founded=team_data.founded
        )
        
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        
        logger.info(f"Team created: {team.id} - {team.name}")
        return team
    
    def get_team(self, team_id: UUID) -> Optional[Team]:
        """Get team by ID"""
        return self.db.query(Team).filter(
            and_(Team.id == team_id, Team.deleted_at.is_(None))
        ).first()
    
    def list_teams(
        self,
        page: int = 1,
        limit: int = 20,
        sport: Optional[str] = None,
        competition: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: str = "asc"
    ) -> Dict[str, Any]:
        """List teams with filters"""
        query = self.db.query(Team).filter(Team.deleted_at.is_(None))
        
        # Apply filters
        if sport:
            query = query.filter(Team.sport_id == sport)
        if competition:
            query = query.filter(Team.competition == competition)
        if search:
            query = query.filter(Team.name.ilike(f"%{search}%"))
        
        # Apply sorting
        if sort_by:
            if sort_by == "name":
                order_func = desc(Team.name) if order == "desc" else Team.name
                query = query.order_by(order_func)
            elif sort_by == "matches":
                # Sort by number of matches played
                from sqlalchemy import func
                from api.models.match import Match
                match_count = func.count(
                    func.distinct(
                        func.case(
                            (Match.team1_id == Team.id, Match.id),
                            (Match.team2_id == Team.id, Match.id),
                            else_=None
                        )
                    )
                ).label('match_count')
                query = query.outerjoin(
                    Match, 
                    or_(Match.team1_id == Team.id, Match.team2_id == Team.id)
                ).group_by(Team.id)
                if order == "desc":
                    query = query.order_by(desc(match_count))
                else:
                    query = query.order_by(match_count)
            else:
                query = query.order_by(Team.name)
        else:
            query = query.order_by(Team.name)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        teams = query.offset((page - 1) * limit).limit(limit).all()
        
        return {
            "teams": teams,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    def get_team_profile(self, team_id: UUID) -> Optional[Dict[str, Any]]:
        """Get team profile with squad and season stats"""
        team = self.get_team(team_id)
        if not team:
            return None
        
        # Get squad
        squad = self.db.query(TeamPlayer).join(Player).filter(
            and_(
                TeamPlayer.team_id == team_id,
                TeamPlayer.is_active == True
            )
        ).all()
        
        # Get season stats (from matches)
        matches = self.db.query(Match).filter(
            or_(Match.team1_id == team_id, Match.team2_id == team_id)
        ).filter(Match.status == 'completed').all()
        
        wins = sum(1 for m in matches if (
            (m.team1_id == team_id and m.score_team1 and m.score_team2 and m.score_team1 > m.score_team2) or
            (m.team2_id == team_id and m.score_team1 and m.score_team2 and m.score_team2 > m.score_team1)
        ))
        draws = sum(1 for m in matches if (
            m.score_team1 and m.score_team2 and m.score_team1 == m.score_team2
        ))
        losses = len(matches) - wins - draws
        
        return {
            "team": team,
            "squad": squad,
            "season_stats": {
                "matches_played": len(matches),
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "points": wins * 3 + draws
            }
        }
    
    def update_team(self, team_id: UUID, team_data: TeamUpdate) -> Optional[Team]:
        """Update team"""
        team = self.get_team(team_id)
        if not team:
            return None
        
        if team_data.name is not None:
            team.name = team_data.name
        if team_data.competition is not None:
            team.competition = team_data.competition
        if team_data.location is not None:
            team.location = team_data.location
        if team_data.stadium is not None:
            team.stadium = team_data.stadium
        if team_data.logo_url is not None:
            team.logo_url = team_data.logo_url
        
        self.db.commit()
        self.db.refresh(team)
        
        logger.info(f"Team updated: {team.id}")
        return team

