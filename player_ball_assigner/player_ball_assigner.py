"""
Player Ball Assigner Module
Determines which player has possession of the ball
Uses modular distance calculation utilities
"""

import numpy as np

# Handle imports
try:
    from ..utils.position_utils import PositionCalculator
except ImportError:
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.position_utils import PositionCalculator


class PlayerBallAssigner:
    """
    Assigns ball possession to players based on proximity
    Uses modular position utilities
    """
    
    def __init__(self, max_distance=70):
        """
        Initialize player ball assigner
        
        Args:
            max_distance: Maximum distance (pixels) to assign ball to player
        """
        self.max_distance = max_distance
        self.position_calculator = PositionCalculator()
    
    def assign_ball_to_player(self, players, ball_bbox):
        """
        Assign ball to the closest player
        
        Args:
            players: Dictionary of player detections {track_id: player_info}
            ball_bbox: Ball bounding box [x1, y1, x2, y2]
            
        Returns:
            Player track ID with ball possession, or -1 if no player
        """
        if not ball_bbox or len(ball_bbox) < 4:
            return -1
        
        # Get ball position (center of bbox)
        ball_position = self.position_calculator.get_bbox_center(ball_bbox)
        
        min_distance = float('inf')
        assigned_player = -1
        
        for player_id, player_info in players.items():
            player_bbox = player_info.get('bbox', [])
            
            if not player_bbox or len(player_bbox) < 4:
                continue
            
            # Get distance from player's foot position to ball
            player_foot = self.position_calculator.get_foot_position(player_bbox)
            
            distance = self.position_calculator.calculate_distance(player_foot, ball_position)
            
            if distance < min_distance:
                min_distance = distance
                assigned_player = player_id
        
        # Only assign if within max_distance threshold
        if min_distance <= self.max_distance:
            return assigned_player
        
        return -1
