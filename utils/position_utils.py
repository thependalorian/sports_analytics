"""
Position Utilities Module
Helper functions for position calculations and transformations
"""

import numpy as np
import pandas as pd


class PositionCalculator:
    """Utility class for position-related calculations"""
    
    @staticmethod
    def get_bbox_center(bbox):
        """
        Calculate center of bounding box
        
        Args:
            bbox: [x1, y1, x2, y2]
            
        Returns:
            [center_x, center_y]
        """
        x1, y1, x2, y2 = bbox
        return [(x1 + x2) / 2, (y1 + y2) / 2]
    
    @staticmethod
    def get_foot_position(bbox):
        """
        Get foot position (bottom center of bbox) for players
        
        Args:
            bbox: [x1, y1, x2, y2]
            
        Returns:
            [foot_x, foot_y]
        """
        x1, y1, x2, y2 = bbox
        return [(x1 + x2) / 2, y2]
    
    @staticmethod
    def calculate_distance(pos1, pos2):
        """
        Calculate Euclidean distance between two positions
        
        Args:
            pos1: [x1, y1]
            pos2: [x2, y2]
            
        Returns:
            Distance in same units as positions
        """
        return np.linalg.norm(np.array(pos1) - np.array(pos2))


class BallInterpolator:
    """Handles interpolation of missing ball positions"""
    
    @staticmethod
    def interpolate_ball_positions(ball_positions):
        """
        Interpolate missing ball positions using pandas
        
        Args:
            ball_positions: List of dicts with ball data per frame
            
        Returns:
            Interpolated ball positions
        """
        # Extract bbox data
        ball_data = [pos.get(1, {}).get('bbox', []) for pos in ball_positions]
        
        # Create DataFrame
        df_ball = pd.DataFrame(ball_data, columns=['x1', 'y1', 'x2', 'y2'])
        
        # Interpolate missing values
        df_ball = df_ball.interpolate().bfill().ffill()
        
        # Convert back to original format
        return [{1: {"bbox": x}} for x in df_ball.to_numpy().tolist()]
    
    @staticmethod
    def interpolate_linear(positions, missing_indices):
        """
        Linear interpolation for specific missing indices
        
        Args:
            positions: List of positions (can be None)
            missing_indices: List of indices with missing positions
            
        Returns:
            List with interpolated positions
        """
        if not missing_indices:
            return positions
        
        result = positions.copy()
        detected_indices = [i for i, pos in enumerate(positions) if pos is not None]
        
        if len(detected_indices) < 2:
            return result
        
        for idx in missing_indices:
            # Find nearest detections
            prev_idx = max([i for i in detected_indices if i < idx], default=None)
            next_idx = min([i for i in detected_indices if i > idx], default=None)
            
            if prev_idx is not None and next_idx is not None:
                # Linear interpolation
                prev_pos = positions[prev_idx]
                next_pos = positions[next_idx]
                
                weight = (idx - prev_idx) / (next_idx - prev_idx)
                
                interpolated = [
                    prev_pos[j] + weight * (next_pos[j] - prev_pos[j])
                    for j in range(len(prev_pos))
                ]
                
                result[idx] = interpolated
        
        return result


