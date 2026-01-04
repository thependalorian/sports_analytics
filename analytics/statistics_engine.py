"""
Statistics Engine Module
Main orchestrator for statistics calculation, export, and reporting
Uses modular components for maintainability
"""

import pandas as pd
import numpy as np
import os

# Handle imports - try relative first, then absolute
try:
    from ..utils.statistics_calculator import StatisticsCalculator
    from ..utils.statistics_exporter import StatisticsExporter
    from ..utils.report_generator import StatisticsReportGenerator
except ImportError:
    # Fallback to absolute imports if relative fails
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.statistics_calculator import StatisticsCalculator
    from utils.statistics_exporter import StatisticsExporter
    from utils.report_generator import StatisticsReportGenerator


class StatisticsEngine:
    """
    Main statistics engine that orchestrates calculation, export, and reporting
    Uses modular components for maintainability
    """

    def __init__(self):
        """Initialize statistics engine"""
        self.player_stats = {}
        self.team_stats = {}
        
        # Initialize modular components
        self.calculator = StatisticsCalculator()
        self.exporter = StatisticsExporter()
        self.report_generator = StatisticsReportGenerator()
    
    def calculate_all_statistics(self, tracking_df, passes_df=None, events_df=None, fps=30):
        """
        Calculate all statistics from tracking data

        Args:
            tracking_df: DataFrame with tracking data
            passes_df: DataFrame with pass data (optional)
            events_df: DataFrame with event data (optional)
            fps: Frames per second
        """
        # Ensure we have DataFrames
        if not isinstance(tracking_df, pd.DataFrame):
            tracking_df = pd.DataFrame(tracking_df)
        
        if passes_df is None:
            passes_df = pd.DataFrame()
        elif not isinstance(passes_df, pd.DataFrame):
            passes_df = pd.DataFrame(passes_df)
        
        if events_df is None:
            events_df = pd.DataFrame()
        elif not isinstance(events_df, pd.DataFrame):
            events_df = pd.DataFrame(events_df)
        
        # Calculate statistics using modular calculator
        stats = self.calculator.calculate_all(tracking_df, passes_df, events_df, fps)
        
        self.player_stats = stats['players']
        self.team_stats = stats['teams']

    def export_statistics_csv(self, output_dir):
        """
        Export statistics to CSV files

        Args:
            output_dir: Directory to save CSV files
        """
        self.exporter.csv_exporter.export_all_stats(
            self.player_stats,
            self.team_stats,
            output_dir
        )
    
    def export_statistics_json(self, output_path):
        """
        Export statistics to JSON file
        
        Args:
            output_path: Path to JSON output file
        """
        self.exporter.json_exporter.export_statistics(
            self.player_stats,
            self.team_stats,
            output_path
        )

    def generate_statistics_report(self, output_path):
        """
        Generate a human-readable statistics report

        Args:
            output_path: Path to text report file
        """
        self.report_generator.generate_report(
            self.player_stats,
            self.team_stats,
            output_path
        )
    
    def get_player_stats(self, track_id=None):
        """
        Get player statistics
        
        Args:
            track_id: Specific player track ID, or None for all
            
        Returns:
            Dictionary of player statistics
        """
        if track_id is None:
            return self.player_stats.copy()
        return self.player_stats.get(track_id, {})
    
    def get_team_stats(self, team=None):
        """
        Get team statistics
        
        Args:
            team: Team number (1 or 2), or None for all
            
        Returns:
            Dictionary of team statistics
        """
        if team is None:
            return self.team_stats.copy()
        return self.team_stats.get(team, {})
