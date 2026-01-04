"""
Statistics Calculator Module
Handles calculation of player and team statistics
"""

import numpy as np
import pandas as pd
from collections import defaultdict


class PlayerStatisticsCalculator:
    """Calculates individual player statistics"""
    
    @staticmethod
    def calculate_player_stats(tracking_df, passes_df, fps=30):
        """
        Calculate statistics for all players
        
        Args:
            tracking_df: DataFrame with tracking data
            passes_df: DataFrame with pass data
            fps: Frames per second
            
        Returns:
            Dictionary of player statistics
        """
        player_stats = {}
        
        if tracking_df.empty:
            return player_stats
        
        for track_id in tracking_df['track_id'].unique():
            player_data = tracking_df[tracking_df['track_id'] == track_id]
            
            # Basic info
            team = player_data['team'].mode().iloc[0] if not player_data['team'].mode().empty else 0
            
            # Distance and speed
            total_distance_m = 0
            avg_speed_kmh = 0
            max_speed_kmh = 0
            
            if 'distance_meters' in player_data.columns:
                total_distance_m = player_data['distance_meters'].max()
            
            if 'speed_kmh' in player_data.columns:
                avg_speed_kmh = player_data['speed_kmh'].mean()
                max_speed_kmh = player_data['speed_kmh'].max()
            
            # Ball possession
            time_with_ball_frames = 0
            if 'has_ball' in player_data.columns:
                time_with_ball_frames = player_data['has_ball'].sum()
            
            player_stats[track_id] = {
                'track_id': track_id,
                'team': team,
                'total_frames': len(player_data),
                'total_distance_m': total_distance_m,
                'avg_speed_kmh': avg_speed_kmh,
                'max_speed_kmh': max_speed_kmh,
                'time_with_ball_frames': time_with_ball_frames,
                'time_with_ball_sec': time_with_ball_frames / fps if fps > 0 else 0
            }
        
        return player_stats


class TeamStatisticsCalculator:
    """Calculates team-level statistics"""
    
    @staticmethod
    def calculate_team_stats(player_stats):
        """
        Calculate statistics for teams
        
        Args:
            player_stats: Dictionary of player statistics
            
        Returns:
            Dictionary of team statistics
        """
        team_stats = {}
        
        for team in [1, 2]:
            team_players = [p for p in player_stats.values() if p['team'] == team]
            
            if not team_players:
                team_stats[team] = {
                    'team': team,
                    'num_players': 0,
                    'total_distance_m': 0,
                    'avg_speed_kmh': 0,
                    'total_time_with_ball_sec': 0
                }
                continue
            
            total_distance_m = sum(p['total_distance_m'] for p in team_players)
            avg_speed_kmh = np.mean([p['avg_speed_kmh'] for p in team_players])
            total_time_with_ball_sec = sum(p['time_with_ball_sec'] for p in team_players)
            
            team_stats[team] = {
                'team': team,
                'num_players': len(team_players),
                'total_distance_m': total_distance_m,
                'avg_speed_kmh': avg_speed_kmh,
                'total_time_with_ball_sec': total_time_with_ball_sec
            }
        
        return team_stats


class StatisticsCalculator:
    """Main statistics calculator that combines player and team calculations"""
    
    def __init__(self):
        """Initialize calculator"""
        self.player_calculator = PlayerStatisticsCalculator()
        self.team_calculator = TeamStatisticsCalculator()
    
    def calculate_all(self, tracking_df, passes_df=None, events_df=None, fps=30):
        """
        Calculate all statistics
        
        Args:
            tracking_df: DataFrame with tracking data
            passes_df: DataFrame with pass data (optional)
            events_df: DataFrame with event data (optional)
            fps: Frames per second
            
        Returns:
            Dictionary with 'players' and 'teams' statistics
        """
        # Calculate player statistics
        player_stats = self.player_calculator.calculate_player_stats(
            tracking_df, passes_df if passes_df is not None else pd.DataFrame(), fps
        )
        
        # Calculate team statistics
        team_stats = self.team_calculator.calculate_team_stats(player_stats)
        
        return {
            'players': player_stats,
            'teams': team_stats
        }

