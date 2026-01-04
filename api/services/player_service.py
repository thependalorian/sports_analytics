"""
Player Service
Location: /api/services/player_service.py
Purpose: Business logic for player operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import date

from api.models.player import Player, PlayerStatistics
from api.models.match import Match
from api.schemas.player import PlayerCreate, PlayerUpdate
from utils.logger import get_logger

logger = get_logger(__name__)

class PlayerService:
    """Player service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_player(self, player_data: PlayerCreate) -> Player:
        """Create a new player"""
        player = Player(
            name=player_data.name,
            sport_id=player_data.sport,
            jersey_number=player_data.jersey_number,
            date_of_birth=player_data.date_of_birth,
            nationality=player_data.nationality,
            height_cm=player_data.height_cm,
            weight_kg=player_data.weight_kg,
            position=player_data.position,
            metadata=player_data.metadata
        )
        
        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)
        
        logger.info(f"Player created: {player.id} - {player.name}")
        return player
    
    def get_player(self, player_id: UUID) -> Optional[Player]:
        """Get player by ID"""
        return self.db.query(Player).filter(
            and_(Player.id == player_id, Player.deleted_at.is_(None))
        ).first()
    
    def list_players(
        self,
        page: int = 1,
        limit: int = 20,
        sport: Optional[str] = None,
        team: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        order: str = "asc"
    ) -> Dict[str, Any]:
        """List players with filters"""
        query = self.db.query(Player).filter(Player.deleted_at.is_(None))
        
        # Apply filters
        if sport:
            query = query.filter(Player.sport_id == sport)
        if search:
            query = query.filter(
                or_(
                    Player.name.ilike(f"%{search}%"),
                    Player.position.ilike(f"%{search}%")
                )
            )
        
        # Apply sorting
        if sort_by:
            if sort_by == "name":
                order_func = desc(Player.name) if order == "desc" else Player.name
                query = query.order_by(order_func)
            elif sort_by == "matches":
                # Sort by number of matches played
                from sqlalchemy import func
                match_count = func.count(PlayerStatistics.id).label('match_count')
                query = query.outerjoin(PlayerStatistics).group_by(Player.id)
                if order == "desc":
                    query = query.order_by(desc(match_count))
                else:
                    query = query.order_by(match_count)
            else:
                query = query.order_by(Player.name)
        else:
            query = query.order_by(Player.name)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        players = query.offset((page - 1) * limit).limit(limit).all()
        
        return {
            "players": players,
            "total": total,
            "page": page,
            "limit": limit
        }
    
    def get_player_profile(self, player_id: UUID) -> Optional[Dict[str, Any]]:
        """Get player profile with career stats"""
        player = self.get_player(player_id)
        if not player:
            return None
        
        # Get matches
        matches = self.db.query(Match).join(PlayerStatistics).filter(
            PlayerStatistics.player_id == player_id
        ).distinct().all()
        
        # Calculate career stats
        stats = self.db.query(
            func.count(PlayerStatistics.id).label('matches_played'),
            func.sum(PlayerStatistics.total_distance_m).label('total_distance'),
            func.avg(PlayerStatistics.total_distance_m).label('avg_distance'),
            func.sum(PlayerStatistics.passes_made).label('total_passes'),
            func.avg(PlayerStatistics.pass_accuracy_pct).label('avg_pass_accuracy')
        ).filter(PlayerStatistics.player_id == player_id).first()
        
        return {
            "player": player,
            "matches": matches,
            "career_stats": {
                "matches_played": stats.matches_played or 0,
                "total_distance_km": round((stats.total_distance or 0) / 1000, 1),
                "avg_distance_per_match_km": round((stats.avg_distance or 0) / 1000, 1),
                "total_passes": stats.total_passes or 0,
                "pass_accuracy_pct": round(stats.avg_pass_accuracy or 0, 1)
            }
        }
    
    def update_player(self, player_id: UUID, player_data: PlayerUpdate) -> Optional[Player]:
        """Update player"""
        player = self.get_player(player_id)
        if not player:
            return None
        
        if player_data.name is not None:
            player.name = player_data.name
        if player_data.jersey_number is not None:
            player.jersey_number = player_data.jersey_number
        if player_data.position is not None:
            player.position = player_data.position
        if player_data.metadata is not None:
            player.metadata = player_data.metadata
        
        self.db.commit()
        self.db.refresh(player)
        
        logger.info(f"Player updated: {player.id}")
        return player

