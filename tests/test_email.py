"""
Email System Tests
Test email sending, templates, queuing
"""
import pytest
from datetime import datetime
import asyncio


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.asyncio
async def test_send_email():
    """Test sending basic email"""
    from src.email.own_email_server import EmailServer, EmailMessage

    server = EmailServer()

    message = EmailMessage(
        to=["test@example.com"],
        subject="Test Email",
        body="This is a test email",
        from_email="noreply@mindframe.ai"
    )

    # Mock sending (don't actually send)
    result = await server.send_email(message, mock=True)

    assert result is True


@pytest.mark.unit
def test_email_template_rendering():
    """Test rendering email template"""
    from src.email.own_email_server import EmailServer

    server = EmailServer()

    variables = {
        "user_name": "John Doe",
        "error_count": 5,
        "error_message": "Database connection failed"
    }

    html = server.render_template("error_alert", variables)

    assert "John Doe" in html
    assert "5" in html
    assert "Database connection failed" in html


@pytest.mark.unit
def test_email_template_validation():
    """Test email template exists"""
    from src.email.own_email_server import EmailServer

    server = EmailServer()

    # Valid templates
    assert server.has_template("error_alert")
    assert server.has_template("system_alert")
    assert server.has_template("daily_report")

    # Invalid template
    assert not server.has_template("nonexistent_template")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_email_queue():
    """Test email priority queue"""
    from src.email.own_email_server import EmailQueue, EmailPriority

    queue = EmailQueue()

    # Add emails with different priorities
    await queue.add(
        to=["low@example.com"],
        subject="Low Priority",
        priority=EmailPriority.LOW
    )

    await queue.add(
        to=["high@example.com"],
        subject="High Priority",
        priority=EmailPriority.HIGH
    )

    await queue.add(
        to=["normal@example.com"],
        subject="Normal Priority",
        priority=EmailPriority.NORMAL
    )

    # Get next email (should be high priority)
    next_email = await queue.get_next()

    assert next_email.subject == "High Priority"


@pytest.mark.unit
@pytest.mark.asyncio
async def test_batch_email_sending():
    """Test batch email sending"""
    from src.email.own_email_server import EmailServer

    server = EmailServer()

    recipients = [f"user{i}@example.com" for i in range(10)]

    result = await server.send_batch(
        recipients=recipients,
        subject="Batch Test",
        body="Batch email",
        mock=True  # Don't actually send
    )

    assert result["sent"] == 10
    assert result["failed"] == 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_send_from_template():
    """Test sending email from template"""
    from src.email.own_email_server import EmailServer, EmailCategory

    server = EmailServer()

    result = await server.send_from_template(
        to=["test@example.com"],
        template_name="error_alert",
        variables={
            "user_name": "Test User",
            "error_count": 3,
            "error_message": "Test error"
        },
        category=EmailCategory.ALERT,
        mock=True
    )

    assert result is True


@pytest.mark.integration
def test_send_email_endpoint(client, auth_headers):
    """Test sending email via API"""
    response = client.post(
        "/api/email/send",
        headers=auth_headers,
        json={
            "to": ["recipient@example.com"],
            "subject": "API Test",
            "body": "Test email from API"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.integration
def test_send_template_email_endpoint(client, auth_headers):
    """Test sending template email via API"""
    response = client.post(
        "/api/email/send-template",
        headers=auth_headers,
        json={
            "to": ["recipient@example.com"],
            "template": "daily_report",
            "variables": {
                "report_date": "2025-01-16",
                "total_users": 1000,
                "revenue": 50000
            }
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.integration
def test_get_email_history(client, auth_headers):
    """Test getting email send history"""
    response = client.get(
        "/api/email/history?limit=20",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "emails" in data
    assert isinstance(data["emails"], list)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_email_delivery_tracking():
    """Test tracking email delivery status"""
    from src.email.own_email_server import EmailServer

    server = EmailServer()

    # Send email
    message_id = await server.send_email_tracked(
        to=["test@example.com"],
        subject="Tracking Test",
        body="Test",
        mock=True
    )

    # Check delivery status
    status = await server.get_delivery_status(message_id)

    assert status["message_id"] == message_id
    assert status["status"] in ["sent", "delivered", "failed", "pending"]


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_complete_email_workflow():
    """Test complete email workflow"""
    from src.email.own_email_server import EmailServer, EmailPriority

    server = EmailServer()

    # 1. Send high priority alert
    alert_result = await server.send_from_template(
        to=["admin@example.com"],
        template_name="error_alert",
        variables={
            "user_name": "Admin",
            "error_count": 10,
            "error_message": "Critical system error"
        },
        priority=EmailPriority.HIGH,
        mock=True
    )

    assert alert_result is True

    # 2. Send normal priority notification
    notify_result = await server.send_email(
        to=["user@example.com"],
        subject="Notification",
        body="You have a new message",
        priority=EmailPriority.NORMAL,
        mock=True
    )

    assert notify_result is True

    # 3. Send batch emails
    batch_result = await server.send_batch(
        recipients=["user1@example.com", "user2@example.com"],
        subject="Newsletter",
        body="Monthly newsletter",
        priority=EmailPriority.LOW,
        mock=True
    )

    assert batch_result["sent"] == 2


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_email_integration_with_error_tracker():
    """Test email integration with error tracking"""
    from src.email.own_email_server import EmailServer
    from src.monitoring.error_tracker import error_tracker

    server = EmailServer()

    # Subscribe to error events
    async def send_error_alert(error_event):
        await server.send_from_template(
            to=["admin@example.com"],
            template_name="error_alert",
            variables={
                "user_name": "Admin",
                "error_count": error_event.occurrences,
                "error_message": error_event.message
            },
            mock=True
        )

    error_tracker.add_alert_callback(send_error_alert)

    # Trigger error
    try:
        raise ValueError("Test error for email")
    except ValueError as e:
        await error_tracker.capture_exception(e)

    # Email should be queued/sent (verified through callback)


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_email_integration_with_event_bus():
    """Test email integration with event bus"""
    from src.email.own_email_server import EmailServer
    from src.core.event_bus import EventBus

    server = EmailServer()
    bus = EventBus()

    emails_sent = []

    # Subscribe to user registration events
    @bus.subscribe("user.registered")
    async def send_welcome_email(event):
        result = await server.send_from_template(
            to=[event.payload["email"]],
            template_name="welcome",  # Would need to create this
            variables={
                "user_name": event.payload["name"]
            },
            mock=True
        )
        emails_sent.append(result)

    # Trigger user registration
    await bus.publish(
        "user.registered",
        {
            "user_id": 123,
            "email": "newuser@example.com",
            "name": "New User"
        }
    )

    await asyncio.sleep(0.1)

    # Welcome email should be sent
    assert len(emails_sent) > 0


@pytest.mark.e2e
def test_email_statistics(client, auth_headers):
    """Test getting email statistics"""

    # Get stats
    response = client.get(
        "/api/email/statistics",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "total_sent" in data
    assert "delivery_rate" in data
    assert "by_category" in data


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_email_retry_logic():
    """Test email retry on failure"""
    from src.email.own_email_server import EmailServer

    server = EmailServer()

    # Track retry attempts
    attempts = []

    async def mock_send_with_failure(email):
        attempts.append(1)
        if len(attempts) < 3:
            raise Exception("Simulated send failure")
        return True

    # Temporarily replace send method
    original_send = server._send
    server._send = mock_send_with_failure

    # Send email (should retry)
    result = await server.send_email_with_retry(
        to=["test@example.com"],
        subject="Retry Test",
        body="Test",
        max_retries=3
    )

    # Should succeed after retries
    assert result is True
    assert len(attempts) == 3

    # Restore original method
    server._send = original_send
