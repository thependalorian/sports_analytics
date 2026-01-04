"""
LanceDB Migration Script
Location: /migrations/lancedb_migration.py
Purpose: Initialize LanceDB tables for sports analytics
Date: 2026-01-04
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from api.lib.lancedb_adapter import get_lancedb
from utils.logger import get_logger

logger = get_logger(__name__)

def create_lancedb_tables():
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
            {"name": "created_at", "type": "string"},
        ],
        "players": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "position", "type": "string"},
            {"name": "created_at", "type": "string"},
        ],
        "teams": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "competition", "type": "string"},
            {"name": "created_at", "type": "string"},
        ],
        "tournaments": [
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string"},
            {"name": "sport", "type": "string"},
            {"name": "status", "type": "string"},
            {"name": "created_at", "type": "string"},
        ]
    }
    
    # Create tables
    for table_name, schema in tables_schema.items():
        try:
            lancedb.create_table_if_not_exists(table_name, schema)
            logger.info(f"Table {table_name} ready")
        except Exception as e:
            logger.error(f"Failed to create table {table_name}: {e}")
    
    logger.info("LanceDB migration completed")

if __name__ == "__main__":
    create_lancedb_tables()

