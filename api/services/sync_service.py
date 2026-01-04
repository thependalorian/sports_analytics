"""
Sync Service (Offline-First)
Location: /api/services/sync_service.py
Purpose: Business logic for offline sync operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

from api.models.sync import SyncQueue, SyncHistory
from api.models.match import Match
from api.models.player import Player
from api.models.team import Team
from api.schemas.sync import SyncRequest, SyncUploadRequest, SyncUploadItem
from utils.logger import get_logger

logger = get_logger(__name__)

class SyncService:
    """Sync service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def sync_matches(self, sync_request: SyncRequest, user_id: UUID) -> Dict[str, Any]:
        """Sync matches (delta updates)"""
        # Get matches updated since last_sync
        matches = self.db.query(Match).filter(
            and_(
                Match.updated_at > sync_request.last_sync,
                Match.deleted_at.is_(None)
            )
        ).all()
        
        # Get deleted matches (soft deletes)
        deleted = self.db.query(Match.id).filter(
            and_(
                Match.deleted_at > sync_request.last_sync,
                Match.deleted_at.isnot(None)
            )
        ).all()
        
        return {
            "matches": [
                {
                    "id": str(match.id),
                    "updated_at": match.updated_at.isoformat(),
                    "data": {
                        "name": match.name,
                        "status": match.status,
                        "sport": match.sport_id,
                        "date": match.date.isoformat()
                    }
                }
                for match in matches
            ],
            "deleted": [str(d[0]) for d in deleted],
            "sync_timestamp": datetime.utcnow().isoformat()
        }
    
    def sync_players(self, sync_request: SyncRequest, user_id: UUID) -> Dict[str, Any]:
        """Sync players (delta updates)"""
        # Get players updated since last_sync
        players = self.db.query(Player).filter(
            and_(
                Player.updated_at > sync_request.last_sync,
                Player.deleted_at.is_(None)
            )
        ).all()
        
        return {
            "players": [
                {
                    "id": str(player.id),
                    "updated_at": player.updated_at.isoformat(),
                    "data": {
                        "name": player.name,
                        "sport": player.sport_id,
                        "position": player.position
                    }
                }
                for player in players
            ],
            "sync_timestamp": datetime.utcnow().isoformat()
        }
    
    def upload_offline_data(self, upload_request: SyncUploadRequest, user_id: UUID) -> Dict[str, Any]:
        """Upload offline data with conflict resolution"""
        synced = 0
        failed = 0
        conflicts = []
        
        for item in upload_request.data:
            try:
                conflict = None
                
                # Check for conflicts (server has newer version)
                if item.action in ['create', 'update']:
                    conflict = self._detect_conflict(item, user_id)
                    if conflict:
                        conflicts.append(conflict)
                        # Resolve conflict: server wins by default
                        if conflict.get('resolution') == 'server_wins':
                            continue  # Skip this item
                
                # Process based on type
                if item.type == 'match':
                    self._process_match_sync(item, user_id)
                elif item.type == 'player':
                    self._process_player_sync(item, user_id)
                elif item.type == 'team':
                    self._process_team_sync(item, user_id)
                
                synced += 1
            except Exception as e:
                logger.error(f"Sync item failed: {e}")
                failed += 1
        
        # Record sync history
        sync_history = SyncHistory(
            user_id=user_id,
            device_id=upload_request.device_id,
            last_sync_at=datetime.utcnow(),
            entities_synced=synced,
            conflicts_resolved=len(conflicts),
            errors=failed
        )
        self.db.add(sync_history)
        self.db.commit()
        
        return {
            "synced": synced,
            "failed": failed,
            "conflicts": conflicts,
            "sync_timestamp": datetime.utcnow().isoformat()
        }
    
    def _detect_conflict(self, item: SyncUploadItem, user_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Detect conflicts between client and server data
        
        Returns:
            Conflict dictionary if conflict exists, None otherwise
        """
        from api.models.match import Match
        from api.models.player import Player
        from api.models.team import Team
        
        if item.type == 'match' and item.action == 'update':
            # Check if server has newer version
            match = self.db.query(Match).filter(Match.id == item.data.get('id')).first()
            if match:
                client_timestamp = item.timestamp
                server_timestamp = match.updated_at
                
                if server_timestamp > client_timestamp:
                    return {
                        "type": item.type,
                        "entity_id": str(item.data.get('id')),
                        "client_timestamp": client_timestamp.isoformat(),
                        "server_timestamp": server_timestamp.isoformat(),
                        "resolution": "server_wins"  # Server wins by default
                    }
        
        return None
    
    def _process_match_sync(self, item: SyncUploadItem, user_id: UUID):
        """Process match sync item"""
        from api.models.match import Match
        from uuid import UUID as UUIDType
        
        if item.action == 'create':
            match_date = item.data.get('date')
            if isinstance(match_date, str):
                match_date = match_date.replace('Z', '+00:00') if 'Z' in match_date else match_date
                match_date = datetime.fromisoformat(match_date)
            
            match = Match(
                name=item.data.get('name'),
                sport_id=item.data.get('sport', 'football'),
                date=match_date,
                team1_name=item.data.get('team1_name'),
                team2_name=item.data.get('team2_name'),
                created_by=user_id,
                status='uploaded'
            )
            self.db.add(match)
        elif item.action == 'update':
            match_id = UUIDType(item.data.get('id'))
            match = self.db.query(Match).filter(Match.id == match_id).first()
            if match:
                if 'name' in item.data:
                    match.name = item.data['name']
                if 'date' in item.data:
                    match_date = item.data['date']
                    if isinstance(match_date, str):
                        match_date = match_date.replace('Z', '+00:00') if 'Z' in match_date else match_date
                        match.date = datetime.fromisoformat(match_date)
                if 'status' in item.data:
                    match.status = item.data['status']
                if 'score_team1' in item.data:
                    match.score_team1 = item.data['score_team1']
                if 'score_team2' in item.data:
                    match.score_team2 = item.data['score_team2']
        elif item.action == 'delete':
            match_id = UUIDType(item.data.get('id'))
            match = self.db.query(Match).filter(Match.id == match_id).first()
            if match:
                match.deleted_at = datetime.utcnow()
        
        self.db.commit()
    
    def _process_player_sync(self, item: SyncUploadItem, user_id: UUID):
        """Process player sync item"""
        from api.models.player import Player
        from uuid import UUID as UUIDType
        
        if item.action == 'create':
            player = Player(
                name=item.data.get('name'),
                sport_id=item.data.get('sport', 'football'),
                jersey_number=item.data.get('jersey_number'),
                position=item.data.get('position'),
                nationality=item.data.get('nationality', 'Namibian')
            )
            self.db.add(player)
        elif item.action == 'update':
            player_id = UUIDType(item.data.get('id'))
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if player:
                if 'name' in item.data:
                    player.name = item.data['name']
                if 'position' in item.data:
                    player.position = item.data['position']
                if 'jersey_number' in item.data:
                    player.jersey_number = item.data['jersey_number']
        elif item.action == 'delete':
            player_id = UUIDType(item.data.get('id'))
            player = self.db.query(Player).filter(Player.id == player_id).first()
            if player:
                player.deleted_at = datetime.utcnow()
        
        self.db.commit()
    
    def _process_team_sync(self, item: SyncUploadItem, user_id: UUID):
        """Process team sync item"""
        from api.models.team import Team
        from uuid import UUID as UUIDType
        
        if item.action == 'create':
            team = Team(
                name=item.data.get('name'),
                sport_id=item.data.get('sport', 'football'),
                competition=item.data.get('competition'),
                location=item.data.get('location')
            )
            self.db.add(team)
        elif item.action == 'update':
            team_id = UUIDType(item.data.get('id'))
            team = self.db.query(Team).filter(Team.id == team_id).first()
            if team:
                if 'name' in item.data:
                    team.name = item.data['name']
                if 'competition' in item.data:
                    team.competition = item.data['competition']
                if 'location' in item.data:
                    team.location = item.data['location']
        elif item.action == 'delete':
            team_id = UUIDType(item.data.get('id'))
            team = self.db.query(Team).filter(Team.id == team_id).first()
            if team:
                team.deleted_at = datetime.utcnow()
        
        self.db.commit()

