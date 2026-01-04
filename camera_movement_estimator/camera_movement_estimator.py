"""
Camera Movement Estimator Module
Estimates camera movement using optical flow
Uses modular optical flow components
"""

import cv2
import numpy as np

# Handle imports
try:
    from ..utils.optical_flow import OpticalFlowTracker
except ImportError:
    import sys
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.optical_flow import OpticalFlowTracker


class CameraMovementEstimator:
    """
    Estimates camera movement between frames using optical flow
    Uses modular optical flow tracker
    """
    
    def __init__(self, frame, min_distance=5):
        """
        Initialize camera movement estimator
        
        Args:
            frame: Reference frame for feature detection
            min_distance: Minimum movement distance to consider
        """
        # Initialize modular optical flow tracker
        self.flow_tracker = OpticalFlowTracker(frame, min_distance=min_distance)
    
    def get_camera_movement(self, frames, read_from_stub=False, stub_path=None):
        """
        Calculate camera movement across frames
        
        Args:
            frames: List of video frames
            read_from_stub: Whether to read from cached file
            stub_path: Path to stub file for caching
            
        Returns:
            List of camera movement vectors [(dx, dy), ...]
        """
        return self.flow_tracker.calculate_movement(frames, read_from_stub, stub_path)
    
    def adjust_positions_to_tracks(self, tracks, camera_movement_per_frame):
        """
        Adjust object positions based on camera movement
        
        Args:
            tracks: Tracking dictionary
            camera_movement_per_frame: List of camera movement vectors
        """
        for object_type, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    position = track_info.get('position', [0, 0])
                    
                    if frame_num < len(camera_movement_per_frame):
                        camera_move_x, camera_move_y = camera_movement_per_frame[frame_num]
                    else:
                        camera_move_x, camera_move_y = 0, 0
                    
                    # Adjust position by camera movement
                    adjusted_position = [
                        position[0] - camera_move_x,
                        position[1] - camera_move_y
                    ]
                    
                    tracks[object_type][frame_num][track_id]['position_adjusted'] = adjusted_position
    
    def draw_camera_movement(self, frames, camera_movement):
        """
        Draw camera movement visualization on frames
        
        Args:
            frames: List of video frames
            camera_movement: List of camera movement vectors
            
        Returns:
            Annotated frames
        """
        output_frames = []
        
        for frame_num, frame in enumerate(frames):
            frame = frame.copy()
            
            if frame_num < len(camera_movement):
                dx, dy = camera_movement[frame_num]
                
                # Draw movement vector
                start_point = (50, 50)
                end_point = (int(50 + dx * 5), int(50 + dy * 5))  # Scale for visibility
                
                cv2.arrowedLine(frame, start_point, end_point, (0, 255, 0), 2, tipLength=0.3)
                
                # Display movement values
                text = f"Camera: dx={dx:.1f}, dy={dy:.1f}"
                cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            output_frames.append(frame)
        
        return output_frames
