"""
Jersey Tracker Module
Handles player detection, tracking, and jersey number recognition
Uses modular components for field masking, jersey detection, and annotations
"""

import cv2
import numpy as np
import os
from collections import defaultdict
from ultralytics import YOLO
import supervision as sv

import sys
import os

# Handle imports - try relative first, then absolute
try:
    from ..utils.field_mask import FieldMask
    from ..utils.jersey_detector import JerseyNumberDetector
    from ..utils.position_utils import PositionCalculator, BallInterpolator
    from ..utils.annotation_drawer import AnnotationDrawer
except ImportError:
    # Fallback to absolute imports if relative fails
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from utils.field_mask import FieldMask
    from utils.jersey_detector import JerseyNumberDetector
    from utils.position_utils import PositionCalculator, BallInterpolator
    from utils.annotation_drawer import AnnotationDrawer


class JerseyTracker:
    """
    Advanced player tracking with jersey number detection
    Uses modular components for maintainability
    """

    def __init__(self, model_path, field_config_path=None, video_name=None,
                 confidence_threshold=0.5, enable_ocr=True):
        """
        Initialize the Jersey Tracker

        Args:
            model_path: Path to YOLOv8/v11 model
            field_config_path: Path to field configuration JSON
            video_name: Name of the video for field config lookup
            confidence_threshold: Detection confidence threshold
            enable_ocr: Whether to enable jersey number OCR
        """
        # Initialize YOLO model
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

        # Initialize tracker
        self.tracker = sv.ByteTrack()

        # Initialize modular components
        self.field_mask = FieldMask(field_config_path, video_name)
        
        if enable_ocr:
            self.jersey_detector = JerseyNumberDetector(
                languages=['en'],
                gpu=True,
                confidence_threshold=0.5
            )
        else:
            self.jersey_detector = None
        
        self.position_calculator = PositionCalculator()
        self.ball_interpolator = BallInterpolator()
        self.annotation_drawer = AnnotationDrawer()
        
        # Track ID mappings
        self.global_track_mapping = {}
        self.next_temp_id = 1001

        # Class mappings
        self.class_names = {0: 'goalkeeper', 1: 'player', 2: 'referee', 3: 'ball'}

    def process_chunk(self, frames, chunk_idx=0):
        """
        Process a chunk of frames with detection and tracking

        Args:
            frames: List of video frames
            chunk_idx: Chunk index for tracking continuity

        Returns:
            Dictionary with tracks for players, ball, and referees
        """
        # Detect objects in frames
        detections = self._detect_frames(frames)
        
        # Initialize tracks structure
        tracks = {"players": [], "referees": [], "ball": []}

        # Process each frame
        for frame_num, detection in enumerate(detections):
            # Prepare detections for tracking
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}
            detection_sv = sv.Detections.from_ultralytics(detection)
            
            # Convert goalkeepers to players for tracking
            for obj_idx, class_id in enumerate(detection_sv.class_id):
                if cls_names.get(class_id) == "goalkeeper":
                    detection_sv.class_id[obj_idx] = cls_names_inv.get("player", class_id)

            # Update tracker
            detection_with_tracks = self.tracker.update_with_detections(detection_sv)

            # Initialize frame tracks
            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})
            
            # Process tracked detections
            for frame_det in detection_with_tracks:
                bbox = frame_det[0].tolist()
                class_id = frame_det[3]
                bytetrack_id = int(frame_det[4])
                class_name = cls_names.get(class_id, "unknown")
                
                if class_name == "player":
                    self._process_player(
                        frames[frame_num],
                        bbox,
                        bytetrack_id,
                        tracks["players"][frame_num]
                    )
                elif class_name == "referee":
                    tracks["referees"][frame_num][bytetrack_id] = {"bbox": bbox}
            
            # Process ball detections (not tracked)
            for frame_det in detection_sv:
                bbox = frame_det[0].tolist()
                class_id = frame_det[3]
                if cls_names.get(class_id) == "ball":
                    tracks["ball"][frame_num][1] = {"bbox": bbox}

        return tracks

    def _process_player(self, frame, bbox, bytetrack_id, frame_players):
        """
        Process a single player detection

        Args:
            frame: Video frame
            bbox: Bounding box
            bytetrack_id: ByteTrack ID
            frame_players: Dictionary to add player to
        """
        # Check if player is inside field
        foot_x = (bbox[0] + bbox[2]) / 2
        foot_y = bbox[3]
        
        if not self.field_mask.is_inside_field((foot_x, foot_y)):
            return
        
        # Detect jersey number
        jersey_number = None
        if self.jersey_detector:
            jersey_number = self.jersey_detector.detect_number(
                frame, bbox, bytetrack_id
            )
        
        # Determine track ID (use jersey number if available)
        if jersey_number:
            track_id = jersey_number
            self.global_track_mapping[bytetrack_id] = jersey_number
        elif bytetrack_id in self.global_track_mapping:
            track_id = self.global_track_mapping[bytetrack_id]
        else:
            track_id = 1000 + bytetrack_id
        
        # Add player to tracks
        frame_players[track_id] = {
            "bbox": bbox,
            "original_track_id": bytetrack_id,
            "jersey_number": jersey_number if jersey_number else None
        }
    
    def _detect_frames(self, frames, batch_size=20):
        """
        Detect objects in frames using YOLO
        
        Args:
            frames: List of frames
            batch_size: Batch size for detection
            
        Returns:
            List of detection results
        """
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i+batch_size]
            batch_detections = self.model.predict(
                batch, conf=self.confidence_threshold, verbose=False
            )
            detections.extend(batch_detections)
        return detections

    def add_position_to_tracks(self, tracks):
        """
        Add position information to tracks

        Args:
            tracks: Dictionary of tracks
        """
        for object_type, object_tracks in tracks.items():
            for frame_num, track in enumerate(object_tracks):
                for track_id, track_info in track.items():
                    bbox = track_info['bbox']

                    if object_type == 'ball':
                        position = self.position_calculator.get_bbox_center(bbox)
                    else:
                        position = self.position_calculator.get_foot_position(bbox)

                    tracks[object_type][frame_num][track_id]['position'] = position

    def interpolate_ball_positions(self, ball_positions):
        """
        Interpolate missing ball positions

        Args:
            ball_positions: List of ball position dicts per frame

        Returns:
            Interpolated ball positions
        """
        return self.ball_interpolator.interpolate_ball_positions(ball_positions)

    def draw_annotations(self, video_frames, tracks, team_ball_control):
        """
        Draw tracking annotations on frames

        Args:
            video_frames: List of video frames
            tracks: Dictionary of tracks
            team_ball_control: Array of team possession per frame

        Returns:
            Annotated frames
        """
        return self.annotation_drawer.draw_annotations(
            video_frames, tracks, team_ball_control
        )

    def export_jersey_mapping(self, output_path):
        """
        Export jersey number to track ID mapping

        Args:
            output_path: CSV output path
        """
        import csv

        if not self.jersey_detector:
            return
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        mapping = self.jersey_detector.get_jersey_mapping()

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['bytetrack_id', 'jersey_number', 'detections', 'confidence'])

            for orig_id, jersey in sorted(mapping.items()):
                stats = self.jersey_detector.get_detection_stats(orig_id)
                writer.writerow([
                    orig_id,
                    jersey,
                    stats['detections'],
                    f"{stats['confidence']:.2f}"
                ])

        print(f"✓ Jersey mapping exported: {output_path}")
