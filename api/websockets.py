"""
WebSocket Handlers
Location: /api/websockets.py
Purpose: WebSocket endpoints for real-time updates
"""

from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, List
import json
from uuid import UUID

from api.database import get_db
from api.models.match import Match
from utils.logger import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    """WebSocket connection manager"""
    
    def __init__(self):
        self.active_connections: Dict[UUID, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, match_id: UUID):
        """Connect client to match room"""
        await websocket.accept()
        if match_id not in self.active_connections:
            self.active_connections[match_id] = []
        self.active_connections[match_id].append(websocket)
        logger.info(f"Client connected to match {match_id}")
    
    def disconnect(self, websocket: WebSocket, match_id: UUID):
        """Disconnect client from match room"""
        if match_id in self.active_connections:
            self.active_connections[match_id].remove(websocket)
            if not self.active_connections[match_id]:
                del self.active_connections[match_id]
        logger.info(f"Client disconnected from match {match_id}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client"""
        await websocket.send_text(message)
    
    async def broadcast_to_match(self, message: dict, match_id: UUID):
        """Broadcast message to all clients in match room"""
        if match_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[match_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.error(f"Error sending message: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                self.disconnect(connection, match_id)

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, match_id: UUID):
    """
    WebSocket endpoint for real-time match updates
    
    Usage:
        ws://api.sportsvision.na/api/v1/matches/{match_id}/stream
    """
    await manager.connect(websocket, match_id)
    
    try:
        while True:
            # Receive messages from client (optional)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle client messages (e.g., subscribe to specific events)
            if message.get("type") == "subscribe":
                logger.info(f"Client subscribed to {message.get('events')}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, match_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket, match_id)

