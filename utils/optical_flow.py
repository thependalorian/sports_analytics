"""
Optical Flow Module
Handles camera movement estimation using optical flow
"""

import cv2
import numpy as np
import pickle
import os


class OpticalFlowTracker:
    """Tracks features using optical flow for camera movement estimation"""
    
    def __init__(self, frame, min_distance=5):
        """
        Initialize optical flow tracker
        
        Args:
            frame: Reference frame
            min_distance: Minimum movement distance to consider
        """
        self.minimum_distance = min_distance
        
        # Optical flow parameters
        self.lk_params = {
            'winSize': (15, 15),
            'maxLevel': 2,
            'criteria': (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        }
        
        # Feature detection parameters
        self.feature_params = {
            'maxCorners': 100,
            'qualityLevel': 0.3,
            'minDistance': 3,
            'blockSize': 7
        }
        
        # Create mask for feature detection
        self.mask = self._create_feature_mask(frame)
    
    def _create_feature_mask(self, frame):
        """
        Create mask to focus on field features
        
        Args:
            frame: Video frame
            
        Returns:
            Binary mask
        """
        h, w = frame.shape[:2]
        mask = np.ones((h, w), dtype=np.uint8) * 255
        
        # Focus on top and bottom regions (field boundaries)
        mask[0:20, :] = 1
        if h > 900:
            mask[h-150:h, :] = 1
        
        return mask
    
    def calculate_movement(self, frames, read_from_stub=False, stub_path=None):
        """
        Calculate camera movement across frames
        
        Args:
            frames: List of video frames
            read_from_stub: Whether to read from cached file
            stub_path: Path to stub file for caching
            
        Returns:
            List of camera movement vectors [(dx, dy), ...]
        """
        # Check stub
        if read_from_stub and stub_path and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                return pickle.load(f)
        
        camera_movement = [[0, 0]] * len(frames)
        
        old_gray = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
        old_features = cv2.goodFeaturesToTrack(old_gray, mask=self.mask, **self.feature_params)
        
        for frame_num in range(1, len(frames)):
            frame_gray = cv2.cvtColor(frames[frame_num], cv2.COLOR_BGR2GRAY)
            
            if old_features is None or len(old_features) == 0:
                old_features = cv2.goodFeaturesToTrack(frame_gray, mask=self.mask, **self.feature_params)
                old_gray = frame_gray.copy()
                continue
            
            # Calculate optical flow
            new_features, status, error = cv2.calcOpticalFlowPyrLK(
                old_gray, frame_gray, old_features, None, **self.lk_params
            )
            
            if new_features is None:
                old_gray = frame_gray.copy()
                continue
            
            # Filter good points
            good_old = old_features[status == 1]
            good_new = new_features[status == 1]
            
            if len(good_old) < 5:
                old_features = cv2.goodFeaturesToTrack(frame_gray, mask=self.mask, **self.feature_params)
                old_gray = frame_gray.copy()
                continue
            
            # Calculate camera movement (median of all feature movements)
            camera_movement_vectors = good_new - good_old
            
            # Use median to be robust to outliers
            camera_movement_x = np.median(camera_movement_vectors[:, 0])
            camera_movement_y = np.median(camera_movement_vectors[:, 1])
            
            if abs(camera_movement_x) > self.minimum_distance or abs(camera_movement_y) > self.minimum_distance:
                camera_movement[frame_num] = [camera_movement_x, camera_movement_y]
                old_features = cv2.goodFeaturesToTrack(frame_gray, mask=self.mask, **self.feature_params)
            
            # Update for next iteration
            old_gray = frame_gray.copy()
            old_features = good_new.reshape(-1, 1, 2)
        
        # Save to stub if requested
        if stub_path:
            os.makedirs(os.path.dirname(stub_path), exist_ok=True)
            with open(stub_path, 'wb') as f:
                pickle.dump(camera_movement, f)
        
        return camera_movement

