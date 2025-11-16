"""
Error Tracking API Endpoints
Self-hosted error tracking (replaces Sentry)
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel

from src.monitoring.error_tracker import (
    error_tracker,
    ErrorContext,
    ErrorSeverity,
    ErrorEvent
)
from src.auth.auth_manager import get_current_user


# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/api/errors", tags=["Error Tracking"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class CaptureExceptionRequest(BaseModel):
    """Request to capture exception"""
    error_type: str
    error_message: str
    stack_trace: str
    context: Optional[ErrorContext] = None
    severity: ErrorSeverity = ErrorSeverity.ERROR


class CaptureMessageRequest(BaseModel):
    """Request to capture custom message"""
    message: str
    level: ErrorSeverity = ErrorSeverity.INFO
    context: Optional[ErrorContext] = None


class ResolveErrorRequest(BaseModel):
    """Request to resolve error"""
    resolved_by: int


class AddCommentRequest(BaseModel):
    """Request to add comment to error"""
    user_id: int
    comment: str


class ErrorSearchParams(BaseModel):
    """Search parameters"""
    query: Optional[str] = None
    severity: Optional[ErrorSeverity] = None
    resolved: Optional[bool] = None
    user_id: Optional[int] = None
    time_range_days: Optional[int] = None


class ConfigureAlertsRequest(BaseModel):
    """Configure alert settings"""
    slack_webhooks: Optional[List[str]] = None
    email_alerts: Optional[List[str]] = None
    threshold_occurrences: Optional[int] = None
    threshold_users: Optional[int] = None


# ============================================================================
# ERROR CAPTURE ENDPOINTS
# ============================================================================

@router.post("/capture/exception")
async def capture_exception(
    request: CaptureExceptionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Capture exception manually

    Usually called from frontend error boundaries or catch blocks

    Example:
    ```javascript
    try {
        riskyOperation()
    } catch (error) {
        await fetch('/api/errors/capture/exception', {
            method: 'POST',
            body: JSON.stringify({
                error_type: error.name,
                error_message: error.message,
                stack_trace: error.stack,
                context: {
                    user_id: currentUser.id,
                    url: window.location.href,
                    user_agent: navigator.userAgent
                }
            })
        })
    }
    ```
    """
    try:
        # Create exception from string data
        class CapturedError(Exception):
            pass

        error = CapturedError(request.error_message)
        error.__traceback__ = None  # Stack trace provided separately

        # Add user context if not provided
        context = request.context or ErrorContext()
        if not context.user_id and current_user:
            context.user_id = current_user.get("id")

        fingerprint = await error_tracker.capture_exception(
            error,
            context=context,
            severity=request.severity
        )

        return {
            "success": True,
            "fingerprint": fingerprint,
            "error_id": fingerprint[:8],
            "message": "Exception captured successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/capture/message")
async def capture_message(
    request: CaptureMessageRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Capture custom message/event

    Use for logging important events that aren't exceptions

    Example:
    ```python
    await error_tracker.capture_message(
        "Payment failed for user 123",
        level=ErrorSeverity.WARNING
    )
    ```
    """
    try:
        context = request.context or ErrorContext()
        if not context.user_id and current_user:
            context.user_id = current_user.get("id")

        await error_tracker.capture_message(
            request.message,
            level=request.level,
            context=context
        )

        return {
            "success": True,
            "message": "Message captured successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ERROR LISTING & SEARCH
# ============================================================================

@router.get("/list")
async def list_errors(
    severity: Optional[ErrorSeverity] = None,
    resolved: Optional[bool] = None,
    limit: int = Query(50, le=100),
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    List all errors with pagination

    Query params:
    - severity: Filter by severity level
    - resolved: Filter by resolved status (true/false)
    - limit: Number of results (max 100)
    - offset: Pagination offset
    """
    try:
        # Get all errors
        errors = list(error_tracker.errors.values())

        # Filter by severity
        if severity:
            errors = [e for e in errors if e.severity == severity]

        # Filter by resolved status
        if resolved is not None:
            errors = [e for e in errors if e.resolved == resolved]

        # Sort by last seen (newest first)
        errors.sort(key=lambda e: e.last_seen, reverse=True)

        # Pagination
        total = len(errors)
        errors = errors[offset:offset + limit]

        return {
            "success": True,
            "total": total,
            "errors": [e.dict() for e in errors],
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search_errors(
    params: ErrorSearchParams,
    current_user: dict = Depends(get_current_user)
):
    """
    Search errors with advanced filtering

    Filters:
    - query: Search in error type and message
    - severity: Filter by severity level
    - resolved: Filter by resolved status
    - user_id: Filter by affected user
    - time_range_days: Only errors from last N days
    """
    try:
        results = error_tracker.search_errors(
            query=params.query,
            severity=params.severity,
            resolved=params.resolved,
            user_id=params.user_id
        )

        # Filter by time range
        if params.time_range_days:
            cutoff = datetime.now() - timedelta(days=params.time_range_days)
            results = [e for e in results if e.last_seen >= cutoff]

        # Sort by occurrences (most frequent first)
        results.sort(key=lambda e: e.occurrences, reverse=True)

        return {
            "success": True,
            "total": len(results),
            "errors": [e.dict() for e in results]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{fingerprint}")
async def get_error_details(
    fingerprint: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about specific error

    Returns full error event with stack trace, context, occurrences, etc.
    """
    try:
        if fingerprint not in error_tracker.errors:
            raise HTTPException(status_code=404, detail="Error not found")

        error = error_tracker.errors[fingerprint]

        return {
            "success": True,
            "error": error.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ERROR MANAGEMENT
# ============================================================================

@router.post("/{fingerprint}/resolve")
async def resolve_error(
    fingerprint: str,
    request: ResolveErrorRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark error as resolved

    Resolved errors are excluded from active error counts
    """
    try:
        success = await error_tracker.resolve_error(
            fingerprint,
            resolved_by=request.resolved_by
        )

        if not success:
            raise HTTPException(status_code=404, detail="Error not found")

        return {
            "success": True,
            "message": f"Error {fingerprint[:8]} marked as resolved"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{fingerprint}")
async def delete_error(
    fingerprint: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Permanently delete error

    Use with caution - this cannot be undone
    """
    try:
        success = await error_tracker.delete_error(fingerprint)

        if not success:
            raise HTTPException(status_code=404, detail="Error not found")

        return {
            "success": True,
            "message": f"Error {fingerprint[:8]} deleted permanently"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{fingerprint}/comment")
async def add_comment(
    fingerprint: str,
    request: AddCommentRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Add comment to error for team collaboration

    Comments are useful for documenting investigation progress
    """
    try:
        if fingerprint not in error_tracker.errors:
            raise HTTPException(status_code=404, detail="Error not found")

        await error_tracker.add_comment(
            fingerprint,
            user_id=request.user_id,
            comment=request.comment
        )

        return {
            "success": True,
            "message": "Comment added successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS & REPORTING
# ============================================================================

@router.get("/stats/overview")
async def get_error_statistics(
    time_range_days: Optional[int] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get error statistics and overview

    Returns:
    - Total errors
    - Total occurrences
    - Unresolved count
    - Critical count
    - Breakdown by severity
    - Top 10 most frequent errors
    - Affected users count
    """
    try:
        time_range = timedelta(days=time_range_days) if time_range_days else None

        stats = error_tracker.get_error_stats(time_range=time_range)

        return {
            "success": True,
            "stats": stats.dict(),
            "time_range_days": time_range_days
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/trends")
async def get_error_trends(
    days: int = Query(7, le=90),
    current_user: dict = Depends(get_current_user)
):
    """
    Get error trends over time

    Returns daily error counts for the last N days
    """
    try:
        # Group errors by day
        trends = {}
        now = datetime.now()

        for i in range(days):
            day = (now - timedelta(days=i)).date()
            trends[str(day)] = {
                "date": str(day),
                "total_errors": 0,
                "total_occurrences": 0,
                "critical": 0,
                "errors": 0,
                "warnings": 0
            }

        # Count errors for each day
        for error in error_tracker.errors.values():
            day = error.last_seen.date()
            day_str = str(day)

            if day_str in trends:
                trends[day_str]["total_errors"] += 1
                trends[day_str]["total_occurrences"] += error.occurrences

                if error.severity == ErrorSeverity.CRITICAL:
                    trends[day_str]["critical"] += 1
                elif error.severity == ErrorSeverity.ERROR:
                    trends[day_str]["errors"] += 1
                elif error.severity == ErrorSeverity.WARNING:
                    trends[day_str]["warnings"] += 1

        # Convert to list and sort
        trend_list = list(trends.values())
        trend_list.sort(key=lambda x: x["date"])

        return {
            "success": True,
            "trends": trend_list,
            "days": days
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONFIGURATION
# ============================================================================

@router.post("/config/alerts")
async def configure_alerts(
    request: ConfigureAlertsRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Configure alert settings

    Settings:
    - slack_webhooks: List of Slack webhook URLs
    - email_alerts: List of email addresses for alerts
    - threshold_occurrences: Alert after N occurrences
    - threshold_users: Alert if N users affected
    """
    try:
        # Add Slack webhooks
        if request.slack_webhooks:
            for webhook in request.slack_webhooks:
                error_tracker.add_slack_webhook(webhook)

        # Add email alerts
        if request.email_alerts:
            for email in request.email_alerts:
                error_tracker.add_email_alert(email)

        # Set thresholds
        if request.threshold_occurrences or request.threshold_users:
            error_tracker.set_alert_thresholds(
                occurrences=request.threshold_occurrences or 10,
                affected_users=request.threshold_users or 5
            )

        return {
            "success": True,
            "message": "Alert configuration updated",
            "config": {
                "slack_webhooks": len(error_tracker.alert_webhooks),
                "email_alerts": len(error_tracker.email_alerts),
                "threshold_occurrences": error_tracker.alert_threshold_occurrences,
                "threshold_users": error_tracker.alert_threshold_users
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_configuration(
    current_user: dict = Depends(get_current_user)
):
    """Get current error tracking configuration"""
    try:
        return {
            "success": True,
            "config": {
                "slack_webhooks_count": len(error_tracker.alert_webhooks),
                "email_alerts_count": len(error_tracker.email_alerts),
                "threshold_occurrences": error_tracker.alert_threshold_occurrences,
                "threshold_users": error_tracker.alert_threshold_users,
                "total_errors_tracked": len(error_tracker.errors)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check endpoint (no auth required)"""
    return {
        "success": True,
        "service": "Error Tracking",
        "status": "operational",
        "errors_tracked": len(error_tracker.errors)
    }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = ['router']
