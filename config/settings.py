"""
Global Settings and Configuration
Location: /config/settings.py
Purpose: Centralized configuration for the sports analytics pipeline
Modular design with sport-specific configurations

For sport-specific settings, see config/sports_config.py
"""

import os
from pathlib import Path
from typing import Dict, Any
import json


class Settings:
    """Global settings for sports analytics pipeline"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    MODELS_DIR = PROJECT_ROOT / "models"
    CONFIG_DIR = PROJECT_ROOT / "config"
    INPUT_VIDEOS_DIR = PROJECT_ROOT / "input_videos"
    OUTPUT_VIDEOS_DIR = PROJECT_ROOT / "output_videos"
    LOGS_DIR = PROJECT_ROOT / "logs"
    DATA_DIR = PROJECT_ROOT / "data"
    
    # Model settings - YOLO11x for Football/Soccer (Recommended over YOLOv8)
    # YOLO11x: 54.7 mAP, 22% fewer parameters, optimized for edge devices
    DEFAULT_MODEL_PATH = MODELS_DIR / "yolo11x.pt"
    LEGACY_MODEL_PATH = MODELS_DIR / "best.pt"  # Fallback if yolo11x.pt not found
    CONFIDENCE_THRESHOLD = 0.5  # Detection confidence (0.0-1.0, higher = fewer false positives)
    
    # Tracking settings
    TRACKER_TYPE = "ByteTrack"
    MIN_TRACK_LENGTH = 5
    
    # Jersey detection settings
    ENABLE_OCR = True
    OCR_CONFIDENCE_THRESHOLD = 0.5
    OCR_LANGUAGES = ['en']
    OCR_USE_GPU = True
    
    # Team assignment settings
    USE_LAB_COLOR_SPACE = True
    TEAM_CLUSTERING_RANDOM_STATE = 42
    
    # Ball assignment settings
    MAX_BALL_PLAYER_DISTANCE = 70  # pixels
    
    # Pass detection settings
    MIN_POSSESSION_FRAMES = 5
    MAX_PASS_DISTANCE = 50  # meters
    
    # Speed and distance settings
    DEFAULT_FPS = 30
    SPEED_WINDOW_SIZE = 5
    FRAME_WINDOW = 5
    
    # Event detection settings
    SPRINT_THRESHOLD = 7.0  # m/s
    CLUSTER_DISTANCE_THRESHOLD = 10.0  # meters
    
    # Field settings (Football/Soccer - FIFA Standard)
    # For other sports, use config/sports_config.py
    FIELD_LENGTH_M = 105  # Football pitch length (FIFA recommended)
    FIELD_WIDTH_M = 68    # Football pitch width (FIFA recommended)
    FIELD_CONFIG_PATH = CONFIG_DIR / "field_config.json"
    
    # Sport selection (default)
    DEFAULT_SPORT = "football"  # Options: football, basketball, rugby, netball
    
    # Camera movement settings
    CAMERA_MIN_DISTANCE = 5
    OPTICAL_FLOW_WIN_SIZE = (15, 15)
    OPTICAL_FLOW_MAX_LEVEL = 2
    
    # Processing settings
    CHUNK_SIZE = 300  # frames
    BATCH_SIZE = 20  # frames for YOLO
    
    # Heatmap settings
    HEATMAP_RESOLUTION = (1050, 680)
    HEATMAP_BLUR_KERNEL = 51
    HEATMAP_BLUR_SIGMA = 15
    
    # Visualization settings
    ANNOTATION_FONT_SCALE = 0.5
    ANNOTATION_THICKNESS = 2
    PLAYER_COLORS = {
        1: (255, 0, 0),    # Red
        2: (0, 0, 255),    # Blue
        'referee': (0, 255, 255),  # Yellow
        'ball': (0, 255, 0)  # Green
    }
    
    # Export settings
    EXPORT_CSV = True
    EXPORT_JSON = True
    EXPORT_REPORTS = True
    EXPORT_HEATMAPS = True
    EXPORT_VISUALIZATIONS = True
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_TO_FILE = True
    LOG_DIR = LOGS_DIR
    
    @classmethod
    def load_from_file(cls, config_path: str = None):
        """
        Load settings from JSON file
        
        Args:
            config_path: Path to config file (default: config/settings.json)
        """
        if config_path is None:
            config_path = cls.CONFIG_DIR / "settings.json"
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Update class attributes
            for key, value in config.items():
                if hasattr(cls, key):
                    setattr(cls, key, value)
    
    @classmethod
    def save_to_file(cls, config_path: str = None):
        """
        Save current settings to JSON file
        
        Args:
            config_path: Path to save config (default: config/settings.json)
        """
        if config_path is None:
            config_path = cls.CONFIG_DIR / "settings.json"
        
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Get all uppercase attributes (settings)
        settings = {
            key: getattr(cls, key)
            for key in dir(cls)
            if key.isupper() and not key.startswith('_')
        }
        
        # Convert Path objects to strings
        for key, value in settings.items():
            if isinstance(value, Path):
                settings[key] = str(value)
        
        with open(config_path, 'w') as f:
            json.dump(settings, f, indent=2, default=str)
    
    @classmethod
    def get_dict(cls) -> Dict[str, Any]:
        """
        Get all settings as dictionary
        
        Returns:
            Dictionary of all settings
        """
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if key.isupper() and not key.startswith('_')
        }
    
    @classmethod
    def ensure_directories(cls):
        """Create all necessary directories"""
        directories = [
            cls.MODELS_DIR,
            cls.CONFIG_DIR,
            cls.INPUT_VIDEOS_DIR,
            cls.OUTPUT_VIDEOS_DIR,
            cls.LOGS_DIR,
            cls.DATA_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)


# Initialize settings
Settings.ensure_directories()

