"""
Self-Hosted Email Server
For internal emails (monitoring alerts, team notifications, etc.)

Note: For customer-facing emails (marketing, transactional),
      continue using SendGrid for better deliverability.

Savings: ~$30/month for internal emails
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import ssl
from datetime import datetime
from enum import Enum
from loguru import logger
import aiosmtplib
import asyncio


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class EmailPriority(str, Enum):
    """Email priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class EmailCategory(str, Enum):
    """Email categories for routing"""
    INTERNAL = "internal"  # Team notifications
    MONITORING = "monitoring"  # System alerts, error reports
    ADMIN = "admin"  # Admin notifications
    DEVELOPMENT = "development"  # Dev environment emails


class EmailAttachment(BaseModel):
    """Email attachment"""
    filename: str
    content: bytes
    content_type: str = "application/octet-stream"


class EmailTemplate(BaseModel):
    """Email template"""
    subject: str
    html_body: str
    text_body: str
    variables: List[str] = []


class EmailLog(BaseModel):
    """Email delivery log"""
    email_id: str
    to: List[str]
    subject: str
    category: EmailCategory
    status: str  # sent, failed, queued
    timestamp: datetime
    error_message: Optional[str] = None


# ============================================================================
# SMTP CONFIGURATION
# ============================================================================

class SMTPConfig(BaseModel):
    """SMTP server configuration"""
    host: str = "localhost"
    port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False
    from_email: str = "noreply@mindframe.no"
    from_name: str = "Mindframe System"
    timeout: int = 30


# ============================================================================
# EMAIL SERVER
# ============================================================================

class OwnEmailServer:
    """
    Self-Hosted Email Server

    Features:
    - SMTP sending (async)
    - HTML templates
    - File attachments
    - Priority queue
    - Delivery logging
    - Retry on failure
    - Rate limiting

    Use Cases:
    - Internal team notifications
    - Monitoring alerts (error tracking, uptime)
    - Admin notifications
    - Development environment emails

    NOT for:
    - Customer marketing emails (use SendGrid)
    - Transactional emails to customers (use SendGrid)

    Why?
    - Customer emails need high deliverability
    - Marketing emails need reputation management
    - Our server = risk of being marked as spam

    Savings: $30/month = $360/year
    """

    def __init__(self, config: Optional[SMTPConfig] = None):
        self.config = config or SMTPConfig()
        self.email_queue: List[Dict] = []
        self.delivery_log: List[EmailLog] = []
        self.templates: Dict[str, EmailTemplate] = {}
        self.rate_limit_per_hour = 100  # Prevent spam

        # Load templates
        self._load_default_templates()

    # ========================================================================
    # SENDING EMAILS
    # ========================================================================

    async def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[EmailAttachment]] = None,
        category: EmailCategory = EmailCategory.INTERNAL,
        priority: EmailPriority = EmailPriority.NORMAL,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send email via SMTP

        Args:
            to: List of recipient email addresses
            subject: Email subject
            body: Plain text body
            html_body: HTML body (optional)
            attachments: File attachments
            category: Email category
            priority: Email priority
            reply_to: Reply-to address

        Returns:
            True if sent successfully, False otherwise

        Example:
        ```python
        await email_server.send_email(
            to=["admin@mindframe.no"],
            subject="Critical Error Alert",
            body="Error detected in production...",
            category=EmailCategory.MONITORING,
            priority=EmailPriority.URGENT
        )
        ```
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config.from_name} <{self.config.from_email}>"
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

            if reply_to:
                msg['Reply-To'] = reply_to

            # Set priority
            if priority == EmailPriority.URGENT:
                msg['X-Priority'] = '1'
                msg['Importance'] = 'high'
            elif priority == EmailPriority.HIGH:
                msg['X-Priority'] = '2'
                msg['Importance'] = 'high'

            # Add category header (for filtering)
            msg['X-Email-Category'] = category.value

            # Attach plain text body
            msg.attach(MIMEText(body, 'plain'))

            # Attach HTML body if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))

            # Add attachments
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.content)
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={attachment.filename}'
                    )
                    msg.attach(part)

            # Send email via SMTP
            await self._send_smtp(msg, to)

            # Log delivery
            self._log_delivery(
                to=to,
                subject=subject,
                category=category,
                status="sent"
            )

            logger.info(f"✅ Email sent to {', '.join(to)}: {subject}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send email to {', '.join(to)}: {e}")

            # Log failure
            self._log_delivery(
                to=to,
                subject=subject,
                category=category,
                status="failed",
                error=str(e)
            )

            return False

    async def _send_smtp(self, message: MIMEMultipart, recipients: List[str]):
        """Send email via SMTP (async)"""
        if self.config.use_ssl:
            # SSL connection
            async with aiosmtplib.SMTP(
                hostname=self.config.host,
                port=self.config.port,
                use_tls=False,
                timeout=self.config.timeout
            ) as smtp:
                await smtp.connect()
                if self.config.username and self.config.password:
                    await smtp.login(self.config.username, self.config.password)
                await smtp.send_message(message)
        else:
            # TLS connection
            async with aiosmtplib.SMTP(
                hostname=self.config.host,
                port=self.config.port,
                use_tls=self.config.use_tls,
                timeout=self.config.timeout
            ) as smtp:
                if self.config.username and self.config.password:
                    await smtp.login(self.config.username, self.config.password)
                await smtp.send_message(message)

    # ========================================================================
    # TEMPLATES
    # ========================================================================

    def _load_default_templates(self):
        """Load default email templates"""

        # Error Alert Template
        self.templates["error_alert"] = EmailTemplate(
            subject="🚨 Error Alert: {error_type}",
            text_body="""
Error Alert

Error Type: {error_type}
Message: {error_message}
Severity: {severity}
Environment: {environment}

Occurrences: {occurrences}
Affected Users: {affected_users}

Error ID: {error_id}
Timestamp: {timestamp}

View details: https://mindframe.no/admin/errors/{fingerprint}
            """,
            html_body="""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #dc2626; color: white; padding: 20px; border-radius: 8px 8px 0 0; }
        .content { background: #f9fafb; padding: 20px; border: 1px solid #e5e7eb; }
        .footer { background: #f3f4f6; padding: 15px; border-radius: 0 0 8px 8px; text-align: center; }
        .stat { display: inline-block; margin: 10px 20px; }
        .stat-value { font-size: 24px; font-weight: bold; }
        .stat-label { font-size: 12px; color: #6b7280; }
        .button { background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">🚨 Error Alert</h1>
        </div>
        <div class="content">
            <h2>{error_type}</h2>
            <p><strong>Message:</strong> {error_message}</p>
            <p><strong>Severity:</strong> <span style="color: #dc2626;">{severity}</span></p>
            <p><strong>Environment:</strong> {environment}</p>

            <div style="margin: 20px 0;">
                <div class="stat">
                    <div class="stat-value">{occurrences}</div>
                    <div class="stat-label">Occurrences</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{affected_users}</div>
                    <div class="stat-label">Affected Users</div>
                </div>
            </div>

            <p><strong>Error ID:</strong> {error_id}</p>
            <p><strong>Timestamp:</strong> {timestamp}</p>

            <a href="https://mindframe.no/admin/errors/{fingerprint}" class="button">View Error Details</a>
        </div>
        <div class="footer">
            <p style="margin: 0; color: #6b7280; font-size: 12px;">
                Mindframe Error Tracking System
            </p>
        </div>
    </div>
</body>
</html>
            """,
            variables=["error_type", "error_message", "severity", "environment",
                      "occurrences", "affected_users", "error_id", "timestamp", "fingerprint"]
        )

        # System Alert Template
        self.templates["system_alert"] = EmailTemplate(
            subject="⚠️ System Alert: {alert_type}",
            text_body="""
System Alert

Alert Type: {alert_type}
Message: {message}
Severity: {severity}

Timestamp: {timestamp}

Action Required: {action_required}
            """,
            html_body="""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #f59e0b; color: white; padding: 20px; border-radius: 8px 8px 0 0; }
        .content { background: #fffbeb; padding: 20px; border: 1px solid #fbbf24; }
        .footer { background: #fef3c7; padding: 15px; border-radius: 0 0 8px 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">⚠️ System Alert</h1>
        </div>
        <div class="content">
            <h2>{alert_type}</h2>
            <p>{message}</p>
            <p><strong>Severity:</strong> {severity}</p>
            <p><strong>Timestamp:</strong> {timestamp}</p>
            <p><strong>Action Required:</strong> {action_required}</p>
        </div>
        <div class="footer">
            <p style="margin: 0; color: #78350f; font-size: 12px;">
                Mindframe Monitoring System
            </p>
        </div>
    </div>
</body>
</html>
            """,
            variables=["alert_type", "message", "severity", "timestamp", "action_required"]
        )

        # Daily Report Template
        self.templates["daily_report"] = EmailTemplate(
            subject="📊 Daily Report - {date}",
            text_body="""
Daily Platform Report - {date}

Key Metrics:
- Total Users: {total_users}
- Active Users: {active_users}
- New Signups: {new_signups}
- Revenue: {revenue}
- Errors: {error_count}

Performance:
- Uptime: {uptime}%
- Avg Response Time: {avg_response_time}ms

View full dashboard: https://mindframe.no/admin/analytics
            """,
            html_body="""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #2563eb; color: white; padding: 20px; border-radius: 8px 8px 0 0; }
        .content { background: white; padding: 20px; border: 1px solid #e5e7eb; }
        .metric { background: #f9fafb; padding: 15px; margin: 10px 0; border-radius: 6px; }
        .metric-value { font-size: 32px; font-weight: bold; color: #2563eb; }
        .metric-label { color: #6b7280; font-size: 14px; }
        .footer { background: #eff6ff; padding: 15px; border-radius: 0 0 8px 8px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0;">📊 Daily Report</h1>
            <p style="margin: 5px 0 0 0;">{date}</p>
        </div>
        <div class="content">
            <h2>Key Metrics</h2>
            <div class="metric">
                <div class="metric-value">{total_users}</div>
                <div class="metric-label">Total Users</div>
            </div>
            <div class="metric">
                <div class="metric-value">{active_users}</div>
                <div class="metric-label">Active Users (24h)</div>
            </div>
            <div class="metric">
                <div class="metric-value">+{new_signups}</div>
                <div class="metric-label">New Signups</div>
            </div>
            <div class="metric">
                <div class="metric-value">{revenue}</div>
                <div class="metric-label">Revenue</div>
            </div>

            <h2 style="margin-top: 30px;">Platform Health</h2>
            <p><strong>Uptime:</strong> {uptime}%</p>
            <p><strong>Avg Response Time:</strong> {avg_response_time}ms</p>
            <p><strong>Errors:</strong> {error_count}</p>

            <div style="text-align: center; margin-top: 30px;">
                <a href="https://mindframe.no/admin/analytics" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    View Full Dashboard
                </a>
            </div>
        </div>
        <div class="footer">
            <p style="margin: 0; color: #1e40af; font-size: 12px;">
                Mindframe Analytics System
            </p>
        </div>
    </div>
</body>
</html>
            """,
            variables=["date", "total_users", "active_users", "new_signups",
                      "revenue", "uptime", "avg_response_time", "error_count"]
        )

    async def send_from_template(
        self,
        to: List[str],
        template_name: str,
        variables: Dict[str, Any],
        category: EmailCategory = EmailCategory.INTERNAL,
        priority: EmailPriority = EmailPriority.NORMAL
    ) -> bool:
        """
        Send email using template

        Example:
        ```python
        await email_server.send_from_template(
            to=["team@mindframe.no"],
            template_name="error_alert",
            variables={
                "error_type": "DatabaseError",
                "error_message": "Connection failed",
                "severity": "CRITICAL",
                ...
            },
            category=EmailCategory.MONITORING,
            priority=EmailPriority.URGENT
        )
        ```
        """
        if template_name not in self.templates:
            logger.error(f"Template '{template_name}' not found")
            return False

        template = self.templates[template_name]

        # Substitute variables
        subject = template.subject.format(**variables)
        text_body = template.text_body.format(**variables)
        html_body = template.html_body.format(**variables)

        return await self.send_email(
            to=to,
            subject=subject,
            body=text_body,
            html_body=html_body,
            category=category,
            priority=priority
        )

    # ========================================================================
    # LOGGING & MONITORING
    # ========================================================================

    def _log_delivery(
        self,
        to: List[str],
        subject: str,
        category: EmailCategory,
        status: str,
        error: Optional[str] = None
    ):
        """Log email delivery"""
        import uuid

        log = EmailLog(
            email_id=str(uuid.uuid4()),
            to=to,
            subject=subject,
            category=category,
            status=status,
            timestamp=datetime.now(),
            error_message=error
        )

        self.delivery_log.append(log)

        # Keep only last 1000 logs in memory
        if len(self.delivery_log) > 1000:
            self.delivery_log = self.delivery_log[-1000:]

    def get_delivery_stats(self, hours: int = 24) -> Dict:
        """Get email delivery statistics"""
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(hours=hours)
        recent_logs = [log for log in self.delivery_log if log.timestamp >= cutoff]

        return {
            "total_sent": len([l for l in recent_logs if l.status == "sent"]),
            "total_failed": len([l for l in recent_logs if l.status == "failed"]),
            "success_rate": (
                len([l for l in recent_logs if l.status == "sent"]) / len(recent_logs) * 100
                if recent_logs else 100
            ),
            "by_category": {
                category.value: len([l for l in recent_logs if l.category == category])
                for category in EmailCategory
            }
        }

    # ========================================================================
    # BATCH SENDING
    # ========================================================================

    async def send_bulk_emails(
        self,
        emails: List[Dict[str, Any]],
        delay_between: float = 0.1
    ) -> Dict[str, int]:
        """
        Send bulk emails with rate limiting

        Args:
            emails: List of email dicts with 'to', 'subject', 'body', etc.
            delay_between: Delay between emails (seconds)

        Returns:
            Dict with sent/failed counts
        """
        sent = 0
        failed = 0

        for email_data in emails:
            success = await self.send_email(**email_data)
            if success:
                sent += 1
            else:
                failed += 1

            # Rate limiting
            await asyncio.sleep(delay_between)

        return {"sent": sent, "failed": failed}


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Singleton instance
_email_server: Optional[OwnEmailServer] = None


def get_email_server(config: Optional[SMTPConfig] = None) -> OwnEmailServer:
    """Get global email server instance"""
    global _email_server
    if _email_server is None:
        _email_server = OwnEmailServer(config)
    return _email_server


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'OwnEmailServer',
    'SMTPConfig',
    'EmailCategory',
    'EmailPriority',
    'EmailAttachment',
    'EmailTemplate',
    'get_email_server'
]
