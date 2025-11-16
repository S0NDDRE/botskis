"""
Event Bus Tests
Test event publishing, subscription, replay
"""
import pytest
import asyncio
from datetime import datetime


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.asyncio
async def test_publish_event():
    """Test publishing event to bus"""
    from src.core.event_bus import EventBus, Event

    bus = EventBus()

    event_id = await bus.publish(
        event_type="user.registered",
        payload={"user_id": 123, "email": "test@example.com"}
    )

    assert event_id is not None
    assert isinstance(event_id, str)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_subscribe_to_event():
    """Test subscribing to events"""
    from src.core.event_bus import EventBus

    bus = EventBus()
    received_events = []

    @bus.subscribe("user.registered")
    async def handle_user_registered(event):
        received_events.append(event)

    # Publish event
    await bus.publish(
        event_type="user.registered",
        payload={"user_id": 123}
    )

    # Give time for async processing
    await asyncio.sleep(0.1)

    assert len(received_events) == 1
    assert received_events[0].payload["user_id"] == 123


@pytest.mark.unit
@pytest.mark.asyncio
async def test_wildcard_subscription():
    """Test wildcard event subscription"""
    from src.core.event_bus import EventBus

    bus = EventBus()
    received_events = []

    @bus.subscribe("user.*")
    async def handle_all_user_events(event):
        received_events.append(event)

    # Publish multiple user events
    await bus.publish("user.registered", {"user_id": 1})
    await bus.publish("user.login", {"user_id": 1})
    await bus.publish("user.logout", {"user_id": 1})

    await asyncio.sleep(0.1)

    assert len(received_events) == 3


@pytest.mark.unit
@pytest.mark.asyncio
async def test_priority_events():
    """Test priority event processing"""
    from src.core.event_bus import EventBus, EventPriority

    bus = EventBus()
    processed_order = []

    @bus.subscribe("alert.*")
    async def handle_alert(event):
        processed_order.append(event.priority)

    # Publish events with different priorities
    await bus.publish("alert.info", {}, priority=EventPriority.LOW)
    await bus.publish("alert.critical", {}, priority=EventPriority.HIGH)
    await bus.publish("alert.warning", {}, priority=EventPriority.NORMAL)

    await asyncio.sleep(0.2)

    # HIGH priority should be processed first
    assert processed_order[0] == EventPriority.HIGH


@pytest.mark.unit
@pytest.mark.asyncio
async def test_event_replay():
    """Test event replay functionality"""
    from src.core.event_bus import EventBus

    bus = EventBus()

    # Publish some events
    await bus.publish("test.event", {"count": 1})
    await bus.publish("test.event", {"count": 2})
    await bus.publish("test.event", {"count": 3})

    # Replay events
    replayed_events = await bus.replay_events(
        event_type="test.event",
        limit=10
    )

    assert len(replayed_events) == 3
    assert replayed_events[0].payload["count"] == 1


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_event_integration_with_error_tracker():
    """Test event bus integration with error tracker"""
    from src.core.event_bus import EventBus
    from src.monitoring.error_tracker import error_tracker

    bus = EventBus()

    # Subscribe to error events
    @bus.subscribe("error.occurred")
    async def handle_error(event):
        # This would normally log to error tracker
        await error_tracker.capture_exception(
            Exception(event.payload.get("message", "Unknown error")),
            context=event.payload.get("context")
        )

    # Publish error event
    await bus.publish(
        "error.occurred",
        {
            "message": "Test error",
            "context": {"endpoint": "/api/test"}
        }
    )

    await asyncio.sleep(0.1)

    # Verify error was tracked
    # Note: Would need to check error_tracker.errors in real implementation


@pytest.mark.integration
@pytest.mark.asyncio
async def test_event_integration_with_email():
    """Test event bus integration with email system"""
    from src.core.event_bus import EventBus

    bus = EventBus()
    emails_sent = []

    @bus.subscribe("user.registered")
    async def send_welcome_email(event):
        # Mock email sending
        emails_sent.append({
            "to": event.payload["email"],
            "template": "welcome",
            "user_id": event.payload["user_id"]
        })

    # User registration triggers email
    await bus.publish(
        "user.registered",
        {
            "user_id": 123,
            "email": "newuser@example.com",
            "name": "New User"
        }
    )

    await asyncio.sleep(0.1)

    assert len(emails_sent) == 1
    assert emails_sent[0]["to"] == "newuser@example.com"
    assert emails_sent[0]["template"] == "welcome"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_multiple_handlers_same_event():
    """Test multiple handlers for same event"""
    from src.core.event_bus import EventBus

    bus = EventBus()

    handler1_called = []
    handler2_called = []

    @bus.subscribe("order.placed")
    async def send_confirmation_email(event):
        handler1_called.append(event.event_id)

    @bus.subscribe("order.placed")
    async def update_inventory(event):
        handler2_called.append(event.event_id)

    # Publish order placed event
    event_id = await bus.publish(
        "order.placed",
        {"order_id": "ord_123", "amount": 99.00}
    )

    await asyncio.sleep(0.1)

    # Both handlers should be called
    assert len(handler1_called) == 1
    assert len(handler2_called) == 1
    assert handler1_called[0] == event_id
    assert handler2_called[0] == event_id


@pytest.mark.integration
def test_event_bus_api_publish(client, auth_headers):
    """Test publishing event via REST API"""
    response = client.post(
        "/api/events/publish",
        headers=auth_headers,
        json={
            "event_type": "custom.event",
            "payload": {
                "message": "Test event from API"
            }
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "event_id" in data


@pytest.mark.integration
def test_event_bus_api_get_history(client, auth_headers):
    """Test getting event history via API"""
    # Publish some events first
    client.post(
        "/api/events/publish",
        headers=auth_headers,
        json={
            "event_type": "test.event",
            "payload": {"count": 1}
        }
    )

    # Get history
    response = client.get(
        "/api/events/history?event_type=test.event",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert len(data["events"]) > 0


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_complete_event_flow():
    """Test complete event-driven flow"""
    from src.core.event_bus import EventBus

    bus = EventBus()

    # Track all actions
    actions_performed = []

    # 1. User registers
    @bus.subscribe("user.registered")
    async def on_user_registered(event):
        actions_performed.append("welcome_email_sent")

        # Trigger another event
        await bus.publish(
            "email.sent",
            {
                "user_id": event.payload["user_id"],
                "email_type": "welcome"
            }
        )

    # 2. Email sent
    @bus.subscribe("email.sent")
    async def on_email_sent(event):
        actions_performed.append("email_logged")

        # Trigger analytics event
        await bus.publish(
            "analytics.track",
            {
                "user_id": event.payload["user_id"],
                "event": "email_sent",
                "properties": {"email_type": event.payload["email_type"]}
            }
        )

    # 3. Analytics tracked
    @bus.subscribe("analytics.track")
    async def on_analytics_track(event):
        actions_performed.append("analytics_recorded")

    # Trigger initial event
    await bus.publish(
        "user.registered",
        {
            "user_id": 123,
            "email": "test@example.com",
            "name": "Test User"
        }
    )

    # Wait for cascade
    await asyncio.sleep(0.3)

    # Verify all actions were performed
    assert "welcome_email_sent" in actions_performed
    assert "email_logged" in actions_performed
    assert "analytics_recorded" in actions_performed


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_dead_letter_queue():
    """Test dead letter queue for failed events"""
    from src.core.event_bus import EventBus

    bus = EventBus()

    @bus.subscribe("test.failing")
    async def failing_handler(event):
        raise Exception("Handler failed!")

    # Publish event that will fail
    event_id = await bus.publish(
        "test.failing",
        {"data": "test"}
    )

    await asyncio.sleep(0.1)

    # Check dead letter queue
    dlq_events = await bus.get_dead_letter_queue()

    # Event should be in DLQ after max retries
    assert len(dlq_events) > 0


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_event_driven_order_processing():
    """Test event-driven order processing workflow"""
    from src.core.event_bus import EventBus

    bus = EventBus()

    workflow_steps = []

    @bus.subscribe("order.placed")
    async def validate_order(event):
        workflow_steps.append("validated")
        await bus.publish("order.validated", event.payload)

    @bus.subscribe("order.validated")
    async def charge_payment(event):
        workflow_steps.append("charged")
        await bus.publish("payment.charged", event.payload)

    @bus.subscribe("payment.charged")
    async def fulfill_order(event):
        workflow_steps.append("fulfilled")
        await bus.publish("order.fulfilled", event.payload)

    @bus.subscribe("order.fulfilled")
    async def send_confirmation(event):
        workflow_steps.append("confirmed")

    # Start workflow
    await bus.publish(
        "order.placed",
        {
            "order_id": "ord_123",
            "customer_id": 456,
            "amount": 99.00
        }
    )

    await asyncio.sleep(0.3)

    # Verify complete workflow
    assert workflow_steps == ["validated", "charged", "fulfilled", "confirmed"]
