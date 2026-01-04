"""
Analytics Service with DuckDB Integration
Location: /api/services/analytics_service.py
Purpose: Advanced analytics using DuckDB SQL queries on LanceDB data
Date: 2026-01-04
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from api.lib.lancedb_adapter import get_lancedb
from api.models.match import Match
from api.models.player import PlayerStatistics
from api.models.team import Team
from utils.logger import get_logger

logger = get_logger(__name__)

class AnalyticsService:
    """Analytics service using DuckDB for complex SQL queries"""
    
    def __init__(self, db: Session):
        self.db = db
        self.lancedb = get_lancedb()
    
    def get_match_analytics(self, match_id: UUID) -> Dict[str, Any]:
        """
        Get comprehensive analytics for a match using DuckDB
        
        Args:
            match_id: Match UUID
            
        Returns:
            Dictionary with match analytics
        """
        # Register matches table
        self.lancedb.register_lancedb_table("matches", "matches_view")
        
        # Execute complex SQL query
        query = f"""
        SELECT 
            COUNT(*) as total_events,
            AVG(total_distance_m) as avg_distance,
            MAX(max_speed_kmh) as max_speed,
            SUM(passes_made) as total_passes,
            AVG(pass_accuracy_pct) as avg_pass_accuracy
        FROM matches_view
        WHERE id = '{match_id}'
        """
        
        result = self.lancedb.execute_sql(query)
        
        return {
            "match_id": str(match_id),
            "analytics": result.to_dict('records')[0] if not result.empty else {},
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_player_performance_trends(
        self,
        player_id: UUID,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get player performance trends over time using DuckDB
        
        Args:
            player_id: Player UUID
            days: Number of days to analyze
            
        Returns:
            Dictionary with performance trends
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Register tables
        self.lancedb.register_lancedb_table("matches", "matches_view")
        self.lancedb.register_lancedb_table("player_statistics", "player_stats_view")
        
        query = f"""
        SELECT 
            DATE(m.date) as match_date,
            COUNT(*) as matches_played,
            AVG(ps.total_distance_m) as avg_distance,
            AVG(ps.avg_speed_kmh) as avg_speed,
            AVG(ps.passes_made) as avg_passes,
            AVG(ps.pass_accuracy_pct) as avg_pass_accuracy
        FROM player_stats_view ps
        JOIN matches_view m ON ps.match_id = m.id
        WHERE ps.player_id = '{player_id}'
          AND m.date >= '{start_date.isoformat()}'
          AND m.deleted_at IS NULL
        GROUP BY DATE(m.date)
        ORDER BY match_date DESC
        """
        
        result = self.lancedb.execute_sql(query)
        
        return {
            "player_id": str(player_id),
            "period_days": days,
            "trends": result.to_dict('records'),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_team_comparison(
        self,
        team1_id: UUID,
        team2_id: UUID,
        days: int = 90
    ) -> Dict[str, Any]:
        """
        Compare two teams using DuckDB analytics
        
        Args:
            team1_id: First team UUID
            team2_id: Second team UUID
            days: Number of days to analyze
            
        Returns:
            Dictionary with team comparison
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Register tables
        self.lancedb.register_lancedb_table("matches", "matches_view")
        self.lancedb.register_lancedb_table("player_statistics", "player_stats_view")
        
        query = f"""
        WITH team1_stats AS (
            SELECT 
                AVG(ps.total_distance_m) as avg_distance,
                AVG(ps.avg_speed_kmh) as avg_speed,
                AVG(ps.passes_made) as avg_passes,
                AVG(ps.pass_accuracy_pct) as avg_pass_accuracy,
                COUNT(DISTINCT m.id) as matches_played
            FROM player_stats_view ps
            JOIN matches_view m ON ps.match_id = m.id
            WHERE (m.team1_id = '{team1_id}' OR m.team2_id = '{team1_id}')
              AND m.date >= '{start_date.isoformat()}'
              AND m.deleted_at IS NULL
        ),
        team2_stats AS (
            SELECT 
                AVG(ps.total_distance_m) as avg_distance,
                AVG(ps.avg_speed_kmh) as avg_speed,
                AVG(ps.passes_made) as avg_passes,
                AVG(ps.pass_accuracy_pct) as avg_pass_accuracy,
                COUNT(DISTINCT m.id) as matches_played
            FROM player_stats_view ps
            JOIN matches_view m ON ps.match_id = m.id
            WHERE (m.team1_id = '{team2_id}' OR m.team2_id = '{team2_id}')
              AND m.date >= '{start_date.isoformat()}'
              AND m.deleted_at IS NULL
        )
        SELECT 
            t1.avg_distance as team1_avg_distance,
            t2.avg_distance as team2_avg_distance,
            t1.avg_speed as team1_avg_speed,
            t2.avg_speed as team2_avg_speed,
            t1.avg_passes as team1_avg_passes,
            t2.avg_passes as team2_avg_passes,
            t1.avg_pass_accuracy as team1_pass_accuracy,
            t2.avg_pass_accuracy as team2_pass_accuracy,
            t1.matches_played as team1_matches,
            t2.matches_played as team2_matches
        FROM team1_stats t1, team2_stats t2
        """
        
        result = self.lancedb.execute_sql(query)
        
        return {
            "team1_id": str(team1_id),
            "team2_id": str(team2_id),
            "period_days": days,
            "comparison": result.to_dict('records')[0] if not result.empty else {},
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_sport_statistics(self, sport_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a sport using DuckDB
        
        Args:
            sport_id: Sport identifier (e.g., 'football', 'basketball')
            
        Returns:
            Dictionary with sport statistics
        """
        # Register tables
        self.lancedb.register_lancedb_table("matches", "matches_view")
        self.lancedb.register_lancedb_table("players", "players_view")
        self.lancedb.register_lancedb_table("teams", "teams_view")
        
        query = f"""
        SELECT 
            (SELECT COUNT(*) FROM matches_view WHERE sport_id = '{sport_id}' AND deleted_at IS NULL) as total_matches,
            (SELECT COUNT(*) FROM players_view WHERE sport_id = '{sport_id}' AND deleted_at IS NULL) as total_players,
            (SELECT COUNT(*) FROM teams_view WHERE sport_id = '{sport_id}' AND deleted_at IS NULL) as total_teams,
            (SELECT AVG(score_team1 + score_team2) 
             FROM matches_view 
             WHERE sport_id = '{sport_id}' 
               AND status = 'completed' 
               AND deleted_at IS NULL) as avg_total_score
        """
        
        result = self.lancedb.execute_sql(query)
        
        return {
            "sport_id": sport_id,
            "statistics": result.to_dict('records')[0] if not result.empty else {},
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_top_performers(
        self,
        sport_id: str,
        metric: str = "total_distance_m",
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get top performing players by metric using DuckDB
        
        Args:
            sport_id: Sport identifier
            metric: Metric to rank by (e.g., 'total_distance_m', 'passes_made')
            limit: Number of top performers to return
            
        Returns:
            Dictionary with top performers
        """
        # Register tables
        self.lancedb.register_lancedb_table("player_statistics", "player_stats_view")
        self.lancedb.register_lancedb_table("players", "players_view")
        self.lancedb.register_lancedb_table("matches", "matches_view")
        
        query = f"""
        SELECT 
            p.id,
            p.name,
            p.position,
            AVG(ps.{metric}) as avg_{metric},
            COUNT(DISTINCT ps.match_id) as matches_played
        FROM player_stats_view ps
        JOIN players_view p ON ps.player_id = p.id
        JOIN matches_view m ON ps.match_id = m.id
        WHERE p.sport_id = '{sport_id}'
          AND m.deleted_at IS NULL
          AND p.deleted_at IS NULL
        GROUP BY p.id, p.name, p.position
        ORDER BY avg_{metric} DESC
        LIMIT {limit}
        """
        
        result = self.lancedb.execute_sql(query)
        
        return {
            "sport_id": sport_id,
            "metric": metric,
            "top_performers": result.to_dict('records'),
            "generated_at": datetime.utcnow().isoformat()
        }

