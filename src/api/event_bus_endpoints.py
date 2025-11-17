"""
Event Bus API Endpoints
Monitoring and debugging event bus
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from src.core.event_bus import (
    event_bus,
    EventPriority,
    EventStatus
)
from src.auth.auth_manager import get_current_user


# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/api/events", tags=["Event Bus"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class PublishEventRequest(BaseModel):
    """Request to publish event"""
    event_type: str
    payload: Dict[str, Any]
    priority: EventPriority = EventPriority.NORMAL
    source: str = "api"
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# ============================================================================
# PUBLISHING
# ============================================================================

@router.post("/publish")
async def publish_event(
    request: PublishEventRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Publish event to event bus

    Example:
    ```python
    POST /api/events/publish
    {
        "event_type": "user.action",
        "payload": {"user_id": 123, "action": "clicked_button"},
        "priority": "normal"
    }
    ```
    """
    try:
        event_id = await event_bus.publish(
            event_type=request.event_type,
            payload=request.payload,
            priority=request.priority,
            source=request.source,
            correlation_id=request.correlation_id,
            metadata=request.metadata
        )

        return {
            "success": True,
            "event_id": event_id,
            "message": f"Event published: {request.event_type}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS & MONITORING
# ============================================================================

@router.get("/stats")
async def get_event_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Get event bus statistics

    Returns:
    - Total events published
    - Total events processed
    - Success rate
    - Queue size
    - Dead letter queue size
    - Events per type
    """
    try:
        stats = event_bus.get_stats()

        return {
            "success": True,
            "stats": stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_event_history(
    event_type: Optional[str] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """
    Get event history

    Query params:
    - event_type: Filter by event type
    - limit: Number of events to return (max 1000)
    """
    try:
        events = event_bus.get_event_history(
            event_type=event_type,
            limit=min(limit, 1000)
        )

        return {
            "success": True,
            "events": [e.dict() for e in events],
            "total": len(events)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_event_logs(
    event_type: Optional[str] = None,
    status: Optional[EventStatus] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """
    Get event processing logs

    Query params:
    - event_type: Filter by event type
    - status: Filter by status (pending/processing/completed/failed)
    - limit: Number of logs to return (max 1000)
    """
    try:
        logs = event_bus.get_event_logs(
            event_type=event_type,
            status=status,
            limit=min(limit, 1000)
        )

        return {
            "success": True,
            "logs": [log.dict() for log in logs],
            "total": len(logs)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DEAD LETTER QUEUE
# ============================================================================

@router.get("/dead-letter-queue")
async def get_dead_letter_queue(
    current_user: dict = Depends(get_current_user)
):
    """Get events in dead letter queue (failed events)"""
    try:
        return {
            "success": True,
            "events": [e.dict() for e in event_bus.dead_letter_queue],
            "total": len(event_bus.dead_letter_queue)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dead-letter-queue/retry")
async def retry_dead_letter_queue(
    current_user: dict = Depends(get_current_user)
):
    """Retry all failed events"""
    try:
        count = len(event_bus.dead_letter_queue)
        await event_bus.retry_dead_letter_queue()

        return {
            "success": True,
            "message": f"Retrying {count} failed events"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EVENT REPLAY
# ============================================================================

@router.post("/replay/{event_id}")
async def replay_event(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Replay single event from history"""
    try:
        await event_bus.replay_event(event_id)

        return {
            "success": True,
            "message": f"Event {event_id} replayed"
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONTROL
# ============================================================================

@router.post("/start")
async def start_processing(
    current_user: dict = Depends(get_current_user)
):
    """Start event bus processing"""
    try:
        await event_bus.start_processing()

        return {
            "success": True,
            "message": "Event bus started"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_processing(
    current_user: dict = Depends(get_current_user)
):
    """Stop event bus processing"""
    try:
        await event_bus.stop_processing()

        return {
            "success": True,
            "message": "Event bus stopped"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint (no auth required)"""
    try:
        stats = event_bus.get_stats()

        return {
            "success": True,
            "service": "Event Bus",
            "status": "operational" if event_bus.processing else "stopped",
            "processing": event_bus.processing,
            "queue_size": stats["queue_size"],
            "handlers": stats["handlers_count"]
        }

    except Exception as e:
        return {
            "success": False,
            "service": "Event Bus",
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = ['router']
