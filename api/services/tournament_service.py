"""
Tournament Service
Location: /api/services/tournament_service.py
Purpose: Business logic for tournament operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import date
from decimal import Decimal

from api.models.tournament import Tournament, TournamentParticipant
from api.models.team import Team
from api.models.match import Match
from api.schemas.tournament import TournamentCreate, TournamentUpdate
from utils.logger import get_logger

logger = get_logger(__name__)

class TournamentService:
    """Tournament service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_tournament(self, tournament_data: TournamentCreate) -> Tournament:
        """Create a new tournament"""
        tournament = Tournament(
            name=tournament_data.name,
            sport_id=tournament_data.sport,
            organizer=tournament_data.organizer,
            format=tournament_data.format,
            teams_count=tournament_data.teams_count,
            prize_money=tournament_data.prize_money,
            currency=tournament_data.currency,
            start_date=tournament_data.start_date,
            end_date=tournament_data.end_date,
            venue=tournament_data.venue
        )
        
        self.db.add(tournament)
        self.db.commit()
        self.db.refresh(tournament)
        
        logger.info(f"Tournament created: {tournament.id} - {tournament.name}")
        return tournament
    
    def get_tournament(self, tournament_id: UUID) -> Optional[Tournament]:
        """Get tournament by ID"""
        return self.db.query(Tournament).filter(
            Tournament.id == tournament_id
        ).first()
    
    def list_tournaments(
        self,
        page: int = 1,
        limit: int = 20,
        sport: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """List tournaments with filters"""
        query = self.db.query(Tournament)
        
        # Apply filters
        if sport:
            query = query.filter(Tournament.sport_id == sport)
        if status:
            query = query.filter(Tournament.status == status)
        if search:
            query = query.filter(Tournament.name.ilike(f"%{search}%"))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        tournaments = query.order_by(desc(Tournament.start_date)).offset((page - 1) * limit).limit(limit).all()
        
        return {
            "tournaments": tournaments,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    def get_tournament_standings(self, tournament_id: UUID) -> Optional[Dict[str, Any]]:
        """Get tournament standings"""
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            return None
        
        # Get participants
        participants = self.db.query(TournamentParticipant).filter(
            TournamentParticipant.tournament_id == tournament_id
        ).all()
        
        # Calculate standings for each team
        standings = []
        for participant in participants:
            # Get matches for this team in tournament
            matches = self.db.query(Match).filter(
                and_(
                    or_(Match.team1_id == participant.team_id, Match.team2_id == participant.team_id),
                    Match.competition == tournament.name,
                    Match.status == 'completed'
                )
            ).all()
            
            wins = sum(1 for m in matches if (
                (m.team1_id == participant.team_id and m.score_team1 and m.score_team2 and m.score_team1 > m.score_team2) or
                (m.team2_id == participant.team_id and m.score_team1 and m.score_team2 and m.score_team2 > m.score_team1)
            ))
            draws = sum(1 for m in matches if (
                m.score_team1 and m.score_team2 and m.score_team1 == m.score_team2
            ))
            losses = len(matches) - wins - draws
            
            standings.append({
                "team_id": str(participant.team_id),
                "team_name": participant.team.name if participant.team else None,
                "matches_played": len(matches),
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "points": wins * 3 + draws,
                "goal_difference": 0,  # TODO: Calculate from match scores
                "goals_for": 0,  # TODO: Calculate from match scores
                "goals_against": 0,  # TODO: Calculate from match scores
                "position": 0  # Will be calculated after sorting
            })
        
        # Sort by points (descending), then goal difference, then goals for
        standings.sort(key=lambda x: (x['points'], x.get('goal_difference', 0), x.get('goals_for', 0)), reverse=True)
        
        # Assign positions
        for i, standing in enumerate(standings, 1):
            standing['position'] = i
        
        return {
            "tournament_id": str(tournament_id),
            "standings": standings
        }
    
    def update_tournament(self, tournament_id: UUID, tournament_data: TournamentUpdate) -> Optional[Tournament]:
        """Update tournament"""
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            return None
        
        if tournament_data.name is not None:
            tournament.name = tournament_data.name
        if tournament_data.status is not None:
            tournament.status = tournament_data.status
        if tournament_data.bracket is not None:
            tournament.bracket = tournament_data.bracket
        
        self.db.commit()
        self.db.refresh(tournament)
        
        logger.info(f"Tournament updated: {tournament.id}")
        return tournament

