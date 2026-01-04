"""
Statistics Exporter Module
Handles export of statistics to various formats (CSV, JSON)
"""

import pandas as pd
import json
import os


class CSVExporter:
    """Exports statistics to CSV format"""
    
    @staticmethod
    def export_player_stats(player_stats, output_path):
        """
        Export player statistics to CSV
        
        Args:
            player_stats: Dictionary of player statistics
            output_path: Output file path
        """
        if not player_stats:
            return
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        player_df = pd.DataFrame(list(player_stats.values()))
        player_df.to_csv(output_path, index=False)
        print(f"✓ Player statistics exported: {output_path}")
    
    @staticmethod
    def export_team_stats(team_stats, output_path):
        """
        Export team statistics to CSV
        
        Args:
            team_stats: Dictionary of team statistics
            output_path: Output file path
        """
        if not team_stats:
            return
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        team_df = pd.DataFrame(list(team_stats.values()))
        team_df.to_csv(output_path, index=False)
        print(f"✓ Team statistics exported: {output_path}")
    
    @staticmethod
    def export_all_stats(player_stats, team_stats, output_dir):
        """
        Export all statistics to CSV files
        
        Args:
            player_stats: Dictionary of player statistics
            team_stats: Dictionary of team statistics
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        CSVExporter.export_player_stats(
            player_stats,
            os.path.join(output_dir, 'player_statistics.csv')
        )
        
        CSVExporter.export_team_stats(
            team_stats,
            os.path.join(output_dir, 'team_statistics.csv')
        )


class JSONExporter:
    """Exports statistics to JSON format"""
    
    @staticmethod
    def export_statistics(player_stats, team_stats, output_path):
        """
        Export statistics to JSON
        
        Args:
            player_stats: Dictionary of player statistics
            team_stats: Dictionary of team statistics
            output_path: Output file path
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        data = {
            'players': player_stats,
            'teams': team_stats
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✓ Statistics exported to JSON: {output_path}")


class StatisticsExporter:
    """Main exporter that combines CSV and JSON export"""
    
    def __init__(self):
        """Initialize exporter"""
        self.csv_exporter = CSVExporter()
        self.json_exporter = JSONExporter()
    
    def export_all(self, player_stats, team_stats, output_dir):
        """
        Export statistics in all formats
        
        Args:
            player_stats: Dictionary of player statistics
            team_stats: Dictionary of team statistics
            output_dir: Output directory
        """
        # Export CSV
        self.csv_exporter.export_all_stats(player_stats, team_stats, output_dir)
        
        # Export JSON
        self.json_exporter.export_statistics(
            player_stats,
            team_stats,
            os.path.join(output_dir, 'statistics.json')
        )

