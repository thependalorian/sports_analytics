"""
Batch Processing Script
Process multiple videos in batch
"""

import os
import sys
import argparse
from pathlib import Path
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import get_logger
from config.settings import Settings

logger = get_logger(__name__)


def batch_process_videos(input_dir, output_dir=None, pattern="*.mp4"):
    """
    Process multiple videos in batch
    
    Args:
        input_dir: Directory containing input videos
        output_dir: Output directory (default: output_videos/)
        pattern: File pattern to match (default: *.mp4)
    """
    from glob import glob
    
    if output_dir is None:
        output_dir = Settings.OUTPUT_VIDEOS_DIR
    
    input_path = Path(input_dir)
    video_files = list(input_path.glob(pattern))
    
    if not video_files:
        logger.warning(f"No videos found matching pattern '{pattern}' in {input_dir}")
        return
    
    logger.info(f"Found {len(video_files)} videos to process")
    
    for video_file in tqdm(video_files, desc="Processing videos"):
        logger.info(f"Processing: {video_file.name}")
        
        try:
            # Import here to avoid circular imports
            # This would call your main analysis function
            # from analyze_match import analyze_video
            
            # analyze_video(str(video_file), output_dir)
            logger.info(f"✓ Completed: {video_file.name}")
        
        except Exception as e:
            logger.error(f"✗ Failed to process {video_file.name}: {e}")
            continue
    
    logger.info("Batch processing complete")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Batch process sports analytics videos")
    parser.add_argument(
        "--input-dir",
        type=str,
        default=str(Settings.INPUT_VIDEOS_DIR),
        help="Input directory containing videos"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: output_videos/)"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*.mp4",
        help="File pattern to match (default: *.mp4)"
    )
    
    args = parser.parse_args()
    
    # Setup logger
    from utils.logger import SportsAnalyticsLogger
    SportsAnalyticsLogger.setup_logger(
        log_dir=str(Settings.LOGS_DIR),
        log_level=getattr(logging, Settings.LOG_LEVEL),
        log_to_file=Settings.LOG_TO_FILE
    )
    
    batch_process_videos(args.input_dir, args.output_dir, args.pattern)


if __name__ == "__main__":
    main()

