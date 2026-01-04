"""
Field Mask Module
Handles field boundary detection and filtering
"""

import cv2
import numpy as np
import json
import os


class FieldMask:
    """
    Manages field boundaries and filters detections within field area
    """
    
    def __init__(self, config_path=None, video_name=None):
        """
        Initialize field mask from configuration
        
        Args:
            config_path: Path to field configuration JSON file
            video_name: Name of video for config lookup
        """
        self.polygon = None
        self.enabled = False
        
        if config_path and os.path.exists(config_path):
            self._load_config(config_path, video_name)
    
    def _load_config(self, config_path, video_name):
        """Load field configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Try video-specific config first, then default
            if video_name and video_name in config:
                vertices = config[video_name].get('pixel_vertices', [])
            elif 'default' in config:
                vertices = config['default'].get('pixel_vertices', [])
            else:
                vertices = []
            
            if len(vertices) >= 3:
                self.polygon = np.array(vertices, dtype=np.float32)
                self.enabled = True
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"⚠️  Failed to load field config: {e}")
            self.enabled = False
    
    def is_inside_field(self, position):
        """
        Check if a position is inside the field boundary
        
        Args:
            position: (x, y) tuple or list
            
        Returns:
            True if inside field, False otherwise
        """
        if not self.enabled or self.polygon is None:
            return True  # If no mask, allow all positions
        
        point = (float(position[0]), float(position[1]))
        return cv2.pointPolygonTest(self.polygon, point, False) >= 0
    
    def get_field_bounds(self):
        """
        Get bounding rectangle of field
        
        Returns:
            (x_min, y_min, x_max, y_max) or None if not enabled
        """
        if not self.enabled or self.polygon is None:
            return None
        
        x_coords = self.polygon[:, 0]
        y_coords = self.polygon[:, 1]
        
        return (
            float(np.min(x_coords)),
            float(np.min(y_coords)),
            float(np.max(x_coords)),
            float(np.max(y_coords))
        )


