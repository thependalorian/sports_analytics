"""
FastAPI Main Application
Location: /api/main.py
Purpose: FastAPI application entry point with all routes and middleware
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import sys
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from api.dependencies import get_settings
from api.routers import (
    auth,
    matches,
    players,
    teams,
    tournaments,
    scouting,
    payments,
    notifications,
    sync,
    user,
    settings as settings_router,
    unam,
    analytics,
    export
)
from api.middleware import RequestLoggingMiddleware, RateLimitMiddleware
from api.websockets import websocket_endpoint
from fastapi import WebSocket
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Sports Analytics API",
    description="Sports Analytics Web Dashboard API - Namibian Market",
    version="2.1.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# CORS Middleware (Namibian market optimization)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour (reduce 3G requests)
)

# Compression Middleware (80% size reduction for 3G)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom Middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(matches.router, prefix="/api/v1/matches", tags=["Matches"])
app.include_router(players.router, prefix="/api/v1/players", tags=["Players"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(tournaments.router, prefix="/api/v1/tournaments", tags=["Tournaments"])
app.include_router(scouting.router, prefix="/api/v1/scouting", tags=["Scouting"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(sync.router, prefix="/api/v1/sync", tags=["Sync"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(settings_router.router, prefix="/api/v1/settings", tags=["Settings"])
app.include_router(unam.router, prefix="/api/v1/unam", tags=["UNAM"])
app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])
app.include_router(export.router, prefix="/api/v1", tags=["Export"])

# WebSocket endpoint for real-time updates
@app.websocket("/api/v1/matches/{match_id}/stream")
async def match_stream(websocket: WebSocket, match_id: str):
    """WebSocket endpoint for real-time match updates"""
    from uuid import UUID
    try:
        match_uuid = UUID(match_id)
        await websocket_endpoint(websocket, match_uuid)
    except ValueError:
        await websocket.close(code=1008, reason="Invalid match ID")

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sports Analytics API",
        "version": "2.1.0",
        "market": "Namibia",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from api.database import engine
    from api.lib.lancedb_adapter import get_lancedb
    from sqlalchemy import text
    
    db_status = "unknown"
    lancedb_status = "unknown"
    
    # Check SQLAlchemy database
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
        logger.error(f"Database health check failed: {e}")
    
    # Check LanceDB
    try:
        lancedb = get_lancedb()
        lancedb_health = lancedb.health_check()
        lancedb_status = lancedb_health.get("status", "unknown")
    except Exception as e:
        lancedb_status = f"error: {str(e)}"
        logger.error(f"LanceDB health check failed: {e}")
    
    overall_status = "healthy" if db_status == "connected" and lancedb_status == "healthy" else "degraded"
    
    return {
        "status": overall_status,
        "environment": settings.ENVIRONMENT,
        "database": {
            "sqlalchemy": db_status,
            "lancedb": lancedb_status
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred",
                "details": {}
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )

