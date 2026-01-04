"""
Sports Configuration Module
Location: /config/sports_config.py
Purpose: Sport-specific configurations (Football, Basketball, Rugby, etc.)
Modular design for easy multi-sport extension

This module defines configurations for different sports, starting with Football/Soccer
as the primary focus. Other sports can be added using the same pattern.
"""

from typing import Dict, List, Tuple, Any
from dataclasses import dataclass


@dataclass
class SportConfig:
    """
    Base configuration for any sport
    Defines common attributes that all sports share
    """
    # Identification
    id: str                          # Unique identifier (e.g., "football", "basketball")
    name: str                        # Display name (e.g., "Football", "Basketball")
    icon: str                        # Unicode emoji or icon identifier
    
    # Playing Area
    field_length_m: float            # Length in meters
    field_width_m: float             # Width in meters
    field_name: str                  # e.g., "pitch", "court", "field"
    
    # Participants
    players_per_team: int            # Standard team size
    max_players: int                 # Maximum on field (inc. substitutes)
    has_goalkeeper: bool             # Does sport have goalkeeper?
    
    # Timing
    periods: int                     # Number of periods/halves
    period_duration_minutes: int     # Duration of each period
    total_duration_minutes: int      # Total match duration
    
    # Scoring
    score_types: List[str]           # e.g., ["goal", "penalty"], ["basket", "free throw"]
    
    # Detection Classes (YOLO)
    yolo_classes: Dict[int, str]     # YOLO class mappings {0: 'goalkeeper', 1: 'player', ...}
    
    # Event Types
    event_types: List[str]           # Sport-specific events
    
    # Metrics
    key_metrics: List[str]           # Primary statistics to track


# ============================================================================
# FOOTBALL / SOCCER CONFIGURATION (PRIMARY FOCUS)
# ============================================================================

FOOTBALL_CONFIG = SportConfig(
    # Identification
    id="football",
    name="Football",
    icon="⚽",
    
    # Playing Area (FIFA Standard)
    field_length_m=105.0,  # International: 100-110m, FIFA: 105m recommended
    field_width_m=68.0,    # International: 64-75m, FIFA: 68m recommended
    field_name="pitch",
    
    # Participants
    players_per_team=11,   # Goalkeeper + 10 outfield
    max_players=14,        # 11 starting + 3 substitutes on bench
    has_goalkeeper=True,
    
    # Timing
    periods=2,             # Two halves
    period_duration_minutes=45,  # 45 minutes per half
    total_duration_minutes=90,   # Plus stoppage time (not counted)
    
    # Scoring
    score_types=["goal", "penalty", "own_goal", "free_kick"],
    
    # Detection Classes (YOLO)
    yolo_classes={
        0: "goalkeeper",
        1: "player",       # Outfield player
        2: "referee",      # Including linesmen
        3: "ball"
    },
    
    # Event Types (Football-Specific)
    event_types=[
        "goal",
        "shot",
        "save",
        "pass",
        "tackle",
        "foul",
        "yellow_card",
        "red_card",
        "corner",
        "free_kick",
        "penalty",
        "offside",
        "substitution",
        "sprint",          # Detected via analytics
        "cluster",         # Detected via analytics (set pieces)
        "trajectory_change"  # Detected via analytics (shots, clearances)
    ],
    
    # Key Metrics (Football Performance)
    key_metrics=[
        "distance_covered_m",
        "max_speed_kmh",
        "avg_speed_kmh",
        "sprints_count",
        "passes_made",
        "pass_accuracy_pct",
        "passes_received",
        "time_with_ball_sec",
        "tackles",
        "interceptions",
        "shots",
        "goals",
        "assists",
        "touches",
        "duels_won",
        "aerial_duels_won"
    ]
)


# Field Zones (Football-Specific)
FOOTBALL_ZONES = {
    "defensive_third": {
        "x_range": (0, 35),  # Meters from own goal
        "description": "Defensive third - own penalty area to 1/3 line"
    },
    "middle_third": {
        "x_range": (35, 70),
        "description": "Middle third - midfield area"
    },
    "attacking_third": {
        "x_range": (70, 105),
        "description": "Attacking third - opposition penalty area"
    },
    "left_wing": {
        "y_range": (0, 22.67),  # Meters from left touchline
        "description": "Left wing area"
    },
    "center": {
        "y_range": (22.67, 45.33),
        "description": "Central area"
    },
    "right_wing": {
        "y_range": (45.33, 68),
        "description": "Right wing area"
    }
}


# Football Positions (Standard 4-4-2, 4-3-3, etc.)
FOOTBALL_POSITIONS = {
    "GK": {"name": "Goalkeeper", "zone": "defensive_third", "x_avg": 5, "y_avg": 34},
    "LB": {"name": "Left Back", "zone": "defensive_third", "x_avg": 20, "y_avg": 10},
    "CB_L": {"name": "Center Back (Left)", "zone": "defensive_third", "x_avg": 20, "y_avg": 25},
    "CB_R": {"name": "Center Back (Right)", "zone": "defensive_third", "x_avg": 20, "y_avg": 43},
    "RB": {"name": "Right Back", "zone": "defensive_third", "x_avg": 20, "y_avg": 58},
    "LM": {"name": "Left Midfielder", "zone": "middle_third", "x_avg": 52, "y_avg": 10},
    "CM_L": {"name": "Center Midfielder (Left)", "zone": "middle_third", "x_avg": 52, "y_avg": 25},
    "CM_R": {"name": "Center Midfielder (Right)", "zone": "middle_third", "x_avg": 52, "y_avg": 43},
    "RM": {"name": "Right Midfielder", "zone": "middle_third", "x_avg": 52, "y_avg": 58},
    "LW": {"name": "Left Winger", "zone": "attacking_third", "x_avg": 85, "y_avg": 10},
    "ST": {"name": "Striker", "zone": "attacking_third", "x_avg": 85, "y_avg": 34},
    "RW": {"name": "Right Winger", "zone": "attacking_third", "x_avg": 85, "y_avg": 58}
}


# Event Detection Thresholds (Football-Specific)
FOOTBALL_THRESHOLDS = {
    "sprint_speed_mps": 7.0,        # 25.2 km/h (professional sprint threshold)
    "high_speed_mps": 5.5,          # 19.8 km/h (high-intensity running)
    "jog_speed_mps": 3.0,           # 10.8 km/h (jogging)
    "walk_speed_mps": 1.5,          # 5.4 km/h (walking)
    
    "cluster_distance_m": 5.0,      # Players within 5m = cluster (corners, free kicks)
    "pass_max_distance_m": 50.0,    # Maximum valid pass distance
    "pass_min_distance_m": 2.0,     # Minimum pass distance (avoid noise)
    
    "shot_distance_m": 35.0,        # Distance from goal for shot classification
    "ball_speed_shot_mps": 15.0,    # Ball speed threshold for shot detection
    
    "possession_min_frames": 5,     # Minimum frames to confirm possession (0.17s at 30fps)
}


# ============================================================================
# MULTI-SPORT CONFIGURATIONS (Future Expansion)
# ============================================================================

# These configs follow the same pattern as FOOTBALL_CONFIG
# Uncomment and complete as needed for multi-sport support

BASKETBALL_CONFIG = SportConfig(
    id="basketball",
    name="Basketball",
    icon="🏀",
    field_length_m=28.0,    # NBA/FIBA court length
    field_width_m=15.0,     # NBA/FIBA court width
    field_name="court",
    players_per_team=5,
    max_players=7,          # 5 starting + 2 subs on bench (simplified)
    has_goalkeeper=False,
    periods=4,              # Four quarters
    period_duration_minutes=12,  # NBA: 12 min, FIBA: 10 min
    total_duration_minutes=48,
    score_types=["basket", "free_throw", "three_pointer"],
    yolo_classes={0: "player", 1: "ball", 2: "referee"},
    event_types=["basket", "rebound", "assist", "block", "steal", "foul", "turnover"],
    key_metrics=["points", "rebounds", "assists", "steals", "blocks", "turnovers", "fg_pct"]
)


RUGBY_CONFIG = SportConfig(
    id="rugby",
    name="Rugby",
    icon="🏉",
    field_length_m=100.0,   # Plus in-goal areas (10m each)
    field_width_m=70.0,
    field_name="field",
    players_per_team=15,    # Rugby Union (Rugby League = 13)
    max_players=23,         # 15 starting + 8 reserves
    has_goalkeeper=False,
    periods=2,              # Two halves
    period_duration_minutes=40,
    total_duration_minutes=80,
    score_types=["try", "conversion", "penalty", "drop_goal"],
    yolo_classes={0: "player", 1: "ball", 2: "referee"},
    event_types=["try", "tackle", "ruck", "maul", "scrum", "lineout", "conversion"],
    key_metrics=["tries", "tackles", "meters_gained", "carries", "turnovers"]
)


# ============================================================================
# NAMIBIAN-SPECIFIC CONFIGURATIONS
# ============================================================================

# Adjustments for Namibian football conditions
NAMIBIAN_FOOTBALL_ADJUSTMENTS = {
    "detection": {
        "confidence_threshold": 0.45,    # Slightly lower (dusty conditions, faded jerseys)
        "nms_threshold": 0.4,            # Non-max suppression (more lenient)
        "max_detections": 50             # Allow more detections (spectators near pitch)
    },
    
    "ocr": {
        "confidence_threshold": 0.4,     # Lower for faded jerseys
        "preprocessing": "enhance",      # Enhance contrast before OCR
        "fallback": "color_matching"     # Use color if OCR fails
    },
    
    "field": {
        "tolerance": 0.95,               # 95% confidence for field boundary (dusty lines)
        "line_enhancement": True         # Enhance white lines before detection
    },
    
    "processing": {
        "chunk_size": 200,               # Smaller chunks for Raspberry Pi (less RAM)
        "skip_frames": 1,                # Process every frame (no skipping, accuracy first)
        "low_memory_mode": True          # Optimize for edge devices
    },
    
    "lighting": {
        "auto_brightness": True,         # Auto-adjust for sun glare
        "shadow_compensation": True,     # Handle afternoon shadows
        "low_light_boost": True          # Boost evening match visibility
    }
}


# Stadium-Specific Calibrations (Pre-Configured)
NAMIBIAN_STADIUMS = {
    "dr_hage_geingob": {
        "name": "Dr Hage Geingob Stadium",
        "location": "Windhoek",
        "capacity": 10000,
        "field_dims": (105, 68),
        "camera_height_m": 20,           # Estimated
        "camera_angle_deg": 15,          # Downward tilt
        "lighting": "good",              # Stadium lights available
        "pitch_condition": "good",       # Well-maintained
        "venue_id": "NAM_WDH_001"
    },
    
    "unam_sam_nujoma": {
        "name": "UNAM Sam Nujoma Campus Stadium",
        "location": "Windhoek (UNAM Main Campus)",
        "capacity": 2000,
        "field_dims": (105, 68),
        "camera_height_m": 15,
        "camera_angle_deg": 10,
        "lighting": "fair",              # Natural light + basic lights
        "pitch_condition": "good",
        "venue_id": "NAM_WDH_UNAM_001"
    },
    
    "oshakati_stadium": {
        "name": "Oshakati Stadium",
        "location": "Oshakati (UNAM Northern Campus)",
        "capacity": 5000,
        "field_dims": (105, 68),
        "camera_height_m": 12,
        "camera_angle_deg": 12,
        "lighting": "fair",
        "pitch_condition": "fair",       # Dusty in dry season
        "venue_id": "NAM_OSH_001"
    },
    
    "rundu_sports_complex": {
        "name": "Rundu Sports Complex",
        "location": "Rundu (UNAM Kavango Campus)",
        "capacity": 3000,
        "field_dims": (100, 65),         # Slightly smaller
        "camera_height_m": 10,
        "camera_angle_deg": 15,
        "lighting": "poor",              # Limited stadium lights
        "pitch_condition": "fair",
        "venue_id": "NAM_RUN_001"
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_sport_config(sport_id: str) -> SportConfig:
    """
    Get configuration for a specific sport
    
    Args:
        sport_id: Sport identifier (e.g., "football", "basketball")
        
    Returns:
        SportConfig object
        
    Raises:
        ValueError: If sport not supported
    """
    configs = {
        "football": FOOTBALL_CONFIG,
        "soccer": FOOTBALL_CONFIG,  # Alias
        "basketball": BASKETBALL_CONFIG,
        "rugby": RUGBY_CONFIG
    }
    
    if sport_id.lower() not in configs:
        raise ValueError(
            f"Sport '{sport_id}' not supported. "
            f"Available: {', '.join(configs.keys())}"
        )
    
    return configs[sport_id.lower()]


def get_sport_zones(sport_id: str) -> Dict[str, Dict]:
    """
    Get field zones for a specific sport
    
    Args:
        sport_id: Sport identifier
        
    Returns:
        Dictionary of zone definitions
    """
    zones = {
        "football": FOOTBALL_ZONES,
        "soccer": FOOTBALL_ZONES,
        # Add other sports here
    }
    
    return zones.get(sport_id.lower(), {})


def get_sport_positions(sport_id: str) -> Dict[str, Dict]:
    """
    Get standard positions for a sport
    
    Args:
        sport_id: Sport identifier
        
    Returns:
        Dictionary of position definitions
    """
    positions = {
        "football": FOOTBALL_POSITIONS,
        "soccer": FOOTBALL_POSITIONS,
        # Add other sports here
    }
    
    return positions.get(sport_id.lower(), {})


def get_sport_thresholds(sport_id: str) -> Dict[str, float]:
    """
    Get event detection thresholds for a sport
    
    Args:
        sport_id: Sport identifier
        
    Returns:
        Dictionary of threshold values
    """
    thresholds = {
        "football": FOOTBALL_THRESHOLDS,
        "soccer": FOOTBALL_THRESHOLDS,
        # Add other sports here
    }
    
    return thresholds.get(sport_id.lower(), {})


def get_namibian_stadium_config(stadium_id: str) -> Dict[str, Any]:
    """
    Get configuration for a Namibian stadium
    
    Args:
        stadium_id: Stadium identifier (e.g., "dr_hage_geingob")
        
    Returns:
        Stadium configuration dictionary
    """
    return NAMIBIAN_STADIUMS.get(stadium_id.lower(), {})


def list_supported_sports() -> List[str]:
    """Get list of supported sports"""
    return ["football", "basketball", "rugby"]


def list_namibian_stadiums() -> List[str]:
    """Get list of pre-configured Namibian stadiums"""
    return list(NAMIBIAN_STADIUMS.keys())


# ============================================================================
# SPORT DETECTION (Auto-detect sport from video - Future)
# ============================================================================

def detect_sport_from_field(field_length_m: float, field_width_m: float) -> str:
    """
    Auto-detect sport based on field dimensions
    
    Args:
        field_length_m: Measured field length
        field_width_m: Measured field width
        
    Returns:
        Sport ID (e.g., "football", "basketball")
    """
    # Football: ~100-110m × 64-75m
    if 90 < field_length_m < 120 and 60 < field_width_m < 80:
        return "football"
    
    # Basketball: ~28m × 15m
    if 24 < field_length_m < 32 and 12 < field_width_m < 18:
        return "basketball"
    
    # Rugby: ~100m × 70m (similar to football, but wider)
    if 90 < field_length_m < 110 and 68 < field_width_m < 75:
        return "rugby"  # Hard to distinguish from football, user must specify
    
    return "unknown"


# ============================================================================
# VALIDATION & TESTING
# ============================================================================

def validate_config(config: SportConfig) -> bool:
    """
    Validate sport configuration
    
    Args:
        config: SportConfig to validate
        
    Returns:
        True if valid, raises ValueError if invalid
    """
    # Check required fields
    assert config.id, "Sport ID required"
    assert config.name, "Sport name required"
    assert config.field_length_m > 0, "Field length must be positive"
    assert config.field_width_m > 0, "Field width must be positive"
    assert config.players_per_team > 0, "Players per team must be positive"
    assert config.periods > 0, "Periods must be positive"
    assert config.period_duration_minutes > 0, "Period duration must be positive"
    
    return True


if __name__ == "__main__":
    # Test configurations
    print("🔍 Testing Sport Configurations...")
    print("-" * 60)
    
    # Test football config
    print(f"\n⚽ {FOOTBALL_CONFIG.name}")
    print(f"   Field: {FOOTBALL_CONFIG.field_length_m}m × {FOOTBALL_CONFIG.field_width_m}m")
    print(f"   Players: {FOOTBALL_CONFIG.players_per_team} per team")
    print(f"   Duration: {FOOTBALL_CONFIG.total_duration_minutes} minutes")
    print(f"   Zones: {len(FOOTBALL_ZONES)} defined")
    print(f"   Positions: {len(FOOTBALL_POSITIONS)} standard positions")
    print(f"   Events: {len(FOOTBALL_CONFIG.event_types)} event types")
    print(f"   Metrics: {len(FOOTBALL_CONFIG.key_metrics)} key metrics")
    validate_config(FOOTBALL_CONFIG)
    print("   ✅ Configuration valid")
    
    # Test Namibian stadiums
    print(f"\n🇳🇦 Namibian Stadiums: {len(NAMIBIAN_STADIUMS)} pre-configured")
    for stadium_id, stadium_info in NAMIBIAN_STADIUMS.items():
        print(f"   • {stadium_info['name']} ({stadium_info['location']})")
        print(f"     Capacity: {stadium_info['capacity']:,}, Lighting: {stadium_info['lighting']}")
    
    # Test helpers
    print(f"\n🔧 Helper Functions:")
    print(f"   get_sport_config('football'): {get_sport_config('football').name} ✅")
    print(f"   get_sport_zones('football'): {len(get_sport_zones('football'))} zones ✅")
    print(f"   list_supported_sports(): {list_supported_sports()} ✅")
    
    print("\n" + "="*60)
    print("✅ All configurations valid and ready!")
    print("="*60)
