"""
Team Assigner Module
Assigns players to teams based on jersey color clustering
Uses modular color extraction and clustering components
"""

import cv2
import numpy as np

# Handle imports
try:
    from ..utils.color_clustering import ColorExtractor, TeamColorClusterer
except ImportError:
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.color_clustering import ColorExtractor, TeamColorClusterer


class TeamAssigner:
    """
    Assigns players to teams using jersey color clustering
    Uses modular components for maintainability
    """
    
    def __init__(self, use_lab=True):
        """
        Initialize team assigner
        
        Args:
            use_lab: Use LAB color space instead of RGB for better clustering
        """
        self.use_lab = use_lab
        self.player_team_dict = {}
        
        # Initialize modular components
        self.color_extractor = ColorExtractor(use_lab=use_lab)
        self.color_clusterer = TeamColorClusterer(use_lab=use_lab)
    
    def assign_team_color(self, frame, player_detections):
        """
        Assign team colors based on player jersey colors
        
        Args:
            frame: Video frame
            player_detections: Dictionary of player detections for first frame
        """
        player_colors = []
        
        for track_id, player_info in player_detections.items():
            bbox = player_info['bbox']
            
            # Extract player jersey color using modular extractor
            player_color = self.color_extractor.extract_jersey_color(frame, bbox)
            
            if player_color is not None:
                player_colors.append(player_color)
        
        # Fit teams using modular clusterer
        success = self.color_clusterer.fit_teams(player_colors)
        
        if not success:
            print("⚠️  Not enough players for color clustering, using default team colors")
        else:
            print(f"✓ Team colors assigned: Team 1={self.color_clusterer.team_colors[1]}, "
                  f"Team 2={self.color_clusterer.team_colors[2]}")
    
    def get_player_team(self, frame, bbox, player_id):
        """
        Get team assignment for a player
        
        Args:
            frame: Video frame
            bbox: Player bounding box
            player_id: Player track ID
            
        Returns:
            Team number (1 or 2)
        """
        # Check if already assigned
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
        
        # Get player color using modular extractor
        player_color = self.color_extractor.extract_jersey_color(frame, bbox)
        
        if player_color is None:
            return 1  # Default to team 1
        
        # Predict team using modular clusterer
        team = self.color_clusterer.predict_team(player_color)
        
        if team is None:
            return 1  # Default to team 1
        
        # Cache the assignment
        self.player_team_dict[player_id] = team
        
        return team
    
    def get_team_colors(self):
        """Get assigned team colors"""
        return self.color_clusterer.team_colors.copy()
