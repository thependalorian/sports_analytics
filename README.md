# ⚽ Sports Analytics Pipeline

A comprehensive, **modular** football video analysis system powered by YOLO11x, ByteTrack, and advanced computer vision techniques. Built with a clean, maintainable architecture for research and production use.

**Repository:** [https://github.com/thependalorian/sports_analytics](https://github.com/thependalorian/sports_analytics)

## 🌟 Features

### Core Tracking & Detection
- **Player Detection & Tracking**: **YOLO11x-based detection** (54.7 mAP, 22% fewer parameters than YOLOv8) with ByteTrack for persistent IDs
- **Jersey Number Recognition**: EasyOCR-powered jersey number detection with validation (optimized for Namibian conditions)
- **Team Assignment**: Automatic team identification using LAB color space clustering
- **Ball Tracking**: Ball detection with trajectory interpolation
- **Referee Detection**: Automatic referee identification

### Advanced Analytics
- **Possession Analysis**: Frame-by-frame team possession tracking
- **Pass Detection**: Automatic pass detection with success/failure classification
- **Speed & Distance Tracking**: Player speed and distance covered calculations
- **Heatmap Generation**: Player and team position heatmaps
- **Event Detection**: Sprint detection, player clustering, ball trajectory changes
- **Commentary Generation**: Automated match commentary with timestamps
- **Statistics Engine**: Comprehensive player, team, and match statistics

### Visualizations
- **Pass Networks**: Visual representation of passing patterns
- **Zone Statistics**: Field zone occupancy heatmaps
- **Speed Overlays**: Real-time speed and distance visualization
- **Team Possession Stats**: Live possession percentage display

### Data Export
- **Tracking Data**: Comprehensive CSV export of all tracking data
- **Pass Statistics**: Detailed pass analysis with accuracy metrics
- **Event Logs**: Timestamped event detection logs
- **Player Statistics**: Per-player performance metrics
- **Match Reports**: Automated text-based match reports (CSV, JSON, TXT)

## 🏗️ Modular Architecture

This project follows a **modular design pattern** with clear separation of concerns:

### Core Modules (`analytics/`)
- `jersey_tracker.py` - Player tracking with jersey number detection
- `heatmap_generator.py` - Position heatmap generation
- `pass_detector.py` - Pass detection and analysis
- `commentary_generator.py` - Automated commentary generation
- `event_detector.py` - Event detection (sprints, clusters, etc.)
- `visualizations.py` - Pass networks and zone statistics
- `csv_exporter.py` - Data export utilities
- `statistics_engine.py` - Comprehensive statistics calculation

### Processing Modules
- `team_assigner/` - Team color clustering and assignment
- `player_ball_assigner/` - Ball possession assignment
- `camera_movement_estimator/` - Optical flow-based camera movement
- `view_transformer/` - Perspective transformation (pixel → field coordinates)
- `speed_and_distance_estimator/` - Speed and distance calculations

### Utility Modules (`utils/`)
- `video_utils.py` - Video reading, writing, and processing
- `bbox_utils.py` - Bounding box operations and calculations
- `field_mask.py` - Field boundary detection and filtering
- `jersey_detector.py` - Jersey number OCR detection
- `position_utils.py` - Position calculations and transformations
- `annotation_drawer.py` - Video annotation drawing
- `statistics_calculator.py` - Statistics calculation utilities
- `statistics_exporter.py` - Statistics export (CSV, JSON)
- `report_generator.py` - Text report generation
- `color_clustering.py` - Color extraction and clustering
- `optical_flow.py` - Optical flow tracking
- `speed_calculator.py` - Speed and distance calculations
- `frame_quality.py` - Frame quality assessment
- `color_utils.py` - Color space conversions

### Tools (`tools/`)
- `define_field_polygon.py` - Interactive field calibration tool

## 📁 Project Structure

```
sports_analytics/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── analyze_match.py                   # ⭐ Main pipeline (PRIMARY ENTRY POINT)
│
├── analytics/                         # Core analytics modules
│   ├── __init__.py
│   ├── jersey_tracker.py              # Player tracking & jersey detection
│   ├── heatmap_generator.py           # Heatmap generation
│   ├── pass_detector.py               # Pass detection
│   ├── commentary_generator.py        # Automated commentary
│   ├── event_detector.py              # Event detection
│   ├── visualizations.py              # Pass networks & zone stats
│   ├── csv_exporter.py                # Data export
│   └── statistics_engine.py           # Statistics calculation
│
├── team_assigner/                     # Team assignment module
│   ├── __init__.py
│   └── team_assigner.py               # Team color clustering
│
├── player_ball_assigner/              # Ball possession module
│   ├── __init__.py
│   └── player_ball_assigner.py       # Ball assignment
│
├── camera_movement_estimator/         # Camera movement module
│   ├── __init__.py
│   └── camera_movement_estimator.py   # Optical flow tracking
│
├── view_transformer/                  # Perspective transformation
│   ├── __init__.py
│   └── view_transformer.py            # Pixel → field coordinates
│
├── speed_and_distance_estimator/      # Speed/distance module
│   ├── __init__.py
│   └── speed_and_distance_estimator.py
│
├── utils/                             # Utility modules
│   ├── __init__.py
│   ├── video_utils.py                 # Video processing
│   ├── bbox_utils.py                  # Bounding box utilities
│   ├── field_mask.py                  # Field boundary detection
│   ├── jersey_detector.py              # Jersey number OCR
│   ├── position_utils.py              # Position calculations
│   ├── annotation_drawer.py           # Video annotations
│   ├── statistics_calculator.py       # Statistics calculation
│   ├── statistics_exporter.py         # Statistics export
│   ├── report_generator.py            # Report generation
│   ├── color_clustering.py            # Color extraction/clustering
│   ├── optical_flow.py                # Optical flow tracking
│   ├── speed_calculator.py            # Speed calculations
│   ├── frame_quality.py               # Frame quality assessment
│   ├── color_utils.py                 # Color space conversions
│   └── logger.py                      # Logging utility
│
├── tools/                             # Utility tools
│   └── define_field_polygon.py        # Field calibration tool
│
├── config/                            # Configuration files
│   ├── field_config.json              # Field calibration data
│   └── settings.py                    # Global settings and configuration
│
├── tests/                             # Unit and integration tests
│   ├── __init__.py
│   ├── test_bbox_utils.py             # Bbox utility tests
│   └── test_position_utils.py         # Position utility tests
│
├── notebooks/                         # Jupyter notebooks
│   └── (research and prototyping notebooks)
│
├── docs/                              # Documentation
│   └── architecture.md                # Architecture documentation
│
├── scripts/                           # Utility scripts
│   └── batch_process.py               # Batch video processing
│
├── data/                              # Sample datasets and calibration data
│   └── (sample datasets, calibration images)
│
├── models/                            # Model weights
│   └── best.pt                        # YOLOv8 model (to be added)
│
├── logs/                              # Log files
│   └── (generated log files)
│
├── input_videos/                      # Input video directory
└── output_videos/                     # Output directory
    ├── heatmaps/                      # Generated heatmaps
    └── visualizations/                # Visualization outputs
```

## 🚀 Quick Start

### Clone Repository

```bash
# Clone the repository
git clone https://github.com/thependalorian/sports_analytics.git
cd sports_analytics

# Install Git LFS (required for large model files)
git lfs install

# Pull large model files from LFS
git lfs pull
```

**Note:** This repository uses Git LFS for large model files (`.pth` and `.pt`). Make sure Git LFS is installed before cloning. See [Git LFS Installation](#git-lfs-setup) below.

### One-Command Setup (Recommended)

```bash
# Automated setup (handles everything)
python scripts/setup.py
```

This will:
1. ✅ Check Python version (3.8+ required)
2. ✅ Create virtual environment
3. ✅ Install dependencies (~5-10 minutes)
4. ✅ Download YOLO11x model (~110MB, 1-2 minutes on 4G)
5. ✅ Create all directories
6. ✅ Run tests
7. ✅ Show next steps

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download YOLO11x model
python scripts/download_models.py --download

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Download YOLO11x Model (Recommended)

**Automatic Download (Easy):**
```bash
python scripts/download_models.py --download
```

**From Repository (Git LFS):**
If you cloned the repository, the YOLO11x model is already included via Git LFS:
```bash
# Ensure Git LFS is installed and initialized
git lfs install
git lfs pull  # Downloads all LFS-tracked files
```

**Manual Download:**
- Download YOLO11x from: https://github.com/ultralytics/assets/releases/download/v8.1.0/yolo11x.pt
- Place in `models/yolo11x.pt`

**Why YOLO11x Over YOLOv8?**
- ✅ 54.7 mAP vs 53.9 mAP (1.5% better accuracy)
- ✅ 56.9M params vs 68M params (22% smaller, faster)
- ✅ Optimized for edge devices (Raspberry Pi 5 deployments)
- ✅ Latest 2024 release (improved architecture)

See `models/README.md` for detailed comparison and optimization tips.

### Field Calibration

Before analyzing a new video, calibrate the field coordinates:

```bash
python tools/define_field_polygon.py input_videos/your_match.mp4
```

**Instructions:**
1. Click on the four field corners in order: **bottom-left, top-left, top-right, bottom-right**
2. Press `r` to reset if needed
3. Press `s` to save the configuration
4. Press `q` to quit

The configuration will be saved to `config/field_config.json`.

### Basic Usage (Command Line) - RECOMMENDED

```bash
# Analyze a match (automatic end-to-end processing)
python analyze_match.py input_videos/match.mp4

# Specify model
python analyze_match.py input_videos/match.mp4 --model models/yolo11x.pt

# Custom output directory
python analyze_match.py input_videos/match.mp4 --output-dir results/match1/

# Skip video export (faster, data only)
python analyze_match.py input_videos/match.mp4 --no-video

# Debug mode (verbose logging)
python analyze_match.py input_videos/match.mp4 --log-level DEBUG
```

### Advanced Usage (Python API)

```python
from analyze_match import MatchAnalyzer

# Initialize analyzer
analyzer = MatchAnalyzer(
    model_path="models/yolo11x.pt",
    sport="football",
    confidence_threshold=0.5,
    enable_ocr=True,
    chunk_size=300
)

# Analyze video
results = analyzer.analyze_video(
    video_path="input_videos/match.mp4",
    output_dir="output_videos/match1/",
    export_video=True,
    export_data=True
)

# Access results
print(f"Passes: {results['passes']['total_passes']}")
print(f"Events: {results['events']}")
print(f"Players: {len(results['player_stats'])}")
```

### Modular Component Usage

```python
from analytics import JerseyTracker, HeatmapGenerator, PassDetector
from utils import read_video, save_video
from team_assigner import TeamAssigner
from view_transformer import ViewTransformer

# Read video
frames = read_video("input_videos/match.mp4")

# Initialize components
tracker = JerseyTracker("models/yolo11x.pt", field_config_path="config/field_config.json")
team_assigner = TeamAssigner(use_lab=True)
view_transformer = ViewTransformer()

# Process video
tracks = tracker.process_chunk(frames, chunk_idx=0)
# ... continue with analysis (see analyze_match.py for complete pipeline)
```

## 📊 Output Files

After running the analysis, you'll find outputs in `output_videos/`:

### Video
- `{video_name}_complete_analysis.mp4` - Annotated video with all visualizations

### CSV Data
- `tracking_data.csv` - Frame-by-frame tracking data
- `passes.csv` - All detected passes with metadata
- `events.csv` - Detected events (sprints, clusters, etc.)
- `jersey_mapping.csv` - Jersey number to track ID mapping
- `team_statistics.csv` - Team-level statistics
- `player_statistics.csv` - Player-level statistics
- `match_statistics.csv` - Overall match statistics
- `statistics.json` - Complete statistics in JSON format

### Reports
- `match_report.txt` - Comprehensive match report
- `commentary.csv` - Automated commentary log
- `statistics_report.txt` - Detailed statistics report

### Visualizations
- `heatmaps/team1_heatmap.png` - Team 1 position heatmap
- `heatmaps/team2_heatmap.png` - Team 2 position heatmap
- `heatmaps/all_players_heatmap.png` - Combined heatmap
- `heatmaps/players/` - Individual player heatmaps
- `visualizations/pass_network_team1.png` - Team 1 pass network
- `visualizations/pass_network_team2.png` - Team 2 pass network
- `visualizations/zones_team1.png` - Team 1 zone statistics
- `visualizations/zones_team2.png` - Team 2 zone statistics

## 🔧 API Documentation

### Core Analytics Modules

#### JerseyTracker
```python
from analytics import JerseyTracker

tracker = JerseyTracker(
    model_path="models/best.pt",
    field_config_path="config/field_config.json",
    video_name="match1",
    confidence_threshold=0.5,
    enable_ocr=True
)

# Process frames
tracks = tracker.process_chunk(frames, chunk_idx=0)

# Add positions
tracker.add_position_to_tracks(tracks)

# Interpolate ball positions
tracks['ball'] = tracker.interpolate_ball_positions(tracks['ball'])

# Draw annotations
annotated_frames = tracker.draw_annotations(frames, tracks, team_ball_control)

# Export jersey mapping
tracker.export_jersey_mapping("output_videos/jersey_mapping.csv")
```

#### HeatmapGenerator
```python
from analytics import HeatmapGenerator

heatmap_gen = HeatmapGenerator(
    field_dims=(105, 68),  # Field dimensions in meters
    resolution=(1050, 680)  # Heatmap resolution
)

# Accumulate positions
heatmap_gen.accumulate_positions(tracks)

# Generate heatmaps
heatmap_gen.generate_heatmap_images("output_videos/heatmaps/")
heatmap_gen.export_team_heatmaps("output_videos/heatmaps/")

# Get statistics
stats = heatmap_gen.get_heatmap_statistics()
```

#### PassDetector
```python
from analytics import PassDetector

pass_detector = PassDetector(
    min_possession_frames=5,
    max_pass_distance=50  # meters
)

# Process frames
for frame_num, frame_tracks in enumerate(tracks['players']):
    pass_detector.process_frame(frame_num, tracks, current_team)

# Get statistics
stats = pass_detector.get_pass_statistics()

# Export passes
pass_detector.export_passes_csv("output_videos/passes.csv")
```

#### StatisticsEngine
```python
from analytics import StatisticsEngine
import pandas as pd

stats_engine = StatisticsEngine()

# Calculate statistics
stats_engine.calculate_all_statistics(
    tracking_df=tracking_df,
    passes_df=passes_df,
    events_df=events_df,
    fps=30
)

# Export statistics
stats_engine.export_statistics_csv("output_videos/")
stats_engine.export_statistics_json("output_videos/statistics.json")
stats_engine.generate_statistics_report("output_videos/statistics_report.txt")

# Get specific statistics
player_stats = stats_engine.get_player_stats(track_id=10)
team_stats = stats_engine.get_team_stats(team=1)
```

### Configuration

#### Global Settings
```python
from config.settings import Settings

# Access settings
model_path = Settings.DEFAULT_MODEL_PATH
confidence = Settings.CONFIDENCE_THRESHOLD
fps = Settings.DEFAULT_FPS

# Load from file
Settings.load_from_file("config/settings.json")

# Save current settings
Settings.save_to_file("config/settings.json")

# Get all settings as dict
all_settings = Settings.get_dict()
```

### Logging

#### Logger Utility
```python
from utils.logger import get_logger, SportsAnalyticsLogger

# Setup logger
logger = SportsAnalyticsLogger.setup_logger(
    log_dir="logs",
    log_level=logging.INFO,
    log_to_file=True
)

# Use logger
logger.info("Processing video...")
logger.debug("Debug information")
logger.error("Error occurred")

# Get logger in any module
logger = get_logger(__name__)
logger.info("Module-specific logging")
```

### Utility Modules

#### Video Utilities
```python
from utils import read_video, save_video, get_video_properties

# Read video
frames = read_video("input_videos/match.mp4")

# Get video properties
props = get_video_properties("input_videos/match.mp4")
print(f"FPS: {props['fps']}, Duration: {props['duration_sec']}s")

# Save video
save_video("output_videos/annotated.mp4", frames, fps=30)
```

#### Bounding Box Utilities
```python
from utils import (
    get_center_of_bbox,
    get_foot_position,
    measure_distance,
    measure_xy_distance
)

bbox = [100, 200, 300, 400]

# Get center
center = get_center_of_bbox(bbox)  # (200, 300)

# Get foot position
foot = get_foot_position(bbox)  # (200, 400)

# Measure distance
distance = measure_distance((100, 100), (200, 200))  # 141.42
x_dist, y_dist = measure_xy_distance((100, 100), (200, 200))  # (-100, -100)
```

#### Color Clustering
```python
from utils.color_clustering import ColorExtractor, TeamColorClusterer

extractor = ColorExtractor(use_lab=True)
clusterer = TeamColorClusterer(use_lab=True)

# Extract colors
player_colors = []
for player in players:
    color = extractor.extract_jersey_color(frame, player['bbox'])
    if color:
        player_colors.append(color)

# Cluster into teams
clusterer.fit_teams(player_colors)
team = clusterer.predict_team(player_color)
```

## ⚙️ Configuration

### Field Configuration (`config/field_config.json`)

```json
{
  "video_name": {
    "pixel_vertices": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
    "court_length_m": 105,
    "court_width_m": 68
  },
  "default": {
    "pixel_vertices": [[...], [...], [...], [...]],
    "court_length_m": 105,
    "court_width_m": 68
  }
}
```

### Customization Parameters

```python
# Detection confidence threshold
tracker = JerseyTracker(model_path, confidence_threshold=0.5)

# Pass detection parameters
pass_detector = PassDetector(
    min_possession_frames=5,
    max_pass_distance=50  # meters
)

# Event detection parameters
event_detector = EventDetector(sprint_threshold=7.0)  # m/s

# Speed calculation
speed_estimator = SpeedAndDistanceEstimator(fps=30, window_size=5)

# Team assignment
team_assigner = TeamAssigner(use_lab=True)  # Use LAB color space

# Chunk size for processing
chunk_size = 300  # Process 300 frames at a time
```

## 🔧 Advanced Features

### Chunked Processing

The pipeline processes videos in chunks to manage memory efficiently:

```python
chunk_size = 300
for chunk_idx in range(0, len(frames), chunk_size):
    chunk = frames[chunk_idx:chunk_idx + chunk_size]
    tracks = tracker.process_chunk(chunk, chunk_idx)
    # Process chunk...
```

### Camera Movement Compensation

Uses optical flow to adjust positions for camera pan/tilt:

```python
from camera_movement_estimator import CameraMovementEstimator

camera_estimator = CameraMovementEstimator(frames[0])
camera_movement = camera_estimator.get_camera_movement(
    frames,
    read_from_stub=True,
    stub_path="cache/camera_movement.pkl"
)
camera_estimator.adjust_positions_to_tracks(tracks, camera_movement)
```

### Perspective Transformation

Converts pixel coordinates to real-world field coordinates:

```python
from view_transformer import ViewTransformer

transformer = ViewTransformer(
    pixel_vertices=[[x1, y1], [x2, y2], [x3, y3], [x4, y4]],
    court_length=105,
    court_width=68
)

# Transform positions
transformer.add_transformed_position_to_tracks(tracks)

# Transform single point
field_pos = transformer.transform_point((500, 300))  # Returns [x_m, y_m]
```

## 📈 Statistics & Metrics

### Team-Level Statistics
- Possession percentage
- Total distance covered (km)
- Average distance per player (km)
- Average speed (m/s)
- Maximum speed (m/s)
- Total passes
- Successful passes
- Pass accuracy percentage
- Sprint count

### Player-Level Statistics
- Distance covered (meters)
- Maximum speed (m/s, km/h)
- Average speed (m/s, km/h)
- Possession time (seconds)
- Possession percentage
- Passes made
- Passes received
- Successful passes
- Pass accuracy percentage
- Sprint count

### Match-Level Statistics
- Total duration (minutes)
- Total frames
- Ball in play percentage
- Total passes
- Successful passes
- Overall pass accuracy
- Average pass distance (meters)
- Longest pass (meters)
- Total events detected
- Total sprints
- Total clusters

## 🛠️ Troubleshooting

### Common Issues

**1. EasyOCR not detecting jersey numbers**
- Ensure good lighting in the video
- Players should be close enough to camera
- Check OCR confidence threshold settings
- Try adjusting `confidence_threshold` in `JerseyNumberDetector`

**2. Poor team assignment**
- Ensure teams have distinctly colored jerseys
- Adjust `use_lab` parameter in `TeamAssigner`
- Manually verify first frame team colors
- Check that enough players are visible in first frame

**3. Inaccurate speed calculations**
- Verify field calibration vertices are correct
- Check that field dimensions match actual field
- Ensure FPS is set correctly
- Verify perspective transformation is accurate

**4. Memory issues**
- Reduce `chunk_size` in processing loop
- Process shorter video clips
- Use a machine with more RAM
- Enable camera movement caching (stub files)

**5. Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the correct directory
- Verify Python version (3.8+)

## 📚 Module Dependencies

### Core Dependencies
- `ultralytics` - YOLOv8 object detection
- `opencv-python` - Computer vision operations
- `supervision` - ByteTrack tracking
- `numpy` - Numerical operations
- `pandas` - Data manipulation

### Optional Dependencies
- `easyocr` - Jersey number OCR (recommended)
- `scikit-learn` - KMeans clustering
- `matplotlib` - Visualization
- `seaborn` - Statistical visualization

## 🧪 Testing

Run tests using pytest:

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=utils --cov=analytics

# Run specific test file
pytest tests/test_bbox_utils.py

# Run with verbose output
pytest -v
```

## 📝 Development

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
pylint analytics/ utils/

# Type checking
mypy analytics/ utils/
```

### Batch Processing

Process multiple videos at once:

```bash
python scripts/batch_process.py --input-dir input_videos/ --pattern "*.mp4"
```

## 📦 Git LFS Setup

This repository uses **Git LFS (Large File Storage)** for model files to avoid GitHub's file size limitations.

### Installing Git LFS

**macOS:**
```bash
brew install git-lfs
git lfs install
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install git-lfs
git lfs install

# Or download from: https://git-lfs.github.com/
```

**Windows:**
```bash
# Using Chocolatey
choco install git-lfs
git lfs install

# Or download installer from: https://git-lfs.github.com/
```

### Cloning with LFS Files

```bash
# Clone repository
git clone https://github.com/thependalorian/sports_analytics.git
cd sports_analytics

# Pull LFS files (if not automatically downloaded)
git lfs pull
```

### Files Tracked by LFS

- `models/**/*.pth` - EasyOCR model files (~79 MB)
- `models/**/*.pt` - YOLO model files (e.g., `yolo11x.pt`)

These files are automatically handled by Git LFS when you clone or pull from the repository.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional event detection (shots, tackles, fouls, etc.)
- Formation analysis
- Tactical pattern recognition
- Real-time processing optimizations
- Integration with sports APIs
- Machine learning model improvements
- Performance optimizations
- Documentation improvements

## 📝 License

This project is provided as-is for educational and research purposes.

## 🙏 Acknowledgments

- **Ultralytics** for YOLOv8
- **Roboflow** for Supervision library (ByteTrack)
- **EasyOCR** team for OCR capabilities
- **OpenCV** community
- Football analytics research community

## 🌐 Web Dashboard (Coming Soon)

### Overview
A comprehensive web dashboard is planned to provide an interactive interface for viewing and analyzing match data. The dashboard will feature:

- **Interactive Visualizations**: Heatmaps, pass networks, and performance charts
- **Real-Time Processing**: Live status updates during video processing
- **Player & Team Analytics**: Detailed statistics and comparisons
- **Video Player**: Annotated video playback with event markers
- **Data Export**: Download analytics in multiple formats

### Architecture
- **Backend**: FastAPI REST API
- **Frontend**: Next.js 14 (React) or Streamlit for rapid prototyping
- **Database**: PostgreSQL for match data storage
- **Real-Time**: WebSocket support for live updates

### Documentation
- **[PRD (Product Requirements Document)](docs/PRD_WEB_DASHBOARD.md)** - Complete product specification
- **[API Documentation](docs/API_DOCUMENTATION.md)** - RESTful API reference
- **[Frontend Architecture](docs/FRONTEND_ARCHITECTURE.md)** - Frontend design and structure

### Quick Start (Planned)

**Backend API:**
```bash
cd api
uvicorn main:app --reload
```

**Frontend Dashboard:**
```bash
cd dashboard
npm install
npm run dev
```

### Features Roadmap

**Phase 1 (MVP):**
- Match upload and processing
- Player statistics display
- Basic visualizations (heatmaps, charts)
- CSV/JSON export

**Phase 2:**
- Real-time processing updates
- Advanced visualizations (pass networks, 3D movement)
- Team comparison tools
- Annotated video player

**Phase 3:**
- Machine learning insights
- Custom analytics builder
- Collaboration features
- Mobile app

See [PRD_WEB_DASHBOARD.md](docs/PRD_WEB_DASHBOARD.md) for complete details.

## 📧 Support

For questions, issues, or suggestions:
- **GitHub Issues:** [https://github.com/thependalorian/sports_analytics/issues](https://github.com/thependalorian/sports_analytics/issues)
- **Repository:** [https://github.com/thependalorian/sports_analytics](https://github.com/thependalorian/sports_analytics)
- Check existing documentation in `docs/` folder
- Review module docstrings: `help(ModuleName)`

---

**Built with ⚽ for football analytics enthusiasts**

*Modular • Scalable • Research-Grade*
