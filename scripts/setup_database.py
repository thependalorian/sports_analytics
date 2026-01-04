"""
Database Setup Script
Location: /scripts/setup_database.py
Purpose: Initialize LanceDB tables and run migrations
Date: 2026-01-04
"""

import sys
from pathlib import Path
import os

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set up minimal logging to avoid video_utils import issues
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock video_utils to avoid cv2 dependency for database setup
import types
sys.modules['utils.video_utils'] = types.ModuleType('video_utils')
sys.modules['utils.bbox_utils'] = types.ModuleType('bbox_utils')
sys.modules['utils.field_mask'] = types.ModuleType('field_mask')
sys.modules['utils.jersey_detector'] = types.ModuleType('jersey_detector')
sys.modules['utils.position_utils'] = types.ModuleType('position_utils')
sys.modules['utils.annotation_drawer'] = types.ModuleType('annotation_drawer')
sys.modules['utils.statistics_calculator'] = types.ModuleType('statistics_calculator')
sys.modules['utils.statistics_exporter'] = types.ModuleType('statistics_exporter')
sys.modules['utils.report_generator'] = types.ModuleType('report_generator')
sys.modules['utils.color_clustering'] = types.ModuleType('color_clustering')
sys.modules['utils.optical_flow'] = types.ModuleType('optical_flow')
sys.modules['utils.speed_calculator'] = types.ModuleType('speed_calculator')
sys.modules['utils.frame_quality'] = types.ModuleType('frame_quality')
sys.modules['utils.color_utils'] = types.ModuleType('color_utils')

from api.lib.lancedb_adapter import get_lancedb

# Logger is already set up above

def setup_lancedb_tables():
    """Create all LanceDB tables"""
    lancedb = get_lancedb()
    
    # Define table schemas
    tables_schema = {
        "users": [
            {"name": "id", "type": "string"},
            {"name": "email", "type": "string"},
            {"name": "full_name", "type": "string"},
            {"name": "organization", "type": "string"},
            {"name": "campus", "type": "string"},
            {"name": "created_at", "type": "string"},
        ],
        "matches": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "date", "type": "string"},
            {"name": "status", "type": "string"},
            {"name": "team1_name", "type": "string"},
            {"name": "team2_name", "type": "string"},
            {"name": "score_team1", "type": "int"},
            {"name": "score_team2", "type": "int"},
            {"name": "created_at", "type": "string"},
        ],
        "players": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "position", "type": "string"},
            {"name": "jersey_number", "type": "int"},
            {"name": "created_at", "type": "string"},
        ],
        "teams": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "competition", "type": "string"},
            {"name": "location", "type": "string"},
            {"name": "created_at", "type": "string"},
        ],
        "tournaments": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "status", "type": "string"},
            {"name": "organizer", "type": "string"},
            {"name": "created_at", "type": "string"},
        ],
        "player_statistics": [
            {"name": "id", "type": "string"},
            {"name": "player_id", "type": "string"},
            {"name": "match_id", "type": "string"},
            {"name": "total_distance_m", "type": "float"},
            {"name": "avg_speed_kmh", "type": "float"},
            {"name": "passes_made", "type": "int"},
            {"name": "pass_accuracy_pct", "type": "float"},
            {"name": "created_at", "type": "string"},
        ]
    }
    
    # Create tables
    created_count = 0
    for table_name, schema in tables_schema.items():
        try:
            lancedb.create_table_if_not_exists(table_name, schema)
            created_count += 1
            logger.info(f"✅ Table '{table_name}' ready")
        except Exception as e:
            logger.error(f"❌ Failed to create table {table_name}: {e}")
    
    # Register all tables for DuckDB
    try:
        lancedb.register_all_tables()
        logger.info("✅ All tables registered with DuckDB")
    except Exception as e:
        logger.warning(f"⚠️ DuckDB registration warning: {e}")
    
    # Health check
    health = lancedb.health_check()
    logger.info(f"📊 Database Health: {health.get('status')}")
    logger.info(f"📊 Tables: {health.get('tables_count', 0)}")
    
    return created_count

if __name__ == "__main__":
    print("🚀 Setting up LanceDB database...")
    count = setup_lancedb_tables()
    print(f"✅ Setup complete! {count} tables ready.")
    print("\n📝 Next steps:")
    print("   1. Start FastAPI: uvicorn api.main:app --reload")
    print("   2. Start Streamlit: streamlit run streamlit_app.py")

