"""
Speed and Distance Estimator Module
Calculates player speeds and distances covered
Uses modular speed calculation components
"""

import cv2
import numpy as np

# Handle imports
try:
    from ..utils.speed_calculator import SpeedCalculator
except ImportError:
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.speed_calculator import SpeedCalculator


class SpeedAndDistanceEstimator:
    """
    Estimates player speeds and distances from tracking data
    Uses modular speed calculator
    """
    
    def __init__(self, fps=30, window_size=5):
        """
        Initialize speed and distance estimator
        
        Args:
            fps: Video frames per second
            window_size: Number of frames for speed smoothing
        """
        self.fps = fps
        self.frame_window = window_size
        
        # Initialize modular speed calculator
        self.speed_calculator = SpeedCalculator(fps=fps, window_size=window_size)
    
    def add_speed_and_distance_to_tracks(self, tracks):
        """
        Calculate and add speed and distance to tracks
        
        Args:
            tracks: Tracking dictionary
        """
        total_distance = {}
        
        for object_type, object_tracks in tracks.items():
            if object_type == "ball" or object_type == "referees":
                continue
            
            if len(object_tracks) < 2:
                continue
            
            # Calculate for each track ID
            track_ids = set()
            for frame_track in object_tracks:
                track_ids.update(frame_track.keys())
            
            for track_id in track_ids:
                total_distance[track_id] = 0.0
                prev_position = None
                speeds = []
                frame_indices = []
                
                for frame_num, track in enumerate(object_tracks):
                    if track_id not in track:
                        continue
                    
                    track_info = track[track_id]
                    
                    # Get transformed position (in meters)
                    position = track_info.get('position_transformed', None)
                    
                    if position is None:
                        position = track_info.get('position', None)
                    
                    if position is None:
                        track[track_id]['speed'] = 0.0
                        track[track_id]['distance_covered'] = total_distance[track_id]
                        continue
                    
                    if prev_position is not None:
                        # Calculate distance moved
                        distance = self.speed_calculator.calculate_distance(prev_position, position)
                        total_distance[track_id] += distance
                        
                        # Calculate speed
                        speed = self.speed_calculator.calculate_speed(prev_position, position)
                        speeds.append(speed)
                        frame_indices.append(frame_num)
                    
                    # Add to track info
                    track[track_id]['speed'] = speeds[-1] if speeds else 0.0
                    track[track_id]['distance_covered'] = total_distance[track_id]
                    track[track_id]['speed_kmh'] = self.speed_calculator.mps_to_kmh(
                        track[track_id]['speed']
                    )
                    track[track_id]['distance_meters'] = total_distance[track_id]
                    
                    prev_position = position
                
                # Smooth speeds
                if speeds:
                    smoothed_speeds = self.speed_calculator.smooth_speeds(speeds)
                    for i, frame_num in enumerate(frame_indices):
                        if frame_num < len(object_tracks):
                            object_tracks[frame_num][track_id]['speed'] = smoothed_speeds[i]
                            object_tracks[frame_num][track_id]['speed_kmh'] = \
                                self.speed_calculator.mps_to_kmh(smoothed_speeds[i])
    
    def draw_speed_and_distance(self, frames, tracks):
        """
        Draw speed and distance information on frames
        
        Args:
            frames: List of video frames
            tracks: Tracking dictionary
            
        Returns:
            Annotated frames
        """
        output_frames = []
        
        for frame_num, frame in enumerate(frames):
            frame = frame.copy()
            
            # Draw player speeds
            if frame_num < len(tracks.get('players', [])):
                for track_id, player in tracks['players'][frame_num].items():
                    speed_kmh = player.get('speed_kmh', 0)
                    distance = player.get('distance_meters', 0)
                    
                    bbox = player.get('bbox', [0, 0, 0, 0])
                    x1, y1, x2, y2 = [int(v) for v in bbox]
                    
                    # Display speed and distance
                    position = (int((x1 + x2) / 2), int(bbox[3]) + 40)
                    
                    cv2.putText(frame, f"{speed_kmh:.2f} km/h",
                               position, cv2.FONT_HERSHEY_SIMPLEX,
                               0.5, (0, 0, 0), 2)
                    
                    cv2.putText(frame, f"{distance:.2f} m",
                               (position[0], position[1] + 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            output_frames.append(frame)
        
        return output_frames
    
    def get_max_speeds(self, tracks):
        """
        Get maximum speeds for each track
        
        Args:
            tracks: Tracking dictionary
            
        Returns:
            Dictionary of {track_id: max_speed_kmh}
        """
        max_speeds = {}
        
        for object_type, object_tracks in tracks.items():
            for frame_track in object_tracks:
                for track_id, track_info in frame_track.items():
                    speed_kmh = track_info.get('speed_kmh', 0)
                    
                    if track_id not in max_speeds:
                        max_speeds[track_id] = speed_kmh
                    else:
                        max_speeds[track_id] = max(max_speeds[track_id], speed_kmh)
        
        return max_speeds
    
    def get_total_distances(self, tracks):
        """
        Get total distances covered for each track
        
        Args:
            tracks: Tracking dictionary
            
        Returns:
            Dictionary of {track_id: total_distance_meters}
        """
        total_distances = {}
        
        for object_type, object_tracks in tracks.items():
            for frame_track in object_tracks:
                for track_id, track_info in frame_track.items():
                    distance = track_info.get('distance_meters', 0)
                    
                    if track_id not in total_distances:
                        total_distances[track_id] = distance
                    else:
                        total_distances[track_id] = max(total_distances[track_id], distance)
        
        return total_distances
