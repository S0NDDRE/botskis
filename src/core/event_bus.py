"""
Event Bus - Async Event-Driven Architecture
Enables loose coupling and scalability

Features:
- Pub/Sub pattern
- Async event handling
- Event filtering
- Event history
- Dead letter queue
- Priority events
- Event replay
"""
from typing import Dict, List, Callable, Any, Optional, Set
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import asyncio
from loguru import logger
import uuid
import json


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class EventPriority(str, Enum):
    """Event priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EventStatus(str, Enum):
    """Event processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class Event(BaseModel):
    """Event model"""
    event_id: str
    event_type: str
    payload: Dict[str, Any]
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime
    source: str
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = {}


class EventHandler(BaseModel):
    """Event handler registration"""
    handler_id: str
    event_type: str
    callback: Any  # Callable (can't serialize)
    filter_func: Optional[Any] = None
    async_handler: bool = True
    retry_count: int = 3
    timeout_seconds: int = 30


class EventLog(BaseModel):
    """Event processing log"""
    event_id: str
    event_type: str
    status: EventStatus
    timestamp: datetime
    handler_id: Optional[str] = None
    error_message: Optional[str] = None
    processing_time_ms: Optional[float] = None


# ============================================================================
# EVENT BUS
# ============================================================================

class EventBus:
    """
    Event Bus - Async Event-Driven Architecture

    Pattern: Pub/Sub

    Benefits:
    - Loose coupling between components
    - Easy to add new features (just subscribe to events)
    - Scalable (async processing)
    - Testable (can mock events)
    - Event history for debugging

    Example usage:
    ```python
    # Publisher
    await event_bus.publish(
        event_type="user.registered",
        payload={"user_id": 123, "email": "john@example.com"}
    )

    # Subscriber
    @event_bus.subscribe("user.registered")
    async def on_user_registered(event: Event):
        # Send welcome email
        await email_service.send_welcome_email(event.payload["email"])
    ```
    """

    def __init__(self):
        # Event handlers by event type
        self.handlers: Dict[str, List[EventHandler]] = {}

        # Event queue (priority-based)
        self.event_queue: asyncio.Queue = asyncio.Queue()

        # Event history
        self.event_history: List[Event] = []
        self.event_logs: List[EventLog] = []

        # Dead letter queue (failed events)
        self.dead_letter_queue: List[Event] = []

        # Processing flags
        self.processing = False
        self.worker_task: Optional[asyncio.Task] = None

        # Stats
        self.stats = {
            "total_events": 0,
            "total_processed": 0,
            "total_failed": 0,
            "events_per_type": {}
        }

    # ========================================================================
    # PUBLISHING
    # ========================================================================

    async def publish(
        self,
        event_type: str,
        payload: Dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        source: str = "system",
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Publish event to bus

        Args:
            event_type: Event type (e.g., "user.registered", "payment.completed")
            payload: Event data
            priority: Event priority
            source: Event source
            correlation_id: For tracking related events
            metadata: Additional metadata

        Returns:
            Event ID

        Example:
        ```python
        event_id = await event_bus.publish(
            event_type="order.created",
            payload={"order_id": 456, "amount": 99.00},
            priority=EventPriority.HIGH,
            source="api.orders"
        )
        ```
        """
        event_id = str(uuid.uuid4())

        event = Event(
            event_id=event_id,
            event_type=event_type,
            payload=payload,
            priority=priority,
            timestamp=datetime.now(),
            source=source,
            correlation_id=correlation_id,
            metadata=metadata or {}
        )

        # Add to queue
        await self.event_queue.put(event)

        # Add to history
        self.event_history.append(event)

        # Keep only last 1000 events in memory
        if len(self.event_history) > 1000:
            self.event_history = self.event_history[-1000:]

        # Update stats
        self.stats["total_events"] += 1
        if event_type not in self.stats["events_per_type"]:
            self.stats["events_per_type"][event_type] = 0
        self.stats["events_per_type"][event_type] += 1

        logger.debug(f"📢 Event published: {event_type} [{event_id}]")
        return event_id

    # ========================================================================
    # SUBSCRIBING
    # ========================================================================

    def subscribe(
        self,
        event_type: str,
        filter_func: Optional[Callable[[Event], bool]] = None,
        retry_count: int = 3,
        timeout_seconds: int = 30
    ):
        """
        Subscribe to events (decorator)

        Args:
            event_type: Event type to subscribe to (supports wildcards: "user.*")
            filter_func: Optional filter function
            retry_count: Number of retries on failure
            timeout_seconds: Handler timeout

        Example:
        ```python
        @event_bus.subscribe("user.registered")
        async def on_user_registered(event: Event):
            user_id = event.payload["user_id"]
            await send_welcome_email(user_id)

        @event_bus.subscribe("payment.*")  # Wildcard
        async def on_any_payment(event: Event):
            await log_payment_event(event)

        @event_bus.subscribe(
            "order.created",
            filter_func=lambda e: e.payload.get("amount", 0) > 100
        )
        async def on_large_order(event: Event):
            await notify_sales_team(event)
        ```
        """
        def decorator(callback: Callable):
            handler_id = str(uuid.uuid4())

            handler = EventHandler(
                handler_id=handler_id,
                event_type=event_type,
                callback=callback,
                filter_func=filter_func,
                async_handler=asyncio.iscoroutinefunction(callback),
                retry_count=retry_count,
                timeout_seconds=timeout_seconds
            )

            # Add to handlers
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            self.handlers[event_type].append(handler)

            logger.info(f"✅ Subscribed to {event_type} [{handler_id}]")
            return callback

        return decorator

    def unsubscribe(self, event_type: str, handler_id: str):
        """Unsubscribe handler"""
        if event_type in self.handlers:
            self.handlers[event_type] = [
                h for h in self.handlers[event_type]
                if h.handler_id != handler_id
            ]
            logger.info(f"❌ Unsubscribed from {event_type} [{handler_id}]")

    # ========================================================================
    # PROCESSING
    # ========================================================================

    async def start_processing(self):
        """Start processing events from queue"""
        if self.processing:
            logger.warning("Event bus already processing")
            return

        self.processing = True
        self.worker_task = asyncio.create_task(self._process_events())
        logger.info("🚀 Event bus started processing")

    async def stop_processing(self):
        """Stop processing events"""
        self.processing = False
        if self.worker_task:
            await self.worker_task
        logger.info("⏸️  Event bus stopped processing")

    async def _process_events(self):
        """Worker that processes events from queue"""
        while self.processing:
            try:
                # Get event from queue (with timeout)
                event = await asyncio.wait_for(
                    self.event_queue.get(),
                    timeout=1.0
                )

                # Process event
                await self._handle_event(event)

            except asyncio.TimeoutError:
                # No events in queue, continue
                continue
            except Exception as e:
                logger.error(f"Error in event processing loop: {e}")

    async def _handle_event(self, event: Event):
        """Handle single event"""
        start_time = datetime.now()

        # Find matching handlers
        matching_handlers = self._find_handlers(event)

        if not matching_handlers:
            logger.debug(f"No handlers for event type: {event.event_type}")
            return

        # Execute all matching handlers
        for handler in matching_handlers:
            await self._execute_handler(event, handler, start_time)

    def _find_handlers(self, event: Event) -> List[EventHandler]:
        """Find handlers matching event type (supports wildcards)"""
        matching = []

        for event_type, handlers in self.handlers.items():
            # Exact match
            if event_type == event.event_type:
                matching.extend(handlers)

            # Wildcard match (e.g., "user.*" matches "user.registered")
            elif "*" in event_type:
                pattern = event_type.replace(".", "\\.").replace("*", ".*")
                import re
                if re.match(f"^{pattern}$", event.event_type):
                    matching.extend(handlers)

        # Apply filters
        filtered = []
        for handler in matching:
            if handler.filter_func is None:
                filtered.append(handler)
            elif handler.filter_func(event):
                filtered.append(handler)

        return filtered

    async def _execute_handler(
        self,
        event: Event,
        handler: EventHandler,
        start_time: datetime
    ):
        """Execute handler with retries and timeout"""
        log = EventLog(
            event_id=event.event_id,
            event_type=event.event_type,
            status=EventStatus.PROCESSING,
            timestamp=datetime.now(),
            handler_id=handler.handler_id
        )

        retries_left = handler.retry_count

        while retries_left >= 0:
            try:
                # Execute with timeout
                if handler.async_handler:
                    await asyncio.wait_for(
                        handler.callback(event),
                        timeout=handler.timeout_seconds
                    )
                else:
                    # Sync handler (run in executor)
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, handler.callback, event)

                # Success
                log.status = EventStatus.COMPLETED
                processing_time = (datetime.now() - start_time).total_seconds() * 1000
                log.processing_time_ms = processing_time

                self.stats["total_processed"] += 1

                logger.debug(
                    f"✅ Handler executed: {event.event_type} "
                    f"[{handler.handler_id[:8]}] ({processing_time:.2f}ms)"
                )
                break

            except asyncio.TimeoutError:
                retries_left -= 1
                if retries_left < 0:
                    log.status = EventStatus.FAILED
                    log.error_message = "Handler timeout"
                    self.stats["total_failed"] += 1
                    logger.error(
                        f"❌ Handler timeout: {event.event_type} "
                        f"[{handler.handler_id[:8]}]"
                    )
                else:
                    logger.warning(f"⚠️  Retrying handler ({retries_left} left)")
                    await asyncio.sleep(1)  # Backoff

            except Exception as e:
                retries_left -= 1
                if retries_left < 0:
                    log.status = EventStatus.FAILED
                    log.error_message = str(e)
                    self.stats["total_failed"] += 1
                    logger.error(
                        f"❌ Handler error: {event.event_type} "
                        f"[{handler.handler_id[:8]}]: {e}"
                    )

                    # Add to dead letter queue
                    self.dead_letter_queue.append(event)
                else:
                    logger.warning(f"⚠️  Retrying handler ({retries_left} left): {e}")
                    await asyncio.sleep(1)

        # Log execution
        self.event_logs.append(log)

        # Keep only last 1000 logs
        if len(self.event_logs) > 1000:
            self.event_logs = self.event_logs[-1000:]

    # ========================================================================
    # EVENT REPLAY
    # ========================================================================

    async def replay_event(self, event_id: str):
        """Replay event from history"""
        event = next((e for e in self.event_history if e.event_id == event_id), None)

        if not event:
            raise ValueError(f"Event {event_id} not found in history")

        await self.event_queue.put(event)
        logger.info(f"🔄 Replaying event {event_id}")

    async def replay_events(
        self,
        event_type: Optional[str] = None,
        since: Optional[datetime] = None
    ):
        """Replay multiple events"""
        events = self.event_history

        # Filter by type
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        # Filter by time
        if since:
            events = [e for e in events if e.timestamp >= since]

        for event in events:
            await self.event_queue.put(event)

        logger.info(f"🔄 Replaying {len(events)} events")

    # ========================================================================
    # DEAD LETTER QUEUE
    # ========================================================================

    async def retry_dead_letter_queue(self):
        """Retry all failed events"""
        events = self.dead_letter_queue.copy()
        self.dead_letter_queue.clear()

        for event in events:
            await self.event_queue.put(event)

        logger.info(f"🔄 Retrying {len(events)} failed events")

    # ========================================================================
    # STATISTICS
    # ========================================================================

    def get_stats(self) -> Dict:
        """Get event bus statistics"""
        return {
            "total_events": self.stats["total_events"],
            "total_processed": self.stats["total_processed"],
            "total_failed": self.stats["total_failed"],
            "success_rate": (
                (self.stats["total_processed"] / self.stats["total_events"] * 100)
                if self.stats["total_events"] > 0 else 100
            ),
            "events_per_type": self.stats["events_per_type"],
            "queue_size": self.event_queue.qsize(),
            "dead_letter_queue_size": len(self.dead_letter_queue),
            "history_size": len(self.event_history),
            "handlers_count": sum(len(h) for h in self.handlers.values())
        }

    def get_event_history(
        self,
        event_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Event]:
        """Get event history"""
        events = self.event_history

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        # Return last N events
        return events[-limit:]

    def get_event_logs(
        self,
        event_type: Optional[str] = None,
        status: Optional[EventStatus] = None,
        limit: int = 100
    ) -> List[EventLog]:
        """Get event processing logs"""
        logs = self.event_logs

        if event_type:
            logs = [l for l in logs if l.event_type == event_type]

        if status:
            logs = [l for l in logs if l.status == status]

        return logs[-limit:]


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Singleton event bus
event_bus = EventBus()


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'EventBus',
    'Event',
    'EventHandler',
    'EventLog',
    'EventPriority',
    'EventStatus',
    'event_bus'
]
