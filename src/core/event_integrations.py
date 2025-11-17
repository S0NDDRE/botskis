"""
Event Bus Integrations
Connect existing systems to event bus for loose coupling

This file shows how to integrate event bus with:
- Error Tracking (send alert when critical error)
- Email (send email when event occurs)
- Chat (notify agents of new chat)
- Analytics (track events)
- Payments (handle payment events)
"""
from src.core.event_bus import event_bus, Event, EventPriority
from src.monitoring.error_tracker import error_tracker, ErrorSeverity
from src.email.own_email_server import get_email_server, EmailCategory, EmailPriority
from src.support.live_chat import chat_manager
from loguru import logger


# ============================================================================
# ERROR TRACKING EVENTS
# ============================================================================

@event_bus.subscribe("error.critical")
async def on_critical_error(event: Event):
    """
    When critical error occurs, send alerts

    Event payload:
    {
        "error_type": "DatabaseError",
        "error_message": "Connection failed",
        "fingerprint": "abc123",
        "occurrences": 15
    }
    """
    email_server = get_email_server()

    await email_server.send_from_template(
        to=["admin@mindframe.no", "team@mindframe.no"],
        template_name="error_alert",
        variables=event.payload,
        category=EmailCategory.MONITORING,
        priority=EmailPriority.URGENT
    )

    logger.info(f"🚨 Critical error alert sent: {event.payload['error_type']}")


@event_bus.subscribe("error.threshold_reached")
async def on_error_threshold(event: Event):
    """When error occurs 10+ times, alert team"""
    logger.warning(
        f"⚠️  Error threshold reached: {event.payload['error_type']} "
        f"({event.payload['occurrences']} occurrences)"
    )


# ============================================================================
# USER EVENTS
# ============================================================================

@event_bus.subscribe("user.registered")
async def on_user_registered(event: Event):
    """
    When user registers, send welcome email

    Event payload:
    {
        "user_id": 123,
        "email": "john@example.com",
        "name": "John Doe"
    }
    """
    email_server = get_email_server()

    await email_server.send_email(
        to=[event.payload["email"]],
        subject=f"Welcome to Mindframe, {event.payload['name']}!",
        body=f"""
        Hi {event.payload['name']},

        Welcome to Mindframe! We're excited to have you on board.

        Here's what you can do next:
        1. Explore our 57 AI agents
        2. Set up your first automation
        3. Connect your tools

        Need help? Reply to this email or visit our support center.

        Best regards,
        The Mindframe Team
        """,
        category=EmailCategory.INTERNAL
    )

    logger.info(f"✉️  Welcome email sent to {event.payload['email']}")


@event_bus.subscribe("user.subscription.started")
async def on_subscription_started(event: Event):
    """Track subscription start"""
    logger.info(
        f"💰 New subscription: User {event.payload['user_id']} "
        f"- Plan: {event.payload['plan']} - €{event.payload['amount']}/month"
    )


@event_bus.subscribe("user.subscription.cancelled")
async def on_subscription_cancelled(event: Event):
    """When subscription cancelled, send feedback survey"""
    email_server = get_email_server()

    await email_server.send_email(
        to=[event.payload["email"]],
        subject="Sorry to see you go - Quick feedback?",
        body=f"""
        Hi {event.payload['name']},

        We noticed you cancelled your subscription. We're sorry to see you go!

        Would you mind sharing why you left? Your feedback helps us improve.

        [Feedback Survey Link]

        If you change your mind, we'd love to have you back!

        Best regards,
        The Mindframe Team
        """,
        category=EmailCategory.INTERNAL
    )

    logger.info(f"📧 Cancellation feedback email sent to {event.payload['email']}")


# ============================================================================
# PAYMENT EVENTS
# ============================================================================

@event_bus.subscribe("payment.completed")
async def on_payment_completed(event: Event):
    """
    When payment completes, send receipt

    Event payload:
    {
        "user_id": 123,
        "email": "john@example.com",
        "amount": 99.00,
        "currency": "EUR",
        "receipt_url": "https://..."
    }
    """
    logger.info(
        f"💳 Payment completed: {event.payload['amount']} {event.payload['currency']} "
        f"from user {event.payload['user_id']}"
    )

    # Analytics tracking would go here
    await event_bus.publish(
        event_type="analytics.revenue",
        payload={
            "amount": event.payload["amount"],
            "currency": event.payload["currency"],
            "timestamp": event.timestamp.isoformat()
        },
        source="payment.processor"
    )


@event_bus.subscribe("payment.failed")
async def on_payment_failed(event: Event):
    """When payment fails, notify user"""
    email_server = get_email_server()

    await email_server.send_email(
        to=[event.payload["email"]],
        subject="Payment Issue - Action Required",
        body=f"""
        Hi there,

        We had trouble processing your payment for Mindframe.

        Reason: {event.payload.get('error_message', 'Unknown error')}

        Please update your payment method to continue using Mindframe.

        [Update Payment Method]

        Best regards,
        The Mindframe Team
        """,
        category=EmailCategory.INTERNAL,
        priority=EmailPriority.HIGH
    )

    logger.warning(
        f"⚠️  Payment failed for user {event.payload['user_id']}: "
        f"{event.payload.get('error_message')}"
    )


# ============================================================================
# CHAT EVENTS
# ============================================================================

@event_bus.subscribe("chat.started")
async def on_chat_started(event: Event):
    """
    When customer starts chat, notify online agents

    Event payload:
    {
        "chat_id": "abc123",
        "customer_id": 123,
        "customer_name": "John Doe",
        "initial_message": "I need help"
    }
    """
    # Get online agents
    online_agents = chat_manager.get_online_agents()

    if online_agents:
        logger.info(
            f"💬 New chat from {event.payload['customer_name']} - "
            f"{len(online_agents)} agents notified"
        )
    else:
        logger.warning(
            f"⚠️  New chat but no agents online - sending email alert"
        )

        # No agents online - email team
        email_server = get_email_server()
        await email_server.send_email(
            to=["support@mindframe.no"],
            subject="New chat - No agents online",
            body=f"""
            New chat started but no agents are online!

            Customer: {event.payload['customer_name']}
            Message: {event.payload['initial_message']}

            Please log in to handle this chat.
            """,
            category=EmailCategory.MONITORING,
            priority=EmailPriority.HIGH
        )


@event_bus.subscribe("chat.message")
async def on_chat_message(event: Event):
    """Track chat messages for analytics"""
    # Could send to analytics system
    pass


# ============================================================================
# ANALYTICS EVENTS
# ============================================================================

@event_bus.subscribe("analytics.*")  # Wildcard - all analytics events
async def on_analytics_event(event: Event):
    """Log all analytics events"""
    logger.debug(f"📊 Analytics event: {event.event_type}")
    # Could save to database, send to external analytics, etc.


# ============================================================================
# SYSTEM EVENTS
# ============================================================================

@event_bus.subscribe("system.health.critical")
async def on_system_health_critical(event: Event):
    """
    When system health is critical, alert team

    Event payload:
    {
        "component": "database",
        "status": "down",
        "error_message": "Connection timeout"
    }
    """
    email_server = get_email_server()

    await email_server.send_from_template(
        to=["admin@mindframe.no", "devops@mindframe.no"],
        template_name="system_alert",
        variables={
            "alert_type": f"Critical System Health: {event.payload['component']}",
            "message": event.payload.get('error_message', 'Unknown error'),
            "severity": "CRITICAL",
            "timestamp": event.timestamp.isoformat(),
            "action_required": "Immediate investigation required"
        },
        category=EmailCategory.MONITORING,
        priority=EmailPriority.URGENT
    )

    logger.critical(
        f"🚨 System health critical: {event.payload['component']} - "
        f"{event.payload.get('error_message')}"
    )


@event_bus.subscribe("system.backup.completed")
async def on_backup_completed(event: Event):
    """Log successful backups"""
    logger.info(
        f"💾 Backup completed: {event.payload.get('backup_type')} "
        f"({event.payload.get('size_mb')} MB)"
    )


# ============================================================================
# AGENT EVENTS
# ============================================================================

@event_bus.subscribe("agent.activated")
async def on_agent_activated(event: Event):
    """
    When user activates agent, track usage

    Event payload:
    {
        "user_id": 123,
        "agent_id": "customer_support_bot",
        "plan": "pro"
    }
    """
    logger.info(
        f"🤖 Agent activated: {event.payload['agent_id']} "
        f"by user {event.payload['user_id']}"
    )

    # Track in analytics
    await event_bus.publish(
        event_type="analytics.agent_usage",
        payload=event.payload,
        source="agent.manager"
    )


@event_bus.subscribe("agent.error")
async def on_agent_error(event: Event):
    """When agent encounters error, track and alert"""
    logger.error(
        f"❌ Agent error: {event.payload['agent_id']} - "
        f"{event.payload.get('error_message')}"
    )

    # If critical, alert team
    if event.payload.get('severity') == 'critical':
        await event_bus.publish(
            event_type="error.critical",
            payload={
                "error_type": "AgentError",
                "error_message": event.payload.get('error_message'),
                "fingerprint": event.payload['agent_id'],
                "occurrences": 1
            },
            priority=EventPriority.CRITICAL
        )


# ============================================================================
# DAILY EVENTS
# ============================================================================

@event_bus.subscribe("daily.report")
async def on_daily_report(event: Event):
    """
    Send daily report email

    Event payload:
    {
        "date": "2025-01-16",
        "total_users": 1000,
        "active_users": 450,
        "new_signups": 25,
        "revenue": "€5,000",
        "error_count": 12,
        "uptime": 99.9,
        "avg_response_time": 150
    }
    """
    email_server = get_email_server()

    await email_server.send_from_template(
        to=["team@mindframe.no", "admin@mindframe.no"],
        template_name="daily_report",
        variables=event.payload,
        category=EmailCategory.ADMIN
    )

    logger.info(f"📊 Daily report sent for {event.payload['date']}")


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'on_critical_error',
    'on_user_registered',
    'on_payment_completed',
    'on_chat_started',
    'on_system_health_critical'
]
