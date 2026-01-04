"""
Database Connection and Session Management
Location: /api/database.py
Purpose: SQLAlchemy database setup and session management
Database: PostgreSQL (Neon Serverless compatible)
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
import logging
from contextlib import contextmanager

# Use standard logging to avoid video_utils dependency
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Database URL from environment (optional - we use LanceDB as primary)
DATABASE_URL = os.getenv("DATABASE_URL", None)

# SQLAlchemy engine and session (lazy initialization - only if DATABASE_URL is set)
engine = None
SessionLocal = None

def _init_sqlalchemy():
    """Lazy initialization of SQLAlchemy engine (only if DATABASE_URL is provided)"""
    global engine, SessionLocal
    
    if engine is not None:
        return  # Already initialized
    
    if not DATABASE_URL:
        logger.info("SQLAlchemy not initialized - using LanceDB only")
        return
    
    try:
        # For Neon Serverless, use HTTP driver
        if "neon.tech" in DATABASE_URL or "neon" in DATABASE_URL.lower():
            try:
                from neon import neon
                logger.info("Using Neon serverless database")
            except ImportError:
                logger.warning("Neon driver not installed, using standard PostgreSQL")
        
        # Create engine
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=10,
            max_overflow=20,
            echo=os.getenv("SQL_ECHO", "False").lower() == "true"
        )
        
        # Session factory
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("SQLAlchemy engine initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize SQLAlchemy engine: {e}. Using LanceDB only.")
        engine = None
        SessionLocal = None

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI (SQLAlchemy)
    Note: This is deprecated - use LanceDBAdapter from dependencies.get_db() instead
    
    Yields:
        Database session
    """
    _init_sqlalchemy()
    if SessionLocal is None:
        raise RuntimeError("SQLAlchemy not available. Use LanceDBAdapter instead.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Database session context manager (SQLAlchemy)
    Note: This is deprecated - use LanceDBAdapter instead
    
    Yields:
        Database session
    """
    _init_sqlalchemy()
    if SessionLocal is None:
        raise RuntimeError("SQLAlchemy not available. Use LanceDBAdapter instead.")
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize database (create tables) - SQLAlchemy only"""
    _init_sqlalchemy()
    if engine is None:
        logger.warning("SQLAlchemy not available. Use LanceDB migrations instead.")
        return
    from api.models import (  # noqa: F401
        user, match, player, team, tournament,
        scouting, payment, notification, sync
    )
    Base.metadata.create_all(bind=engine)
    logger.info("SQLAlchemy database initialized")

def drop_db():
    """Drop all database tables (use with caution!) - SQLAlchemy only"""
    _init_sqlalchemy()
    if engine is None:
        logger.warning("SQLAlchemy not available.")
        return
    Base.metadata.drop_all(bind=engine)
    logger.warning("All SQLAlchemy database tables dropped")

