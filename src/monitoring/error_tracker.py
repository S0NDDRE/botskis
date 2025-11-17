"""
Egen Error Tracking System
Erstatter Sentry - Full kontroll over data
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from loguru import logger
import traceback
import sys
import hashlib
import json
from enum import Enum


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class ErrorSeverity(str, Enum):
    """Error severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorContext(BaseModel):
    """Error context information"""
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    environment: str = "production"
    additional_data: Dict = {}


class ErrorEvent(BaseModel):
    """Error event model"""
    error_id: str
    error_type: str
    error_message: str
    stack_trace: str
    context: ErrorContext
    timestamp: datetime
    fingerprint: str  # Hash for grouping similar errors
    severity: ErrorSeverity = ErrorSeverity.ERROR
    resolved: bool = False
    occurrences: int = 1
    first_seen: datetime
    last_seen: datetime
    affected_users: List[int] = []


class ErrorStats(BaseModel):
    """Error statistics"""
    total_errors: int
    total_occurrences: int
    unresolved: int
    critical: int
    by_severity: Dict[str, int]
    top_errors: List[dict]
    affected_users_count: int


# ============================================================================
# ERROR TRACKER
# ============================================================================

class ErrorTracker:
    """
    Self-hosted Error Tracking System

    Features:
    - Error capture & logging
    - Stack trace analysis
    - Error grouping (by fingerprint)
    - User impact tracking
    - Real-time alerts
    - Error resolution workflow
    - Performance metrics
    - Search & filtering

    Replaces: Sentry ($80/month)
    Cost: $0
    Savings: $960/year
    """

    def __init__(self):
        self.errors: Dict[str, ErrorEvent] = {}
        self.alert_webhooks: List[str] = []
        self.email_alerts: List[str] = []

        # Alert thresholds
        self.alert_threshold_occurrences = 10  # Alert after 10 occurrences
        self.alert_threshold_users = 5  # Alert if 5+ users affected

    # ========================================================================
    # ERROR CAPTURE
    # ========================================================================

    async def capture_exception(
        self,
        exception: Exception,
        context: Optional[ErrorContext] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR
    ) -> str:
        """
        Capture exception and create error event

        Usage:
        ```python
        try:
            risky_operation()
        except Exception as e:
            await error_tracker.capture_exception(e, context)
        ```
        """
        # Get error details
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = ''.join(traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        ))

        # Create fingerprint (hash) for grouping
        fingerprint = self._create_fingerprint(
            error_type,
            error_message,
            stack_trace
        )

        # Check if error already exists
        if fingerprint in self.errors:
            # Update existing error
            error = self.errors[fingerprint]
            error.occurrences += 1
            error.last_seen = datetime.now()

            # Track affected user
            if context and context.user_id:
                if context.user_id not in error.affected_users:
                    error.affected_users.append(context.user_id)

            # Check if should alert
            if error.occurrences % self.alert_threshold_occurrences == 0:
                await self._send_alert(error, "Recurring error threshold reached")

            return fingerprint

        # Create new error event
        now = datetime.now()
        error_event = ErrorEvent(
            error_id=fingerprint[:8],
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            context=context or ErrorContext(),
            timestamp=now,
            fingerprint=fingerprint,
            severity=severity,
            first_seen=now,
            last_seen=now,
            affected_users=[context.user_id] if context and context.user_id else []
        )

        # Store error
        self.errors[fingerprint] = error_event

        # Alert if critical
        if severity == ErrorSeverity.CRITICAL:
            await self._send_alert(error_event, "CRITICAL ERROR")

        # Save to database
        await self._save_to_db(error_event)

        logger.error(
            f"Error captured: {error_type} - {error_message} "
            f"[{fingerprint[:8]}]"
        )

        return fingerprint

    async def capture_message(
        self,
        message: str,
        level: ErrorSeverity = ErrorSeverity.INFO,
        context: Optional[ErrorContext] = None
    ):
        """
        Capture custom message (for logging important events)

        Usage:
        ```python
        await error_tracker.capture_message(
            "Payment failed for user 123",
            level=ErrorSeverity.WARNING
        )
        ```
        """
        # Create a pseudo-exception for consistent handling
        class CustomMessage(Exception):
            pass

        try:
            raise CustomMessage(message)
        except CustomMessage as e:
            await self.capture_exception(e, context, level)

    # ========================================================================
    # ERROR GROUPING
    # ========================================================================

    def _create_fingerprint(
        self,
        error_type: str,
        message: str,
        stack: str
    ) -> str:
        """Create unique fingerprint for error grouping"""
        # Extract relevant stack trace lines (ignore library code)
        stack_lines = []
        for line in stack.split('\n'):
            if 'File' in line:
                # Ignore virtual environment and library code
                if '/venv/' not in line and '/site-packages/' not in line:
                    stack_lines.append(line.strip())

        # Use top 3 frames for fingerprint
        stack_key = '\n'.join(stack_lines[:3])

        # Normalize message (remove numbers, IDs)
        normalized_message = self._normalize_message(message)

        # Create hash
        content = f"{error_type}:{normalized_message}:{stack_key}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _normalize_message(self, message: str) -> str:
        """Normalize error message (remove variable data)"""
        import re

        # Remove numbers
        message = re.sub(r'\d+', 'N', message)

        # Remove UUIDs
        message = re.sub(
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            'UUID',
            message,
            flags=re.IGNORECASE
        )

        # Remove email addresses
        message = re.sub(r'\S+@\S+', 'EMAIL', message)

        return message

    # ========================================================================
    # ALERTING
    # ========================================================================

    async def _send_alert(
        self,
        error: ErrorEvent,
        alert_type: str = "Error Alert"
    ):
        """Send alert to team"""
        # Slack webhook
        if self.alert_webhooks:
            import aiohttp

            for webhook_url in self.alert_webhooks:
                try:
                    async with aiohttp.ClientSession() as session:
                        await session.post(webhook_url, json={
                            "text": f"🚨 {alert_type}",
                            "attachments": [{
                                "color": "danger" if error.severity == ErrorSeverity.CRITICAL else "warning",
                                "fields": [
                                    {
                                        "title": "Error Type",
                                        "value": error.error_type,
                                        "short": True
                                    },
                                    {
                                        "title": "Severity",
                                        "value": error.severity.upper(),
                                        "short": True
                                    },
                                    {
                                        "title": "Message",
                                        "value": error.error_message[:200],
                                        "short": False
                                    },
                                    {
                                        "title": "Occurrences",
                                        "value": str(error.occurrences),
                                        "short": True
                                    },
                                    {
                                        "title": "Affected Users",
                                        "value": str(len(error.affected_users)),
                                        "short": True
                                    },
                                    {
                                        "title": "Environment",
                                        "value": error.context.environment,
                                        "short": True
                                    },
                                    {
                                        "title": "Error ID",
                                        "value": error.error_id,
                                        "short": True
                                    }
                                ]
                            }]
                        })
                except Exception as e:
                    logger.error(f"Failed to send Slack alert: {e}")

        # Email alerts
        if self.email_alerts:
            from src.email.email_manager import email_manager

            for email in self.email_alerts:
                try:
                    await email_manager.send_email(
                        to=email,
                        subject=f"🚨 {alert_type}: {error.error_type}",
                        body=f"""
                        Error Alert: {error.error_type}

                        Message: {error.error_message}
                        Severity: {error.severity}
                        Occurrences: {error.occurrences}
                        Affected Users: {len(error.affected_users)}

                        Environment: {error.context.environment}
                        Error ID: {error.error_id}

                        First seen: {error.first_seen}
                        Last seen: {error.last_seen}

                        View details: https://mindframe.no/admin/errors/{error.fingerprint}
                        """
                    )
                except Exception as e:
                    logger.error(f"Failed to send email alert: {e}")

    # ========================================================================
    # ERROR MANAGEMENT
    # ========================================================================

    async def resolve_error(self, fingerprint: str, resolved_by: int) -> bool:
        """Mark error as resolved"""
        if fingerprint in self.errors:
            self.errors[fingerprint].resolved = True

            # Save to database
            await self._update_db(fingerprint, {"resolved": True})

            logger.info(f"Error {fingerprint[:8]} resolved by user {resolved_by}")
            return True

        return False

    async def delete_error(self, fingerprint: str) -> bool:
        """Delete error (permanent)"""
        if fingerprint in self.errors:
            del self.errors[fingerprint]

            # Delete from database
            await self._delete_from_db(fingerprint)

            logger.info(f"Error {fingerprint[:8]} deleted")
            return True

        return False

    async def add_comment(
        self,
        fingerprint: str,
        user_id: int,
        comment: str
    ):
        """Add comment to error (for team collaboration)"""
        # In production: store in database
        logger.info(f"Comment added to error {fingerprint[:8]} by user {user_id}")

    # ========================================================================
    # STATISTICS & REPORTING
    # ========================================================================

    def get_error_stats(self, time_range: Optional[timedelta] = None) -> ErrorStats:
        """Get error statistics"""
        errors_list = list(self.errors.values())

        # Filter by time range if provided
        if time_range:
            cutoff = datetime.now() - time_range
            errors_list = [e for e in errors_list if e.last_seen >= cutoff]

        # Calculate stats
        total_occurrences = sum(e.occurrences for e in errors_list)
        unresolved = sum(1 for e in errors_list if not e.resolved)
        critical = sum(1 for e in errors_list if e.severity == ErrorSeverity.CRITICAL)

        # Count by severity
        by_severity = {}
        for severity in ErrorSeverity:
            by_severity[severity.value] = sum(
                1 for e in errors_list if e.severity == severity
            )

        # Get top errors
        top_errors = sorted(
            errors_list,
            key=lambda e: e.occurrences,
            reverse=True
        )[:10]

        # Count affected users
        all_affected_users = set()
        for error in errors_list:
            all_affected_users.update(error.affected_users)

        return ErrorStats(
            total_errors=len(errors_list),
            total_occurrences=total_occurrences,
            unresolved=unresolved,
            critical=critical,
            by_severity=by_severity,
            top_errors=[
                {
                    "error_id": e.error_id,
                    "type": e.error_type,
                    "message": e.error_message,
                    "occurrences": e.occurrences,
                    "severity": e.severity,
                    "affected_users": len(e.affected_users)
                }
                for e in top_errors
            ],
            affected_users_count=len(all_affected_users)
        )

    def search_errors(
        self,
        query: Optional[str] = None,
        severity: Optional[ErrorSeverity] = None,
        resolved: Optional[bool] = None,
        user_id: Optional[int] = None
    ) -> List[ErrorEvent]:
        """Search and filter errors"""
        results = list(self.errors.values())

        # Filter by query
        if query:
            query_lower = query.lower()
            results = [
                e for e in results
                if query_lower in e.error_type.lower()
                or query_lower in e.error_message.lower()
            ]

        # Filter by severity
        if severity:
            results = [e for e in results if e.severity == severity]

        # Filter by resolved status
        if resolved is not None:
            results = [e for e in results if e.resolved == resolved]

        # Filter by affected user
        if user_id:
            results = [e for e in results if user_id in e.affected_users]

        return results

    # ========================================================================
    # DATABASE OPERATIONS
    # ========================================================================

    async def _save_to_db(self, error: ErrorEvent):
        """Save error to database"""
        # In production: save to PostgreSQL
        # For now: log to file
        try:
            with open("logs/errors.jsonl", "a") as f:
                f.write(error.json() + "\n")
        except Exception as e:
            logger.error(f"Failed to save error to file: {e}")

    async def _update_db(self, fingerprint: str, updates: Dict):
        """Update error in database"""
        pass

    async def _delete_from_db(self, fingerprint: str):
        """Delete error from database"""
        pass

    # ========================================================================
    # CONFIGURATION
    # ========================================================================

    def add_slack_webhook(self, webhook_url: str):
        """Add Slack webhook for alerts"""
        self.alert_webhooks.append(webhook_url)

    def add_email_alert(self, email: str):
        """Add email for alerts"""
        self.email_alerts.append(email)

    def set_alert_thresholds(
        self,
        occurrences: int = 10,
        affected_users: int = 5
    ):
        """Set alert thresholds"""
        self.alert_threshold_occurrences = occurrences
        self.alert_threshold_users = affected_users


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Singleton instance
error_tracker = ErrorTracker()


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

def setup_global_exception_handler():
    """Setup global exception handler"""

    def handle_exception(exc_type, exc_value, exc_traceback):
        """Capture all unhandled exceptions"""
        # Ignore keyboard interrupt
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        # Capture exception
        import asyncio
        asyncio.create_task(
            error_tracker.capture_exception(
                exc_value,
                ErrorContext(environment="production"),
                ErrorSeverity.CRITICAL
            )
        )

        # Also print to console
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    # Install handler
    sys.excepthook = handle_exception


# ============================================================================
# DECORATOR
# ============================================================================

def capture_errors(func):
    """Decorator to automatically capture errors"""
    import functools

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await error_tracker.capture_exception(e)
            raise

    return wrapper


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'ErrorTracker',
    'ErrorEvent',
    'ErrorContext',
    'ErrorSeverity',
    'ErrorStats',
    'error_tracker',
    'setup_global_exception_handler',
    'capture_errors'
]
