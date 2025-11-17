"""
Email Server API Endpoints
Self-hosted email for internal use
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr

from src.email.own_email_server import (
    get_email_server,
    EmailCategory,
    EmailPriority,
    EmailAttachment,
    SMTPConfig
)
from src.auth.auth_manager import get_current_user


# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(prefix="/api/email", tags=["Email Server"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class SendEmailRequest(BaseModel):
    """Request to send email"""
    to: List[EmailStr]
    subject: str
    body: str
    html_body: Optional[str] = None
    category: EmailCategory = EmailCategory.INTERNAL
    priority: EmailPriority = EmailPriority.NORMAL
    reply_to: Optional[EmailStr] = None


class SendTemplateEmailRequest(BaseModel):
    """Request to send templated email"""
    to: List[EmailStr]
    template_name: str
    variables: Dict[str, Any]
    category: EmailCategory = EmailCategory.INTERNAL
    priority: EmailPriority = EmailPriority.NORMAL


class BulkEmailRequest(BaseModel):
    """Request to send bulk emails"""
    emails: List[SendEmailRequest]
    delay_between: float = 0.1


class ConfigureEmailServerRequest(BaseModel):
    """Request to configure email server"""
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: Optional[bool] = None
    from_email: Optional[EmailStr] = None
    from_name: Optional[str] = None


# ============================================================================
# EMAIL SENDING ENDPOINTS
# ============================================================================

@router.post("/send")
async def send_email(
    request: SendEmailRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send email via self-hosted SMTP server

    For internal use only (monitoring, alerts, team notifications)

    Example:
    ```python
    POST /api/email/send
    {
        "to": ["admin@mindframe.no"],
        "subject": "Critical Error Alert",
        "body": "Error detected in production...",
        "category": "monitoring",
        "priority": "urgent"
    }
    ```
    """
    try:
        email_server = get_email_server()

        success = await email_server.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            html_body=request.html_body,
            category=request.category,
            priority=request.priority,
            reply_to=request.reply_to
        )

        if success:
            return {
                "success": True,
                "message": f"Email sent to {len(request.to)} recipient(s)"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send/template")
async def send_template_email(
    request: SendTemplateEmailRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send email using template

    Available templates:
    - error_alert: Error tracking alerts
    - system_alert: System monitoring alerts
    - daily_report: Daily analytics report

    Example:
    ```python
    POST /api/email/send/template
    {
        "to": ["team@mindframe.no"],
        "template_name": "error_alert",
        "variables": {
            "error_type": "DatabaseError",
            "error_message": "Connection timeout",
            "severity": "CRITICAL",
            "environment": "production",
            "occurrences": 15,
            "affected_users": 3,
            "error_id": "abc123",
            "timestamp": "2025-01-16 14:30:00",
            "fingerprint": "def456"
        },
        "category": "monitoring",
        "priority": "urgent"
    }
    ```
    """
    try:
        email_server = get_email_server()

        success = await email_server.send_from_template(
            to=request.to,
            template_name=request.template_name,
            variables=request.variables,
            category=request.category,
            priority=request.priority
        )

        if success:
            return {
                "success": True,
                "message": f"Template email '{request.template_name}' sent to {len(request.to)} recipient(s)"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send template email (template may not exist)"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send/bulk")
async def send_bulk_emails(
    request: BulkEmailRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send bulk emails with rate limiting

    Use for batch notifications, daily reports, etc.

    Max: 100 emails per request
    """
    try:
        if len(request.emails) > 100:
            raise HTTPException(
                status_code=400,
                detail="Maximum 100 emails per bulk request"
            )

        email_server = get_email_server()

        # Convert to dict format
        emails_data = [email.dict() for email in request.emails]

        result = await email_server.send_bulk_emails(
            emails=emails_data,
            delay_between=request.delay_between
        )

        return {
            "success": True,
            "sent": result["sent"],
            "failed": result["failed"],
            "total": len(request.emails)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# TEMPLATES
# ============================================================================

@router.get("/templates")
async def list_templates(
    current_user: dict = Depends(get_current_user)
):
    """
    List available email templates

    Returns template names and required variables
    """
    try:
        email_server = get_email_server()

        templates_info = []
        for name, template in email_server.templates.items():
            templates_info.append({
                "name": name,
                "subject": template.subject,
                "variables": template.variables
            })

        return {
            "success": True,
            "templates": templates_info,
            "total": len(templates_info)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/{template_name}")
async def get_template(
    template_name: str,
    current_user: dict = Depends(get_current_user)
):
    """Get template details"""
    try:
        email_server = get_email_server()

        if template_name not in email_server.templates:
            raise HTTPException(status_code=404, detail="Template not found")

        template = email_server.templates[template_name]

        return {
            "success": True,
            "template": {
                "name": template_name,
                "subject": template.subject,
                "text_body": template.text_body,
                "html_body": template.html_body,
                "variables": template.variables
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS & MONITORING
# ============================================================================

@router.get("/stats")
async def get_email_stats(
    hours: int = 24,
    current_user: dict = Depends(get_current_user)
):
    """
    Get email delivery statistics

    Query params:
    - hours: Time range (default: 24)

    Returns:
    - Total sent/failed
    - Success rate
    - Breakdown by category
    """
    try:
        email_server = get_email_server()

        stats = email_server.get_delivery_stats(hours=hours)

        return {
            "success": True,
            "stats": stats,
            "time_range_hours": hours
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/logs")
async def get_email_logs(
    limit: int = 100,
    category: Optional[EmailCategory] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get email delivery logs

    Query params:
    - limit: Number of logs to return (max 1000)
    - category: Filter by category
    - status: Filter by status (sent/failed)
    """
    try:
        email_server = get_email_server()

        logs = email_server.delivery_log

        # Filter by category
        if category:
            logs = [log for log in logs if log.category == category]

        # Filter by status
        if status:
            logs = [log for log in logs if log.status == status]

        # Sort by timestamp (newest first)
        logs.sort(key=lambda log: log.timestamp, reverse=True)

        # Limit
        logs = logs[:min(limit, 1000)]

        return {
            "success": True,
            "logs": [log.dict() for log in logs],
            "total": len(logs)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CONFIGURATION
# ============================================================================

@router.post("/config")
async def configure_email_server(
    request: ConfigureEmailServerRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Configure email server settings

    Requires admin privileges

    Example:
    ```python
    POST /api/email/config
    {
        "host": "smtp.gmail.com",
        "port": 587,
        "username": "noreply@mindframe.no",
        "password": "app_password",
        "use_tls": true,
        "from_email": "noreply@mindframe.no",
        "from_name": "Mindframe Platform"
    }
    ```
    """
    try:
        # Check admin privileges
        if not current_user.get("is_admin"):
            raise HTTPException(
                status_code=403,
                detail="Admin privileges required"
            )

        email_server = get_email_server()

        # Update config
        if request.host:
            email_server.config.host = request.host
        if request.port:
            email_server.config.port = request.port
        if request.username:
            email_server.config.username = request.username
        if request.password:
            email_server.config.password = request.password
        if request.use_tls is not None:
            email_server.config.use_tls = request.use_tls
        if request.from_email:
            email_server.config.from_email = request.from_email
        if request.from_name:
            email_server.config.from_name = request.from_name

        return {
            "success": True,
            "message": "Email server configuration updated"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_email_config(
    current_user: dict = Depends(get_current_user)
):
    """Get current email server configuration (sanitized)"""
    try:
        email_server = get_email_server()

        return {
            "success": True,
            "config": {
                "host": email_server.config.host,
                "port": email_server.config.port,
                "use_tls": email_server.config.use_tls,
                "use_ssl": email_server.config.use_ssl,
                "from_email": email_server.config.from_email,
                "from_name": email_server.config.from_name,
                "username": email_server.config.username,
                "password": "***" if email_server.config.password else None
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
    try:
        email_server = get_email_server()

        return {
            "success": True,
            "service": "Email Server",
            "status": "operational",
            "config_host": email_server.config.host,
            "templates_loaded": len(email_server.templates)
        }

    except Exception as e:
        return {
            "success": False,
            "service": "Email Server",
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = ['router']
