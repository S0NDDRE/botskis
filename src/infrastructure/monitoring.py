"""
Application Performance Monitoring (APM)
Real-time monitoring and alerting

Features:
- Request/response tracking
- Performance metrics
- Resource monitoring (CPU, RAM, Disk)
- Real-time alerts (Slack, Email)
- Health checks
- Uptime monitoring
- Automatic issue detection
"""
from typing import Dict, List, Optional, Callable
from pydantic import BaseModel
from datetime import datetime, timedelta
from collections import deque
import time
import psutil
import asyncio
from loguru import logger
from enum import Enum


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class AlertSeverity(str, Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class HealthStatus(str, Enum):
    """Health check status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class RequestMetric(BaseModel):
    """HTTP request metric"""
    request_id: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    timestamp: datetime
    user_id: Optional[int] = None
    error: Optional[str] = None


class PerformanceMetric(BaseModel):
    """Performance metrics snapshot"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    disk_percent: float
    active_connections: int
    requests_per_second: float
    avg_response_time_ms: float
    error_rate: float


class Alert(BaseModel):
    """System alert"""
    alert_id: str
    severity: AlertSeverity
    title: str
    message: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class HealthCheck(BaseModel):
    """Component health check"""
    component: str
    status: HealthStatus
    message: str
    last_check: datetime
    response_time_ms: Optional[float] = None


# ============================================================================
# APM MONITOR
# ============================================================================

class APMMonitor:
    """
    Application Performance Monitoring

    Tracks:
    - Request/response metrics
    - System resources (CPU, RAM, Disk)
    - Performance trends
    - Automatic alerts

    Features:
    - Real-time monitoring
    - Historical data
    - Automatic issue detection
    - Alerting (Slack, Email)

    Usage:
    ```python
    # Track request
    with apm.track_request("GET", "/api/users") as tracker:
        response = await handle_request()
        tracker.status_code = 200

    # Check system health
    health = await apm.get_system_health()
    if health.status == HealthStatus.UNHEALTHY:
        await apm.alert("System unhealthy!")
    ```
    """

    def __init__(self):
        # Request metrics (keep last 10,000)
        self.request_metrics: deque = deque(maxlen=10000)

        # Performance snapshots (keep last 1440 = 24h if 1/min)
        self.performance_history: deque = deque(maxlen=1440)

        # Active alerts
        self.alerts: List[Alert] = []

        # Health checks
        self.health_checks: Dict[str, HealthCheck] = {}

        # Alert thresholds
        self.thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0,
            "error_rate": 5.0,  # %
            "response_time_ms": 1000.0
        }

        # Alert callbacks
        self.alert_callbacks: List[Callable] = []

        # Start background monitoring
        self.monitoring = False
        self.monitor_task: Optional[asyncio.Task] = None

    # ========================================================================
    # REQUEST TRACKING
    # ========================================================================

    class RequestTracker:
        """Context manager for tracking requests"""

        def __init__(self, monitor: 'APMMonitor', method: str, path: str):
            self.monitor = monitor
            self.method = method
            self.path = path
            self.start_time = time.time()
            self.status_code: Optional[int] = None
            self.error: Optional[str] = None
            self.user_id: Optional[int] = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            duration_ms = (time.time() - self.start_time) * 1000

            # Track error if occurred
            if exc_type:
                self.error = str(exc_val)
                self.status_code = 500

            # Record metric
            metric = RequestMetric(
                request_id=str(time.time()),
                method=self.method,
                path=self.path,
                status_code=self.status_code or 500,
                duration_ms=duration_ms,
                timestamp=datetime.now(),
                user_id=self.user_id,
                error=self.error
            )

            self.monitor.request_metrics.append(metric)

            # Check for slow requests
            if duration_ms > self.monitor.thresholds["response_time_ms"]:
                logger.warning(
                    f"⚠️  Slow request: {self.method} {self.path} "
                    f"({duration_ms:.0f}ms)"
                )

    def track_request(self, method: str, path: str) -> RequestTracker:
        """
        Track HTTP request

        Example:
        ```python
        with apm.track_request("GET", "/api/users") as tracker:
            users = await get_users()
            tracker.status_code = 200
            tracker.user_id = current_user.id
            return users
        ```
        """
        return self.RequestTracker(self, method, path)

    # ========================================================================
    # SYSTEM MONITORING
    # ========================================================================

    async def get_system_metrics(self) -> PerformanceMetric:
        """Get current system metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_mb = memory.used / (1024 * 1024)

        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent

        # Network connections
        try:
            connections = len(psutil.net_connections(kind='inet'))
        except:
            connections = 0

        # Calculate request metrics
        recent_requests = [
            m for m in self.request_metrics
            if m.timestamp > datetime.now() - timedelta(seconds=60)
        ]

        requests_per_second = len(recent_requests) / 60.0

        if recent_requests:
            avg_response_time = sum(m.duration_ms for m in recent_requests) / len(recent_requests)
            error_count = sum(1 for m in recent_requests if m.status_code >= 500)
            error_rate = (error_count / len(recent_requests)) * 100
        else:
            avg_response_time = 0.0
            error_rate = 0.0

        metric = PerformanceMetric(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            memory_mb=memory_mb,
            disk_percent=disk_percent,
            active_connections=connections,
            requests_per_second=requests_per_second,
            avg_response_time_ms=avg_response_time,
            error_rate=error_rate
        )

        return metric

    async def start_monitoring(self, interval_seconds: int = 60):
        """
        Start background monitoring

        Collects metrics every N seconds
        """
        self.monitoring = True

        async def monitor_loop():
            while self.monitoring:
                try:
                    # Collect metrics
                    metrics = await self.get_system_metrics()
                    self.performance_history.append(metrics)

                    # Check thresholds and alert
                    await self._check_thresholds(metrics)

                except Exception as e:
                    logger.error(f"Monitoring error: {e}")

                await asyncio.sleep(interval_seconds)

        self.monitor_task = asyncio.create_task(monitor_loop())
        logger.info(f"📊 Monitoring started (interval: {interval_seconds}s)")

    async def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        if self.monitor_task:
            await self.monitor_task
        logger.info("⏸️  Monitoring stopped")

    async def _check_thresholds(self, metrics: PerformanceMetric):
        """Check if metrics exceed thresholds and alert"""

        # CPU threshold
        if metrics.cpu_percent > self.thresholds["cpu_percent"]:
            await self.create_alert(
                severity=AlertSeverity.WARNING,
                title="High CPU Usage",
                message=f"CPU usage at {metrics.cpu_percent:.1f}% (threshold: {self.thresholds['cpu_percent']}%)"
            )

        # Memory threshold
        if metrics.memory_percent > self.thresholds["memory_percent"]:
            await self.create_alert(
                severity=AlertSeverity.WARNING,
                title="High Memory Usage",
                message=f"Memory usage at {metrics.memory_percent:.1f}% (threshold: {self.thresholds['memory_percent']}%)"
            )

        # Disk threshold
        if metrics.disk_percent > self.thresholds["disk_percent"]:
            await self.create_alert(
                severity=AlertSeverity.ERROR,
                title="High Disk Usage",
                message=f"Disk usage at {metrics.disk_percent:.1f}% (threshold: {self.thresholds['disk_percent']}%)"
            )

        # Error rate threshold
        if metrics.error_rate > self.thresholds["error_rate"]:
            await self.create_alert(
                severity=AlertSeverity.ERROR,
                title="High Error Rate",
                message=f"Error rate at {metrics.error_rate:.1f}% (threshold: {self.thresholds['error_rate']}%)"
            )

        # Response time threshold
        if metrics.avg_response_time_ms > self.thresholds["response_time_ms"]:
            await self.create_alert(
                severity=AlertSeverity.WARNING,
                title="Slow Response Time",
                message=f"Avg response time {metrics.avg_response_time_ms:.0f}ms (threshold: {self.thresholds['response_time_ms']}ms)"
            )

    # ========================================================================
    # HEALTH CHECKS
    # ========================================================================

    async def register_health_check(
        self,
        component: str,
        check_func: Callable
    ):
        """
        Register health check for component

        Example:
        ```python
        async def check_database():
            try:
                await db.execute("SELECT 1")
                return HealthStatus.HEALTHY, "Database connected"
            except Exception as e:
                return HealthStatus.UNHEALTHY, f"Database error: {e}"

        await apm.register_health_check("database", check_database)
        ```
        """
        try:
            start_time = time.time()
            status, message = await check_func()
            response_time = (time.time() - start_time) * 1000

            health_check = HealthCheck(
                component=component,
                status=status,
                message=message,
                last_check=datetime.now(),
                response_time_ms=response_time
            )

            self.health_checks[component] = health_check

            # Alert if unhealthy
            if status == HealthStatus.UNHEALTHY:
                await self.create_alert(
                    severity=AlertSeverity.CRITICAL,
                    title=f"{component} Unhealthy",
                    message=message
                )

        except Exception as e:
            health_check = HealthCheck(
                component=component,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {e}",
                last_check=datetime.now()
            )
            self.health_checks[component] = health_check

    async def get_system_health(self) -> Dict:
        """Get overall system health"""
        if not self.health_checks:
            return {
                "status": HealthStatus.HEALTHY,
                "message": "No health checks configured",
                "components": {}
            }

        # Determine overall status
        statuses = [hc.status for hc in self.health_checks.values()]

        if HealthStatus.UNHEALTHY in statuses:
            overall_status = HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in statuses:
            overall_status = HealthStatus.DEGRADED
        else:
            overall_status = HealthStatus.HEALTHY

        return {
            "status": overall_status,
            "components": {
                name: hc.dict() for name, hc in self.health_checks.items()
            },
            "last_updated": datetime.now()
        }

    # ========================================================================
    # ALERTING
    # ========================================================================

    async def create_alert(
        self,
        severity: AlertSeverity,
        title: str,
        message: str
    ):
        """Create and send alert"""
        import uuid

        # Check if similar alert already exists (prevent spam)
        existing = [
            a for a in self.alerts
            if a.title == title and not a.resolved
        ]

        if existing:
            logger.debug(f"Alert already exists: {title}")
            return

        alert = Alert(
            alert_id=str(uuid.uuid4()),
            severity=severity,
            title=title,
            message=message,
            timestamp=datetime.now()
        )

        self.alerts.append(alert)

        # Log alert
        logger.warning(f"🚨 ALERT [{severity}]: {title} - {message}")

        # Send to alert callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Alert callback failed: {e}")

    def add_alert_callback(self, callback: Callable):
        """
        Add alert callback (Slack, Email, etc.)

        Example:
        ```python
        async def send_to_slack(alert: Alert):
            await slack.send_message(
                channel="#alerts",
                text=f"[{alert.severity}] {alert.title}: {alert.message}"
            )

        apm.add_alert_callback(send_to_slack)
        ```
        """
        self.alert_callbacks.append(callback)

    # ========================================================================
    # STATISTICS
    # ========================================================================

    def get_request_stats(self, minutes: int = 60) -> Dict:
        """Get request statistics for last N minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        recent = [m for m in self.request_metrics if m.timestamp > cutoff]

        if not recent:
            return {
                "total_requests": 0,
                "requests_per_minute": 0.0,
                "avg_response_time_ms": 0.0,
                "error_rate": 0.0,
                "status_codes": {}
            }

        # Calculate stats
        total_requests = len(recent)
        requests_per_minute = total_requests / minutes

        avg_response_time = sum(m.duration_ms for m in recent) / total_requests

        error_count = sum(1 for m in recent if m.status_code >= 500)
        error_rate = (error_count / total_requests) * 100

        # Group by status code
        status_codes = {}
        for metric in recent:
            code = metric.status_code
            status_codes[code] = status_codes.get(code, 0) + 1

        return {
            "total_requests": total_requests,
            "requests_per_minute": requests_per_minute,
            "avg_response_time_ms": avg_response_time,
            "error_rate": error_rate,
            "status_codes": status_codes,
            "time_range_minutes": minutes
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Singleton APM monitor
apm = APMMonitor()


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'APMMonitor',
    'RequestMetric',
    'PerformanceMetric',
    'Alert',
    'HealthCheck',
    'AlertSeverity',
    'HealthStatus',
    'apm'
]
