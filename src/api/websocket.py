"""
WebSocket support for real-time updates with JWT authentication
"""
from fastapi import WebSocket, WebSocketDisconnect, status
from typing import Dict, List, Set, Optional
import json
import asyncio
from loguru import logger
from jose import jwt, JWTError
from config.settings import settings


class ConnectionManager:
    """
    WebSocket connection manager for broadcasting updates
    """

    def __init__(self):
        # Active connections: user_id -> list of websockets
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # All connections (for broadcasting to everyone)
        self.all_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket, user_id: int):
        """
        Connect a new websocket client

        Args:
            websocket: WebSocket connection
            user_id: User ID for this connection
        """
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(websocket)
        self.all_connections.add(websocket)

        logger.info(f"WebSocket connected: user_id={user_id}, total={len(self.all_connections)}")

    def disconnect(self, websocket: WebSocket, user_id: int):
        """
        Disconnect a websocket client

        Args:
            websocket: WebSocket connection
            user_id: User ID for this connection
        """
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)

            # Remove user from dict if no more connections
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

        if websocket in self.all_connections:
            self.all_connections.remove(websocket)

        logger.info(f"WebSocket disconnected: user_id={user_id}, total={len(self.all_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send message to a specific websocket

        Args:
            message: Message data
            websocket: Target websocket
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")

    async def send_to_user(self, message: dict, user_id: int):
        """
        Send message to all connections of a specific user

        Args:
            message: Message data
            user_id: Target user ID
        """
        if user_id in self.active_connections:
            disconnected = []

            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")
                    disconnected.append(connection)

            # Remove disconnected websockets
            for ws in disconnected:
                self.disconnect(ws, user_id)

    async def broadcast(self, message: dict):
        """
        Broadcast message to all connected clients

        Args:
            message: Message data
        """
        disconnected = []

        for connection in self.all_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.append(connection)

        # Remove disconnected websockets
        for ws in disconnected:
            # Find and remove from active_connections
            for user_id, connections in list(self.active_connections.items()):
                if ws in connections:
                    self.disconnect(ws, user_id)
                    break

    async def send_agent_update(self, agent_id: int, user_id: int, data: dict):
        """
        Send agent status update to user

        Args:
            agent_id: Agent ID
            user_id: User ID
            data: Update data
        """
        message = {
            "type": "agent_update",
            "agent_id": agent_id,
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }

        await self.send_to_user(message, user_id)

    async def send_system_update(self, data: dict):
        """
        Send system-wide update (e.g., health status)

        Args:
            data: Update data
        """
        message = {
            "type": "system_update",
            "data": data,
            "timestamp": asyncio.get_event_loop().time()
        }

        await self.broadcast(message)

    async def send_metrics_update(self, user_id: int, metrics: dict):
        """
        Send metrics update to user

        Args:
            user_id: User ID
            metrics: Metrics data
        """
        message = {
            "type": "metrics_update",
            "data": metrics,
            "timestamp": asyncio.get_event_loop().time()
        }

        await self.send_to_user(message, user_id)


# Global connection manager instance
manager = ConnectionManager()


# ============================================================================
# WEBSOCKET AUTHENTICATION
# ============================================================================

async def verify_websocket_token(websocket: WebSocket, token: str) -> Optional[dict]:
    """
    Verify JWT token for WebSocket connection

    Args:
        websocket: WebSocket connection
        token: JWT token from client

    Returns:
        User data if valid, None if invalid
    """
    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        user_id = payload.get("user_id")
        email = payload.get("email")

        if user_id is None:
            logger.warning("WebSocket auth failed: Missing user_id in token")
            return None

        return {
            "user_id": user_id,
            "email": email
        }

    except JWTError as e:
        logger.warning(f"WebSocket auth failed: Invalid token - {str(e)}")
        return None
    except Exception as e:
        logger.error(f"WebSocket auth error: {str(e)}")
        return None


async def authenticate_websocket(websocket: WebSocket) -> Optional[int]:
    """
    Authenticate WebSocket connection

    Supports two methods:
    1. Token in query parameter: ws://host/ws?token=xxx
    2. Token in first message: {"type": "auth", "token": "xxx"}

    Args:
        websocket: WebSocket connection

    Returns:
        user_id if authenticated, None if authentication failed
    """
    try:
        # Method 1: Try to get token from query parameters
        token = websocket.query_params.get("token")

        if token:
            user_data = await verify_websocket_token(websocket, token)
            if user_data:
                logger.info(f"WebSocket authenticated via query param: user_id={user_data['user_id']}")
                return user_data["user_id"]

        # Method 2: Wait for authentication message
        # Accept connection first to receive auth message
        await websocket.accept()

        # Wait for auth message (5 second timeout)
        try:
            data = await asyncio.wait_for(
                websocket.receive_json(),
                timeout=5.0
            )

            if data.get("type") == "auth":
                token = data.get("token")
                if token:
                    user_data = await verify_websocket_token(websocket, token)
                    if user_data:
                        # Send auth success message
                        await websocket.send_json({
                            "type": "auth_success",
                            "user_id": user_data["user_id"]
                        })
                        logger.info(f"WebSocket authenticated via message: user_id={user_data['user_id']}")
                        return user_data["user_id"]

        except asyncio.TimeoutError:
            logger.warning("WebSocket auth timeout: No auth message received")

        # Authentication failed
        await websocket.send_json({
            "type": "auth_failed",
            "message": "Authentication required"
        })
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    except Exception as e:
        logger.error(f"WebSocket authentication error: {str(e)}")
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass
        return None


async def handle_websocket_message(websocket: WebSocket, user_id: int, data: dict):
    """
    Handle incoming WebSocket messages from client

    Args:
        websocket: Client websocket
        user_id: User ID
        data: Message data
    """
    message_type = data.get("type")

    if message_type == "ping":
        # Respond to ping
        await manager.send_personal_message({"type": "pong"}, websocket)

    elif message_type == "subscribe_agent":
        # Subscribe to agent updates
        agent_id = data.get("agent_id")
        await manager.send_personal_message({
            "type": "subscribed",
            "agent_id": agent_id
        }, websocket)

    elif message_type == "request_metrics":
        # Client requesting metrics update
        # This would trigger metrics collection and send back
        pass

    else:
        logger.warning(f"Unknown message type: {message_type}")


# Usage example in main.py (WITH AUTHENTICATION):
"""
from fastapi import WebSocket
from src.api.websocket import manager, handle_websocket_message, authenticate_websocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Authenticate WebSocket connection
    user_id = await authenticate_websocket(websocket)

    if user_id is None:
        # Authentication failed, connection already closed
        return

    # Connect authenticated websocket
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(websocket, user_id, data)

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


# Client-side usage:
# Method 1: Token in query parameter
ws = new WebSocket('ws://localhost:8000/ws?token=YOUR_JWT_TOKEN');

# Method 2: Token in first message
ws = new WebSocket('ws://localhost:8000/ws');
ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'auth',
        token: 'YOUR_JWT_TOKEN'
    }));
};
"""
