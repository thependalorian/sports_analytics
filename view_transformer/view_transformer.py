"""
View Transformer Module
Transforms pixel coordinates to real-world field coordinates
"""

import cv2
import numpy as np


class ViewTransformer:
    """
    Performs perspective transformation from camera view to bird's-eye field view
    """
    
    def __init__(self, pixel_vertices=None, court_length=105, court_width=68):
        """
        Initialize view transformer
        
        Args:
            pixel_vertices: Optional 4 corner points in pixel coordinates
            court_length: Field length in meters (default: 105)
            court_width: Field width in meters (default: 68)
        """
        self.court_length = court_length
        self.court_width = court_width
        
        self.pixel_vertices = None
        self.target_vertices = None
        self.transformation_matrix = None
        
        if pixel_vertices is not None:
            self.set_field_vertices(pixel_vertices)
    
    def set_field_vertices(self, pixel_vertices):
        """
        Set field vertices for perspective transformation
        
        Args:
            pixel_vertices: List of 4 corner points in pixel coordinates
                           [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        """
        if len(pixel_vertices) != 4:
            raise ValueError("pixel_vertices must contain exactly 4 points")
        
        self.pixel_vertices = np.array(pixel_vertices, dtype=np.float32)
        
        # Target vertices (bird's-eye view in meters)
        # Order: top-left, top-right, bottom-right, bottom-left
        self.target_vertices = np.array([
            [0, 0],
            [self.court_length, 0],
            [self.court_length, self.court_width],
            [0, self.court_width]
        ], dtype=np.float32)
        
        # Calculate transformation matrix
        self.transformation_matrix = cv2.getPerspectiveTransform(
            self.pixel_vertices,
            self.target_vertices
        )
    
    def transform_point(self, point):
        """
        Transform a single point from pixel to field coordinates
        
        Args:
            point: [x, y] in pixel coordinates
            
        Returns:
            [x, y] in field coordinates (meters) or None if outside field
        """
        if self.transformation_matrix is None:
            return None
        
        # Check if point is inside field polygon
        p = (int(point[0]), int(point[1]))
        is_inside = cv2.pointPolygonTest(self.pixel_vertices, p, False) >= 0
        
        if not is_inside:
            return None
        
        # Transform point
        reshaped_point = np.array(point).reshape(-1, 1, 2).astype(np.float32)
        transformed_point = cv2.perspectiveTransform(
            reshaped_point,
            self.transformation_matrix
        )
        
        return transformed_point.reshape(-1, 2).squeeze().tolist()
    
    def add_transformed_position_to_tracks(self, tracks):
        """
        Add transformed field positions to all tracks
        
        Args:
            tracks: Tracking dictionary
        """
        for object_type, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    # Get position (adjusted for camera movement if available)
                    position = track_info.get('position_adjusted', track_info.get('position', None))
                    
                    if position is None:
                        continue
                    
                    # Transform to field coordinates
                    position_transformed = self.transform_point(position)
                    
                    if position_transformed is not None:
                        tracks[object_type][frame_num][track_id]['position_transformed'] = position_transformed
    
    def draw_field_overlay(self, frame, alpha=0.3):
        """
        Draw field overlay on frame for visualization
        
        Args:
            frame: Video frame
            alpha: Transparency of overlay
            
        Returns:
            Frame with overlay
        """
        if self.pixel_vertices is None:
            return frame
        
        overlay = frame.copy()
        
        # Draw field polygon
        pts = self.pixel_vertices.astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(overlay, [pts], True, (0, 255, 0), 3)
        
        # Draw corner circles
        for vertex in self.pixel_vertices:
            cv2.circle(overlay, tuple(vertex.astype(int)), 10, (0, 0, 255), -1)
        
        # Blend with original frame
        result = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        
        return result
