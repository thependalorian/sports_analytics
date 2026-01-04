#!/usr/bin/env python3
"""
Main Match Analysis Pipeline
Location: /sports_analytics/analyze_match.py
Purpose: Orchestrate end-to-end football match video analysis

This is the primary entry point for analyzing football match videos.
Coordinates all modules: detection, tracking, analytics, visualization, export.

Usage:
    python analyze_match.py input_videos/match.mp4
    python analyze_match.py input_videos/match.mp4 --output-dir output_videos/match1/
    python analyze_match.py input_videos/match.mp4 --model models/yolo11x.pt --sport football
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
import cv2
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Core imports
from config.settings import Settings
from utils.logger import get_logger, SportsAnalyticsLogger
from utils.video_utils import read_video, save_video, get_video_properties

# Analytics modules
from analytics import (
    JerseyTracker,
    HeatmapGenerator,
    PassDetector,
    EventDetector,
    CommentaryGenerator,
    VisualizationGenerator,
    CSVExporter,
    StatisticsEngine
)

# Processing modules
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement_estimator import CameraMovementEstimator
from view_transformer import ViewTransformer
from speed_and_distance_estimator import SpeedAndDistanceEstimator

logger = get_logger(__name__)


class MatchAnalyzer:
    """
    Main match analyzer - orchestrates entire pipeline
    Modular design for maintainability and extensibility
    """
    
    def __init__(
        self,
        model_path: str,
        sport: str = "football",
        field_config_path: Optional[str] = None,
        confidence_threshold: float = 0.5,
        enable_ocr: bool = True,
        chunk_size: int = 300
    ):
        """
        Initialize match analyzer
        
        Args:
            model_path: Path to YOLO model (yolo11x.pt or yolov8x.pt)
            sport: Sport type (football, basketball, rugby, etc.)
            field_config_path: Path to field calibration config
            confidence_threshold: YOLO detection confidence (0.0-1.0)
            enable_ocr: Enable jersey number recognition
            chunk_size: Frames per processing chunk (memory management)
        """
        self.sport = sport
        self.chunk_size = chunk_size
        
        logger.info(f"🚀 Initializing Match Analyzer for {sport}")
        logger.info(f"   Model: {model_path}")
        logger.info(f"   OCR: {'Enabled' if enable_ocr else 'Disabled'}")
        logger.info(f"   Chunk size: {chunk_size} frames")
        
        # Initialize all components
        self._initialize_components(
            model_path,
            field_config_path,
            confidence_threshold,
            enable_ocr
        )
    
    def _initialize_components(
        self,
        model_path: str,
        field_config_path: Optional[str],
        confidence_threshold: float,
        enable_ocr: bool
    ):
        """Initialize all processing components"""
        
        logger.info("📦 Loading components...")
        
        # Core tracker
        self.tracker = JerseyTracker(
            model_path=model_path,
            field_config_path=field_config_path,
            confidence_threshold=confidence_threshold,
            enable_ocr=enable_ocr
        )
        
        # Team assignment
        self.team_assigner = TeamAssigner(use_lab=True)
        
        # Ball possession
        self.ball_assigner = PlayerBallAssigner(max_distance=70)
        
        # Camera movement
        self.camera_estimator = None  # Lazy init with first frame
        
        # View transformation
        self.view_transformer = None  # Lazy init with field config
        
        # Speed & distance
        self.speed_estimator = SpeedAndDistanceEstimator(
            fps=Settings.DEFAULT_FPS,
            window_size=Settings.SPEED_WINDOW_SIZE
        )
        
        # Analytics
        self.heatmap_gen = HeatmapGenerator(
            field_dims=(Settings.FIELD_LENGTH_M, Settings.FIELD_WIDTH_M),
            resolution=Settings.HEATMAP_RESOLUTION
        )
        
        self.pass_detector = PassDetector(
            min_possession_frames=Settings.MIN_POSSESSION_FRAMES,
            max_pass_distance=Settings.MAX_PASS_DISTANCE
        )
        
        self.event_detector = EventDetector(
            sprint_threshold=Settings.SPRINT_THRESHOLD
        )
        
        self.commentary_gen = CommentaryGenerator()
        
        # Visualization
        self.viz_gen = VisualizationGenerator()
        
        # Export & statistics
        self.csv_exporter = CSVExporter()
        self.stats_engine = StatisticsEngine()
        
        logger.info("✅ All components loaded")
    
    def analyze_video(
        self,
        video_path: str,
        output_dir: Optional[str] = None,
        export_video: bool = True,
        export_data: bool = True
    ) -> Dict:
        """
        Analyze complete match video
        
        Args:
            video_path: Path to input video
            output_dir: Output directory (default: output_videos/{video_name}/)
            export_video: Whether to export annotated video
            export_data: Whether to export CSVs, JSON, reports
            
        Returns:
            Dictionary with analysis results and statistics
        """
        start_time = time.time()
        
        # Setup output directory
        video_path = Path(video_path)
        video_name = video_path.stem
        
        if output_dir is None:
            output_dir = Settings.OUTPUT_VIDEOS_DIR / video_name
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"📹 Analyzing: {video_name}")
        logger.info(f"   Input: {video_path}")
        logger.info(f"   Output: {output_dir}")
        
        # Read video
        logger.info("📖 Reading video...")
        frames = read_video(str(video_path))
        video_props = get_video_properties(str(video_path))
        fps = video_props['fps']
        
        logger.info(f"   Frames: {len(frames)}, FPS: {fps}, Duration: {video_props['duration_sec']:.1f}s")
        
        # Initialize lazy components
        if self.camera_estimator is None:
            self.camera_estimator = CameraMovementEstimator(frames[0])
        
        # Process video in chunks
        logger.info(f"🔄 Processing {len(frames)} frames in chunks of {self.chunk_size}...")
        
        all_tracks = {"players": [], "ball": [], "referees": []}
        
        for chunk_idx in range(0, len(frames), self.chunk_size):
            chunk_end = min(chunk_idx + self.chunk_size, len(frames))
            chunk = frames[chunk_idx:chunk_end]
            
            logger.info(f"   Chunk {chunk_idx // self.chunk_size + 1}: Frames {chunk_idx}-{chunk_end}")
            
            # Detect & track
            tracks = self.tracker.process_chunk(chunk, chunk_idx=chunk_idx)
            
            # Append to all tracks
            all_tracks['players'].extend(tracks['players'])
            all_tracks['ball'].extend(tracks['ball'])
            all_tracks['referees'].extend(tracks['referees'])
        
        logger.info(f"✅ Detection & tracking complete")
        
        # Assign teams (first frame with most players)
        logger.info("🎽 Assigning teams...")
        first_frame_with_players = self._find_frame_with_most_players(all_tracks, frames)
        if first_frame_with_players >= 0:
            player_detections = all_tracks['players'][first_frame_with_players]
            self.team_assigner.assign_team_color(frames[first_frame_with_players], player_detections)
        
        # Assign teams to all players
        for frame_idx, frame_tracks in enumerate(all_tracks['players']):
            for player_id, player_info in frame_tracks.items():
                bbox = player_info.get('bbox', [])
                if bbox and len(bbox) == 4:
                    team = self.team_assigner.get_player_team(frames[frame_idx], bbox, player_id)
                    player_info['team'] = team
        
        logger.info("✅ Team assignment complete")
        
        # Camera movement compensation
        logger.info("🎥 Estimating camera movement...")
        camera_movement = self.camera_estimator.get_camera_movement(
            frames,
            read_from_stub=True,
            stub_path=str(output_dir / "camera_movement.pkl")
        )
        self.camera_estimator.adjust_positions_to_tracks(all_tracks, camera_movement)
        logger.info("✅ Camera compensation complete")
        
        # Perspective transformation
        logger.info("🗺️  Transforming perspective...")
        if self.tracker.field_mask.config:
            # Use field config from tracker
            config = self.tracker.field_mask.config
            self.view_transformer = ViewTransformer(
                pixel_vertices=config['pixel_vertices'],
                court_length=config.get('court_length_m', Settings.FIELD_LENGTH_M),
                court_width=config.get('court_width_m', Settings.FIELD_WIDTH_M)
            )
            self.view_transformer.add_transformed_position_to_tracks(all_tracks)
            logger.info("✅ Perspective transformation complete")
        else:
            logger.warning("⚠️  No field config - skipping perspective transformation")
        
        # Interpolate ball positions
        logger.info("⚽ Interpolating ball positions...")
        all_tracks['ball'] = self.tracker.interpolate_ball_positions(all_tracks['ball'])
        
        # Ball assignment
        logger.info("🤾 Assigning ball possession...")
        team_ball_control = []
        for frame_idx, frame_tracks in enumerate(all_tracks['players']):
            ball_data = all_tracks['ball'][frame_idx] if frame_idx < len(all_tracks['ball']) else {}
            ball_bbox = ball_data.get(1, {}).get('bbox', []) if ball_data else []
            
            if ball_bbox and len(ball_bbox) == 4:
                assigned_player = self.ball_assigner.assign_ball_to_player(frame_tracks, ball_bbox)
                
                if assigned_player != -1 and assigned_player in frame_tracks:
                    frame_tracks[assigned_player]['has_ball'] = True
                    team = frame_tracks[assigned_player].get('team', 1)
                else:
                    team = team_ball_control[-1] if team_ball_control else 1
            else:
                team = team_ball_control[-1] if team_ball_control else 1
            
            team_ball_control.append(team)
        
        logger.info("✅ Ball assignment complete")
        
        # Speed & distance
        logger.info("⚡ Calculating speed & distance...")
        self.speed_estimator.add_speed_and_distance_to_tracks(all_tracks, fps=fps)
        logger.info("✅ Speed & distance complete")
        
        # Pass detection
        logger.info("🎯 Detecting passes...")
        for frame_idx in range(len(all_tracks['players'])):
            current_team = team_ball_control[frame_idx] if frame_idx < len(team_ball_control) else 1
            frame_tracks_dict = {
                'players': [all_tracks['players'][frame_idx]] if frame_idx < len(all_tracks['players']) else [{}],
                'ball': [all_tracks['ball'][frame_idx]] if frame_idx < len(all_tracks['ball']) else [{}]
            }
            self.pass_detector.process_frame(frame_idx, frame_tracks_dict, current_team)
        
        pass_stats = self.pass_detector.get_pass_statistics()
        logger.info(f"✅ Pass detection complete: {pass_stats['total_passes']} passes detected")
        
        # Event detection
        logger.info("🔔 Detecting events...")
        events = self.event_detector.detect_events(all_tracks, fps=fps)
        logger.info(f"✅ Event detection complete: {len(events)} events detected")
        
        # Heatmap generation
        logger.info("🗺️  Generating heatmaps...")
        self.heatmap_gen.accumulate_positions(all_tracks)
        heatmap_dir = output_dir / "heatmaps"
        heatmap_dir.mkdir(exist_ok=True)
        self.heatmap_gen.generate_heatmap_images(str(heatmap_dir))
        self.heatmap_gen.export_team_heatmaps(str(heatmap_dir))
        logger.info(f"✅ Heatmaps saved to {heatmap_dir}")
        
        # Commentary generation
        logger.info("📝 Generating commentary...")
        commentary = self.commentary_gen.generate_commentary(all_tracks, events, pass_stats, fps=fps)
        self.commentary_gen.export_commentary_csv(str(output_dir / "commentary.csv"))
        logger.info(f"✅ Commentary generated: {len(commentary)} entries")
        
        # Export data
        if export_data:
            logger.info("💾 Exporting data...")
            
            # CSV exports
            self.csv_exporter.export_tracking_data(all_tracks, str(output_dir / "tracking_data.csv"))
            self.pass_detector.export_passes_csv(str(output_dir / "passes.csv"))
            self.event_detector.export_events_csv(events, str(output_dir / "events.csv"))
            self.tracker.export_jersey_mapping(str(output_dir / "jersey_mapping.csv"))
            
            # Statistics calculation
            logger.info("📊 Calculating statistics...")
            import pandas as pd
            
            # Convert tracking to DataFrame
            tracking_data = self._convert_tracks_to_dataframe(all_tracks, fps)
            passes_df = pd.DataFrame(self.pass_detector.passes) if self.pass_detector.passes else pd.DataFrame()
            events_df = pd.DataFrame(events) if events else pd.DataFrame()
            
            self.stats_engine.calculate_all_statistics(tracking_data, passes_df, events_df, fps)
            
            # Export statistics
            self.stats_engine.export_statistics_csv(str(output_dir))
            self.stats_engine.export_statistics_json(str(output_dir / "statistics.json"))
            self.stats_engine.generate_statistics_report(str(output_dir / "statistics_report.txt"))
            
            # Visualizations
            logger.info("📈 Generating visualizations...")
            viz_dir = output_dir / "visualizations"
            viz_dir.mkdir(exist_ok=True)
            
            # Pass networks
            self.viz_gen.generate_pass_network(
                self.pass_detector.passes,
                team=1,
                output_path=str(viz_dir / "pass_network_team1.png")
            )
            self.viz_gen.generate_pass_network(
                self.pass_detector.passes,
                team=2,
                output_path=str(viz_dir / "pass_network_team2.png")
            )
            
            # Zone statistics
            self.viz_gen.generate_zone_statistics(
                all_tracks,
                team=1,
                output_path=str(viz_dir / "zones_team1.png")
            )
            self.viz_gen.generate_zone_statistics(
                all_tracks,
                team=2,
                output_path=str(viz_dir / "zones_team2.png")
            )
            
            logger.info(f"✅ Data exported to {output_dir}")
        
        # Export annotated video
        if export_video:
            logger.info("🎬 Creating annotated video...")
            annotated_frames = self.tracker.draw_annotations(frames, all_tracks, team_ball_control)
            
            output_video_path = output_dir / f"{video_path.stem}_complete_analysis.mp4"
            save_video(str(output_video_path), annotated_frames, fps=fps)
            logger.info(f"✅ Annotated video saved: {output_video_path}")
        
        # Analysis complete
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        logger.info(f"")
        logger.info(f"🎉 Analysis Complete!")
        logger.info(f"   Duration: {minutes}m {seconds}s")
        logger.info(f"   Output: {output_dir}")
        
        # Return summary
        return {
            'video_name': video_path.stem,
            'frames_processed': len(frames),
            'duration_seconds': elapsed_time,
            'passes': pass_stats,
            'events': len(events),
            'player_stats': self.stats_engine.get_player_stats(),
            'team_stats': self.stats_engine.get_team_stats(),
            'output_directory': str(output_dir)
        }
    
    def _find_frame_with_most_players(self, tracks: Dict, frames: List[np.ndarray]) -> int:
        """
        Find frame with most player detections (for team assignment)
        
        Args:
            tracks: Tracking data
            frames: Video frames
            
        Returns:
            Frame index with most players, or -1 if none
        """
        max_players = 0
        best_frame = -1
        
        # Check first 30 seconds (900 frames at 30fps)
        search_frames = min(900, len(tracks['players']))
        
        for frame_idx in range(0, search_frames, 30):  # Sample every 30 frames
            if frame_idx < len(tracks['players']):
                player_count = len(tracks['players'][frame_idx])
                if player_count > max_players:
                    max_players = player_count
                    best_frame = frame_idx
        
        return best_frame
    
    def _convert_tracks_to_dataframe(self, tracks: Dict, fps: float) -> 'pd.DataFrame':
        """
        Convert tracking data to pandas DataFrame for statistics
        
        Args:
            tracks: Tracking dictionary
            fps: Video frames per second
            
        Returns:
            DataFrame with tracking data
        """
        import pandas as pd
        
        rows = []
        
        for frame_idx, frame_tracks in enumerate(tracks['players']):
            for player_id, player_info in frame_tracks.items():
                row = {
                    'frame': frame_idx,
                    'timestamp': frame_idx / fps,
                    'player_id': player_id,
                    'team': player_info.get('team', 1),
                    'jersey_number': player_info.get('jersey_number', ''),
                    'bbox_x1': player_info.get('bbox', [0, 0, 0, 0])[0],
                    'bbox_y1': player_info.get('bbox', [0, 0, 0, 0])[1],
                    'bbox_x2': player_info.get('bbox', [0, 0, 0, 0])[2],
                    'bbox_y2': player_info.get('bbox', [0, 0, 0, 0])[3],
                    'position_x': player_info.get('position', [0, 0])[0],
                    'position_y': player_info.get('position', [0, 0])[1],
                    'position_transformed_x': player_info.get('position_transformed', [0, 0])[0],
                    'position_transformed_y': player_info.get('position_transformed', [0, 0])[1],
                    'speed_mps': player_info.get('speed', 0),
                    'distance_m': player_info.get('distance', 0),
                    'has_ball': player_info.get('has_ball', False)
                }
                rows.append(row)
        
        return pd.DataFrame(rows)


def main():
    """Main function - CLI interface"""
    
    parser = argparse.ArgumentParser(
        description="⚽ Football Match Video Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_match.py input_videos/match.mp4
  python analyze_match.py input_videos/match.mp4 --model models/yolo11x.pt
  python analyze_match.py input_videos/match.mp4 --output-dir results/match1/ --no-video
  python analyze_match.py input_videos/match.mp4 --sport football --confidence 0.6
        """
    )
    
    parser.add_argument(
        "video",
        type=str,
        help="Path to input video file"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default=str(Settings.DEFAULT_MODEL_PATH),
        help=f"Path to YOLO model (default: {Settings.DEFAULT_MODEL_PATH})"
    )
    
    parser.add_argument(
        "--sport",
        type=str,
        default="football",
        choices=["football", "basketball", "rugby", "netball", "hockey", "cricket", "tennis", "volleyball"],
        help="Sport type (default: football)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: output_videos/{video_name}/)"
    )
    
    parser.add_argument(
        "--field-config",
        type=str,
        default=str(Settings.FIELD_CONFIG_PATH),
        help=f"Field calibration config (default: {Settings.FIELD_CONFIG_PATH})"
    )
    
    parser.add_argument(
        "--confidence",
        type=float,
        default=Settings.CONFIDENCE_THRESHOLD,
        help=f"Detection confidence threshold (default: {Settings.CONFIDENCE_THRESHOLD})"
    )
    
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=Settings.CHUNK_SIZE,
        help=f"Frames per processing chunk (default: {Settings.CHUNK_SIZE})"
    )
    
    parser.add_argument(
        "--no-ocr",
        action="store_true",
        help="Disable jersey number recognition (faster)"
    )
    
    parser.add_argument(
        "--no-video",
        action="store_true",
        help="Skip annotated video export (faster)"
    )
    
    parser.add_argument(
        "--no-data",
        action="store_true",
        help="Skip CSV/JSON export"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default=Settings.LOG_LEVEL,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help=f"Logging level (default: {Settings.LOG_LEVEL})"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    import logging
    SportsAnalyticsLogger.setup_logger(
        log_dir=str(Settings.LOGS_DIR),
        log_level=getattr(logging, args.log_level),
        log_to_file=True
    )
    
    # Validate input
    if not Path(args.video).exists():
        logger.error(f"❌ Video file not found: {args.video}")
        sys.exit(1)
    
    if not Path(args.model).exists():
        logger.error(f"❌ Model file not found: {args.model}")
        logger.error(f"   Download YOLO11x: https://github.com/ultralytics/assets/releases")
        logger.error(f"   Place it in: models/yolo11x.pt")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = MatchAnalyzer(
        model_path=args.model,
        sport=args.sport,
        field_config_path=args.field_config,
        confidence_threshold=args.confidence,
        enable_ocr=not args.no_ocr,
        chunk_size=args.chunk_size
    )
    
    # Analyze video
    try:
        results = analyzer.analyze_video(
            video_path=args.video,
            output_dir=args.output_dir,
            export_video=not args.no_video,
            export_data=not args.no_data
        )
        
        # Print summary
        print("\n" + "="*60)
        print("📊 ANALYSIS SUMMARY")
        print("="*60)
        print(f"Video: {results['video_name']}")
        print(f"Frames: {results['frames_processed']}")
        print(f"Duration: {results['duration_seconds']:.1f}s")
        print(f"\nPasses: {results['passes']['total_passes']}")
        print(f"  Team 1: {results['passes']['team1_passes']} ({results['passes']['team1_accuracy']:.1f}% accuracy)")
        print(f"  Team 2: {results['passes']['team2_passes']} ({results['passes']['team2_accuracy']:.1f}% accuracy)")
        print(f"\nEvents: {results['events']}")
        print(f"\nPlayers: {len(results['player_stats'])}")
        print(f"Teams: {len(results['team_stats'])}")
        print(f"\nOutput: {results['output_directory']}")
        print("="*60)
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
