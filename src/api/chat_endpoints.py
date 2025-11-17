"""
Live Chat & Support API Endpoints
WebSocket + REST API for self-hosted chat
"""
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import List, Optional
from pydantic import BaseModel
from datetime import timedelta

from src.support.live_chat import (
    chat_manager,
    ChatStatus,
    MessageType,
    TicketPriority,
    TicketStatus
)
from src.auth.auth_manager import get_current_user


# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/api/chat", tags=["Live Chat"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class StartChatRequest(BaseModel):
    """Request to start chat session"""
    customer_name: str
    customer_email: str
    initial_message: Optional[str] = None


class SendMessageRequest(BaseModel):
    """Request to send message"""
    content: str
    message_type: MessageType = MessageType.TEXT
    file_url: Optional[str] = None


class CreateTicketRequest(BaseModel):
    """Request to create support ticket"""
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.NORMAL
    chat_id: Optional[str] = None


class AssignTicketRequest(BaseModel):
    """Request to assign ticket"""
    agent_id: int
    agent_name: str


class AddCannedResponseRequest(BaseModel):
    """Request to add canned response"""
    title: str
    content: str
    category: str
    shortcut: str


# ============================================================================
# CHAT ENDPOINTS
# ============================================================================

@router.post("/start")
async def start_chat_session(
    request: StartChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Start new chat session

    Creates chat and auto-assigns to available agent

    Example:
    ```python
    POST /api/chat/start
    {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "initial_message": "Hi, I need help with payment"
    }
    ```
    """
    try:
        chat = chat_manager.create_chat_session(
            customer_id=current_user.get("id"),
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            initial_message=request.initial_message
        )

        return {
            "success": True,
            "chat": chat.dict(),
            "websocket_url": f"/ws/chat/{chat.chat_id}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{chat_id}")
async def get_chat_session(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get chat session details with full message history"""
    try:
        if chat_id not in chat_manager.chats:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat = chat_manager.chats[chat_id]

        return {
            "success": True,
            "chat": chat.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/my-chats")
async def get_my_chats(
    status: Optional[ChatStatus] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all chats for current user

    Query params:
    - status: Filter by chat status
    """
    try:
        user_id = current_user.get("id")

        # Get chats for this user (as customer or agent)
        chats = [
            chat for chat in chat_manager.chats.values()
            if chat.customer_id == user_id or chat.agent_id == user_id
        ]

        # Filter by status
        if status:
            chats = [chat for chat in chats if chat.status == status]

        # Sort by last message (newest first)
        chats.sort(key=lambda c: c.last_message_at, reverse=True)

        return {
            "success": True,
            "chats": [chat.dict() for chat in chats],
            "total": len(chats)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{chat_id}/message")
async def send_message(
    chat_id: str,
    request: SendMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send message in chat

    Note: WebSocket is preferred for real-time messaging,
    but this REST endpoint is available as fallback
    """
    try:
        if chat_id not in chat_manager.chats:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat = chat_manager.chats[chat_id]
        user_id = current_user.get("id")

        # Determine sender type
        if user_id == chat.customer_id:
            sender_type = "customer"
            sender_name = chat.customer_name
        elif user_id == chat.agent_id:
            sender_type = "agent"
            sender_name = chat.agent_name
        else:
            raise HTTPException(status_code=403, detail="Not authorized for this chat")

        # Add message
        message = chat_manager.add_message(
            chat_id=chat_id,
            sender_id=user_id,
            sender_name=sender_name,
            sender_type=sender_type,
            message_type=request.message_type,
            content=request.content,
            file_url=request.file_url
        )

        return {
            "success": True,
            "message": message.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/{chat_id}/close")
async def close_chat_session(
    chat_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Close/resolve chat session"""
    try:
        if chat_id not in chat_manager.chats:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat = chat_manager.chats[chat_id]
        chat.status = ChatStatus.RESOLVED

        return {
            "success": True,
            "message": f"Chat {chat_id} closed"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SUPPORT TICKETS
# ============================================================================

@router.post("/tickets")
async def create_ticket(
    request: CreateTicketRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create support ticket

    Can be standalone or linked to chat session
    """
    try:
        ticket = chat_manager.create_ticket(
            customer_id=current_user.get("id"),
            customer_name=current_user.get("name", "Unknown"),
            customer_email=current_user.get("email"),
            subject=request.subject,
            description=request.description,
            priority=request.priority,
            chat_id=request.chat_id
        )

        return {
            "success": True,
            "ticket": ticket.dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tickets")
async def list_tickets(
    status: Optional[TicketStatus] = None,
    priority: Optional[TicketPriority] = None,
    assigned_to_me: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """
    List support tickets

    Query params:
    - status: Filter by status
    - priority: Filter by priority
    - assigned_to_me: Only tickets assigned to me
    """
    try:
        tickets = list(chat_manager.tickets.values())

        # Filter by status
        if status:
            tickets = [t for t in tickets if t.status == status]

        # Filter by priority
        if priority:
            tickets = [t for t in tickets if t.priority == priority]

        # Filter by assigned agent
        if assigned_to_me:
            user_id = current_user.get("id")
            tickets = [t for t in tickets if t.assigned_to == user_id]

        # Sort by created date (newest first)
        tickets.sort(key=lambda t: t.created_at, reverse=True)

        return {
            "success": True,
            "tickets": [ticket.dict() for ticket in tickets],
            "total": len(tickets)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tickets/{ticket_id}")
async def get_ticket(
    ticket_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get ticket details"""
    try:
        if ticket_id not in chat_manager.tickets:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket = chat_manager.tickets[ticket_id]

        return {
            "success": True,
            "ticket": ticket.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tickets/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: str,
    request: AssignTicketRequest,
    current_user: dict = Depends(get_current_user)
):
    """Assign ticket to agent"""
    try:
        chat_manager.assign_ticket(
            ticket_id=ticket_id,
            agent_id=request.agent_id,
            agent_name=request.agent_name
        )

        return {
            "success": True,
            "message": f"Ticket assigned to {request.agent_name}"
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tickets/{ticket_id}/resolve")
async def resolve_ticket(
    ticket_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Mark ticket as resolved"""
    try:
        chat_manager.resolve_ticket(ticket_id)

        return {
            "success": True,
            "message": f"Ticket {ticket_id} resolved"
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CANNED RESPONSES
# ============================================================================

@router.get("/canned-responses")
async def list_canned_responses(
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List canned responses

    Query params:
    - category: Filter by category
    """
    try:
        responses = list(chat_manager.canned_responses.values())

        if category:
            responses = [r for r in responses if r.category == category]

        return {
            "success": True,
            "responses": [r.dict() for r in responses],
            "total": len(responses)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/canned-responses")
async def add_canned_response(
    request: AddCannedResponseRequest,
    current_user: dict = Depends(get_current_user)
):
    """Add new canned response"""
    try:
        response = chat_manager.add_canned_response(
            title=request.title,
            content=request.content,
            category=request.category,
            shortcut=request.shortcut
        )

        return {
            "success": True,
            "response": response.dict()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AGENT PRESENCE
# ============================================================================

@router.post("/agent/online")
async def set_agent_online(
    current_user: dict = Depends(get_current_user)
):
    """Mark current user as online agent"""
    try:
        chat_manager.set_agent_online(
            agent_id=current_user.get("id"),
            agent_name=current_user.get("name", "Agent")
        )

        return {
            "success": True,
            "message": "You are now online"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/offline")
async def set_agent_offline(
    current_user: dict = Depends(get_current_user)
):
    """Mark current user as offline agent"""
    try:
        chat_manager.set_agent_offline(current_user.get("id"))

        return {
            "success": True,
            "message": "You are now offline"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agents/online")
async def get_online_agents():
    """Get list of online agents (no auth required for public display)"""
    try:
        agents = chat_manager.get_online_agents()

        return {
            "success": True,
            "agents": [a.dict() for a in agents],
            "total": len(agents)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS
# ============================================================================

@router.get("/stats/chats")
async def get_chat_statistics(
    time_range_hours: int = 24,
    current_user: dict = Depends(get_current_user)
):
    """
    Get chat statistics

    Query params:
    - time_range_hours: Time range in hours (default: 24)
    """
    try:
        stats = chat_manager.get_chat_stats(
            time_range=timedelta(hours=time_range_hours)
        )

        return {
            "success": True,
            "stats": stats,
            "time_range_hours": time_range_hours
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/tickets")
async def get_ticket_statistics(
    time_range_hours: int = 24,
    current_user: dict = Depends(get_current_user)
):
    """Get ticket statistics"""
    try:
        stats = chat_manager.get_ticket_stats(
            time_range=timedelta(hours=time_range_hours)
        )

        return {
            "success": True,
            "stats": stats,
            "time_range_hours": time_range_hours
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    """
    WebSocket endpoint for real-time chat

    Connect to: ws://localhost:8000/api/chat/ws/{chat_id}

    Messages:
    - Receive: {"type": "message", "data": {...}}
    - Receive: {"type": "typing", "user_id": 123, "typing": true}
    - Send: {"type": "message", "content": "Hello"}
    - Send: {"type": "typing", "typing": true}
    """
    await websocket.accept()

    # Store connection
    chat_manager.connections[chat_id] = websocket

    try:
        while True:
            # Receive message from WebSocket
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "typing":
                # Typing indicator
                user_id = data.get("user_id")
                typing = data.get("typing", False)
                await chat_manager.set_typing(chat_id, user_id, typing)

            elif message_type == "message":
                # Chat message
                # Message is added via REST API endpoint
                # This is just for real-time sync
                pass

    except WebSocketDisconnect:
        # Remove connection
        if chat_id in chat_manager.connections:
            del chat_manager.connections[chat_id]


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint (no auth required)"""
    return {
        "success": True,
        "service": "Live Chat",
        "status": "operational",
        "active_chats": len([c for c in chat_manager.chats.values() if c.status == ChatStatus.ACTIVE]),
        "online_agents": len(chat_manager.get_online_agents())
    }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = ['router']
