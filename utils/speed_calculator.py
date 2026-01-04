"""
Speed Calculator Module
Calculates speeds and distances from position data
"""

import numpy as np


class SpeedCalculator:
    """Calculates speeds and distances from tracking positions"""
    
    def __init__(self, fps=30, window_size=5):
        """
        Initialize speed calculator
        
        Args:
            fps: Video frames per second
            window_size: Number of frames for speed smoothing
        """
        self.fps = fps
        self.frame_window = window_size
        self.frame_rate = 1 / fps  # seconds per frame
    
    def calculate_speed(self, position1, position2, time_elapsed=None):
        """
        Calculate speed between two positions
        
        Args:
            position1: First position [x, y]
            position2: Second position [x, y]
            time_elapsed: Time elapsed in seconds (default: frame_rate)
            
        Returns:
            Speed in m/s
        """
        if position1 is None or position2 is None:
            return 0.0
        
        distance = np.linalg.norm(np.array(position2) - np.array(position1))
        
        if time_elapsed is None:
            time_elapsed = self.frame_rate
        
        if time_elapsed <= 0:
            return 0.0
        
        return distance / time_elapsed
    
    def calculate_distance(self, position1, position2):
        """
        Calculate Euclidean distance between two positions
        
        Args:
            position1: First position [x, y]
            position2: Second position [x, y]
            
        Returns:
            Distance in same units as positions
        """
        if position1 is None or position2 is None:
            return 0.0
        
        return np.linalg.norm(np.array(position2) - np.array(position1))
    
    def smooth_speeds(self, speeds, window_size=None):
        """
        Apply moving average to smooth speed values
        
        Args:
            speeds: List of speed values
            window_size: Window size for smoothing (default: self.frame_window)
            
        Returns:
            List of smoothed speeds
        """
        if window_size is None:
            window_size = self.frame_window
        
        if len(speeds) < 2:
            return speeds
        
        smoothed = []
        for i in range(len(speeds)):
            start_idx = max(0, i - window_size // 2)
            end_idx = min(len(speeds), i + window_size // 2 + 1)
            
            window_speeds = speeds[start_idx:end_idx]
            smoothed.append(np.mean(window_speeds))
        
        return smoothed
    
    def mps_to_kmh(self, speed_mps):
        """Convert meters per second to kilometers per hour"""
        return speed_mps * 3.6
    
    def kmh_to_mps(self, speed_kmh):
        """Convert kilometers per hour to meters per second"""
        return speed_kmh / 3.6

