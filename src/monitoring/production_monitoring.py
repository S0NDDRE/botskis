"""
Production Monitoring Setup
Sentry, Performance Monitoring, Uptime Checks
"""
import os
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from loguru import logger
from typing import Optional
import requests
import time

# ============================================================================
# SENTRY CONFIGURATION
# ============================================================================

def setup_sentry():
    """
    Initialize Sentry for error tracking and performance monitoring
    """
    sentry_dsn = os.getenv("SENTRY_DSN")
    environment = os.getenv("APP_ENV", "production")

    if not sentry_dsn:
        logger.warning("⚠️  SENTRY_DSN not configured - error tracking disabled")
        return

    try:
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=environment,

            # Integrations
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
                RedisIntegration(),
                LoggingIntegration(
                    level=None,  # Capture logs from all levels
                    event_level=None  # Don't create events from logs
                ),
            ],

            # Performance Monitoring
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),

            # Error Sampling
            sample_rate=1.0,  # Capture 100% of errors

            # Release Tracking
            release=os.getenv("APP_VERSION", "1.0.0"),

            # Additional Configuration
            send_default_pii=False,  # Don't send personally identifiable info
            attach_stacktrace=True,
            max_breadcrumbs=50,

            # Before Send Hook (filter sensitive data)
            before_send=filter_sensitive_data,
        )

        logger.success(f"✅ Sentry initialized (environment: {environment})")

    except Exception as e:
        logger.error(f"❌ Failed to initialize Sentry: {e}")


def filter_sensitive_data(event, hint):
    """
    Filter sensitive data before sending to Sentry

    Args:
        event: Sentry event dict
        hint: Additional context

    Returns:
        Modified event or None to drop event
    """
    # Remove sensitive data from request
    if "request" in event:
        request = event["request"]

        # Remove authorization headers
        if "headers" in request:
            headers = request["headers"]
            if "Authorization" in headers:
                headers["Authorization"] = "[FILTERED]"
            if "Cookie" in headers:
                headers["Cookie"] = "[FILTERED]"

        # Remove sensitive query parameters
        if "query_string" in request:
            sensitive_params = ["password", "token", "api_key", "secret"]
            query_string = request["query_string"]
            for param in sensitive_params:
                if param in query_string.lower():
                    request["query_string"] = "[FILTERED]"
                    break

    # Remove sensitive data from extra context
    if "extra" in event:
        sensitive_keys = ["password", "token", "api_key", "secret", "openai_api_key"]
        for key in list(event["extra"].keys()):
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                event["extra"][key] = "[FILTERED]"

    return event


# ============================================================================
# PERFORMANCE MONITORING
# ============================================================================

class PerformanceMonitor:
    """
    Monitor application performance metrics
    """

    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_error": 0,
            "avg_response_time": 0,
            "response_times": []
        }

    def record_request(self, success: bool, response_time: float):
        """
        Record request metrics

        Args:
            success: Whether request was successful
            response_time: Response time in seconds
        """
        self.metrics["requests_total"] += 1

        if success:
            self.metrics["requests_success"] += 1
        else:
            self.metrics["requests_error"] += 1

        self.metrics["response_times"].append(response_time)

        # Keep only last 1000 response times
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]

        # Update average
        self.metrics["avg_response_time"] = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])

    def get_metrics(self) -> dict:
        """Get current metrics"""
        return {
            "requests_total": self.metrics["requests_total"],
            "requests_success": self.metrics["requests_success"],
            "requests_error": self.metrics["requests_error"],
            "success_rate": (
                self.metrics["requests_success"] / self.metrics["requests_total"] * 100
                if self.metrics["requests_total"] > 0 else 0
            ),
            "avg_response_time_ms": self.metrics["avg_response_time"] * 1000,
            "p95_response_time_ms": (
                self._calculate_percentile(95) * 1000
                if self.metrics["response_times"] else 0
            ),
            "p99_response_time_ms": (
                self._calculate_percentile(99) * 1000
                if self.metrics["response_times"] else 0
            )
        }

    def _calculate_percentile(self, percentile: int) -> float:
        """Calculate percentile of response times"""
        if not self.metrics["response_times"]:
            return 0

        sorted_times = sorted(self.metrics["response_times"])
        index = int(len(sorted_times) * (percentile / 100))
        return sorted_times[min(index, len(sorted_times) - 1)]


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


# ============================================================================
# UPTIME MONITORING
# ============================================================================

class UptimeMonitor:
    """
    Monitor service uptime and availability
    """

    def __init__(self, check_interval: int = 60):
        """
        Initialize uptime monitor

        Args:
            check_interval: Interval between health checks in seconds
        """
        self.check_interval = check_interval
        self.endpoints_to_check = []
        self.last_check_results = {}

    def add_endpoint(self, name: str, url: str):
        """
        Add endpoint to monitor

        Args:
            name: Endpoint name
            url: URL to check
        """
        self.endpoints_to_check.append({
            "name": name,
            "url": url
        })
        logger.info(f"Added endpoint to uptime monitoring: {name} ({url})")

    def check_health(self) -> dict:
        """
        Check health of all registered endpoints

        Returns:
            Dict with health status of each endpoint
        """
        results = {}

        for endpoint in self.endpoints_to_check:
            try:
                start_time = time.time()
                response = requests.get(endpoint["url"], timeout=5)
                response_time = time.time() - start_time

                is_healthy = response.status_code == 200

                results[endpoint["name"]] = {
                    "status": "healthy" if is_healthy else "unhealthy",
                    "status_code": response.status_code,
                    "response_time_ms": response_time * 1000,
                    "timestamp": time.time()
                }

                if not is_healthy:
                    logger.warning(
                        f"⚠️  Endpoint {endpoint['name']} unhealthy: "
                        f"status_code={response.status_code}"
                    )

                    # Send Sentry alert
                    sentry_sdk.capture_message(
                        f"Endpoint {endpoint['name']} unhealthy",
                        level="warning",
                        extra=results[endpoint["name"]]
                    )

            except Exception as e:
                logger.error(f"❌ Failed to check endpoint {endpoint['name']}: {e}")
                results[endpoint["name"]] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                }

                # Send Sentry alert
                sentry_sdk.capture_exception(e)

        self.last_check_results = results
        return results

    def get_status(self) -> dict:
        """Get current uptime status"""
        return {
            "endpoints": self.last_check_results,
            "overall_status": (
                "healthy" if all(
                    r.get("status") == "healthy"
                    for r in self.last_check_results.values()
                ) else "degraded"
            )
        }


# Global uptime monitor instance
uptime_monitor = UptimeMonitor()


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

def get_health_status() -> dict:
    """
    Get comprehensive health status

    Returns:
        Health status dict
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "performance": performance_monitor.get_metrics(),
        "uptime": uptime_monitor.get_status(),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("APP_ENV", "production")
    }


# ============================================================================
# ALERT CONFIGURATION
# ============================================================================

def send_alert(title: str, message: str, level: str = "error"):
    """
    Send alert through configured channels

    Args:
        title: Alert title
        message: Alert message
        level: Alert level (error, warning, info)
    """
    # Send to Sentry
    if level == "error":
        sentry_sdk.capture_message(
            f"{title}: {message}",
            level="error"
        )
    elif level == "warning":
        sentry_sdk.capture_message(
            f"{title}: {message}",
            level="warning"
        )

    # Log alert
    if level == "error":
        logger.error(f"🚨 ALERT: {title} - {message}")
    elif level == "warning":
        logger.warning(f"⚠️  ALERT: {title} - {message}")
    else:
        logger.info(f"ℹ️  ALERT: {title} - {message}")

    # Send to other channels (email, Slack, etc.)
    # TODO: Implement email/Slack notifications


# ============================================================================
# INCIDENT TRACKING
# ============================================================================

class IncidentTracker:
    """
    Track and manage incidents
    """

    def __init__(self):
        self.active_incidents = []
        self.incident_history = []

    def create_incident(
        self,
        title: str,
        description: str,
        severity: str,
        affected_services: list
    ) -> dict:
        """
        Create new incident

        Args:
            title: Incident title
            description: Incident description
            severity: Severity level (critical, high, medium, low)
            affected_services: List of affected services

        Returns:
            Incident dict
        """
        incident = {
            "id": f"INC-{int(time.time())}",
            "title": title,
            "description": description,
            "severity": severity,
            "affected_services": affected_services,
            "status": "investigating",
            "created_at": time.time(),
            "updated_at": time.time(),
            "updates": []
        }

        self.active_incidents.append(incident)

        # Send alert
        send_alert(
            f"New Incident: {title}",
            f"Severity: {severity}\nAffected: {', '.join(affected_services)}\n{description}",
            level="error" if severity == "critical" else "warning"
        )

        logger.error(
            f"🚨 Incident Created: {incident['id']} - {title} "
            f"(severity: {severity})"
        )

        return incident

    def update_incident(self, incident_id: str, status: str, update_message: str):
        """
        Update incident status

        Args:
            incident_id: Incident ID
            status: New status (investigating, identified, monitoring, resolved)
            update_message: Update message
        """
        for incident in self.active_incidents:
            if incident["id"] == incident_id:
                incident["status"] = status
                incident["updated_at"] = time.time()
                incident["updates"].append({
                    "timestamp": time.time(),
                    "status": status,
                    "message": update_message
                })

                logger.info(
                    f"Incident Updated: {incident_id} - {status}: {update_message}"
                )

                # If resolved, move to history
                if status == "resolved":
                    self.active_incidents.remove(incident)
                    self.incident_history.append(incident)
                    logger.success(f"✅ Incident Resolved: {incident_id}")

                break

    def get_active_incidents(self) -> list:
        """Get all active incidents"""
        return self.active_incidents

    def get_incident_history(self, limit: int = 10) -> list:
        """Get incident history"""
        return self.incident_history[-limit:]


# Global incident tracker
incident_tracker = IncidentTracker()


# ============================================================================
# SETUP FUNCTION
# ============================================================================

def setup_production_monitoring():
    """
    Setup all production monitoring systems
    """
    logger.info("Setting up production monitoring...")

    # Initialize Sentry
    setup_sentry()

    # Configure uptime monitoring endpoints
    base_url = os.getenv("APP_URL", "http://localhost:8000")
    uptime_monitor.add_endpoint("API Health", f"{base_url}/health")
    uptime_monitor.add_endpoint("API Status", f"{base_url}/api/v1/status")
    uptime_monitor.add_endpoint("Income Bots", f"{base_url}/api/v1/income/stats")
    uptime_monitor.add_endpoint("Marketplace", f"{base_url}/api/v1/marketplace/agents")

    logger.success("✅ Production monitoring configured")
    logger.info("📊 Monitoring Features:")
    logger.info("  - Error tracking (Sentry)")
    logger.info("  - Performance monitoring")
    logger.info("  - Uptime monitoring")
    logger.info("  - Incident tracking")
    logger.info("  - Health checks")


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Setup monitoring
    setup_production_monitoring()

    # Check health
    health = get_health_status()
    logger.info(f"Health Status: {health}")

    # Example: Create incident
    incident = incident_tracker.create_incident(
        title="High Error Rate on Income Bots",
        description="Freelance bot experiencing 50% error rate",
        severity="high",
        affected_services=["income_bots", "freelance_bot"]
    )

    # Update incident
    incident_tracker.update_incident(
        incident["id"],
        status="identified",
        update_message="Root cause identified: OpenAI API rate limit"
    )

    incident_tracker.update_incident(
        incident["id"],
        status="resolved",
        update_message="Implemented retry logic with exponential backoff"
    )
