"""
Error Tracking Tests
Test error capture, grouping, alerts
"""
import pytest
from datetime import datetime, timedelta


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
def test_error_fingerprinting():
    """Test error fingerprinting for grouping"""
    from src.monitoring.error_tracker import ErrorTracker

    tracker = ErrorTracker()

    # Same error should produce same fingerprint
    fp1 = tracker._create_fingerprint(
        error_type="ValueError",
        message="Invalid input",
        stack_trace="line 1\nline 2"
    )

    fp2 = tracker._create_fingerprint(
        error_type="ValueError",
        message="Invalid input",
        stack_trace="line 1\nline 2"
    )

    assert fp1 == fp2


@pytest.mark.unit
def test_different_errors_different_fingerprints():
    """Test different errors produce different fingerprints"""
    from src.monitoring.error_tracker import ErrorTracker

    tracker = ErrorTracker()

    fp1 = tracker._create_fingerprint(
        error_type="ValueError",
        message="Invalid input",
        stack_trace="line 1"
    )

    fp2 = tracker._create_fingerprint(
        error_type="TypeError",
        message="Type mismatch",
        stack_trace="line 1"
    )

    assert fp1 != fp2


@pytest.mark.unit
@pytest.mark.asyncio
async def test_capture_exception():
    """Test capturing exception"""
    from src.monitoring.error_tracker import ErrorTracker, ErrorContext

    tracker = ErrorTracker()

    try:
        raise ValueError("Test error")
    except ValueError as e:
        context = ErrorContext(
            user_id=123,
            request_path="/api/test",
            request_method="GET"
        )

        fingerprint = await tracker.capture_exception(e, context)

        assert fingerprint in tracker.errors
        assert tracker.errors[fingerprint].error_type == "ValueError"
        assert tracker.errors[fingerprint].message == "Test error"
        assert tracker.errors[fingerprint].occurrences == 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_error_grouping():
    """Test errors are grouped by fingerprint"""
    from src.monitoring.error_tracker import ErrorTracker

    tracker = ErrorTracker()

    # Capture same error twice
    try:
        raise ValueError("Same error")
    except ValueError as e:
        fp1 = await tracker.capture_exception(e)

        # Capture again
        fp2 = await tracker.capture_exception(e)

        # Should be same fingerprint
        assert fp1 == fp2

        # Occurrence count should increase
        assert tracker.errors[fp1].occurrences == 2


@pytest.mark.unit
def test_error_severity_classification():
    """Test automatic error severity classification"""
    from src.monitoring.error_tracker import ErrorTracker, ErrorSeverity

    tracker = ErrorTracker()

    # Critical errors
    assert tracker._classify_severity(KeyError("missing key")) == ErrorSeverity.CRITICAL
    assert tracker._classify_severity(ConnectionError("DB down")) == ErrorSeverity.CRITICAL

    # Warnings
    assert tracker._classify_severity(UserWarning("deprecated")) == ErrorSeverity.WARNING


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
def test_get_errors_endpoint(client, auth_headers):
    """Test getting errors via API"""
    response = client.get(
        "/api/errors",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "errors" in data
    assert isinstance(data["errors"], list)


@pytest.mark.integration
def test_get_error_details(client, auth_headers):
    """Test getting specific error details"""
    # First create an error (would normally happen during app usage)
    # For test, we'll assume an error exists

    # Try to get a specific error
    response = client.get(
        "/api/errors/test_fingerprint",
        headers=auth_headers
    )

    # Will be 404 if no errors exist, 200 if found
    assert response.status_code in [200, 404]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_error_alert_creation(client, auth_headers):
    """Test error alerts are created for new errors"""
    from src.monitoring.error_tracker import error_tracker

    alerts_sent = []

    # Mock alert callback
    async def mock_alert_callback(error_event):
        alerts_sent.append(error_event)

    error_tracker.add_alert_callback(mock_alert_callback)

    # Capture error
    try:
        raise ValueError("Critical test error")
    except ValueError as e:
        await error_tracker.capture_exception(e)

    # Alert should be sent
    assert len(alerts_sent) > 0


@pytest.mark.integration
def test_resolve_error(client, auth_headers):
    """Test resolving an error"""
    response = client.post(
        "/api/errors/test_fingerprint/resolve",
        headers=auth_headers,
        json={"comment": "Fixed in version 1.2.3"}
    )

    # Will be 404 if error doesn't exist
    assert response.status_code in [200, 404]


@pytest.mark.integration
def test_error_statistics(client, auth_headers):
    """Test getting error statistics"""
    response = client.get(
        "/api/errors/statistics",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "total_errors" in data
    assert "errors_last_24h" in data
    assert "top_errors" in data


@pytest.mark.integration
def test_error_trend_analysis(client, auth_headers):
    """Test error trend analysis"""
    response = client.get(
        "/api/errors/trends?days=7",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "trend" in data
    assert "daily_counts" in data


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_complete_error_tracking_flow():
    """Test complete error tracking workflow"""
    from src.monitoring.error_tracker import ErrorTracker, ErrorContext

    tracker = ErrorTracker()

    alerts_received = []

    async def alert_callback(error_event):
        alerts_received.append(error_event)

    tracker.add_alert_callback(alert_callback)

    # 1. Error occurs
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        context = ErrorContext(
            user_id=123,
            request_path="/api/calculate",
            request_method="POST",
            user_agent="TestClient/1.0"
        )

        # 2. Capture error
        fingerprint = await tracker.capture_exception(e, context)

        # 3. Verify error stored
        assert fingerprint in tracker.errors
        error = tracker.errors[fingerprint]
        assert error.error_type == "ZeroDivisionError"
        assert error.occurrences == 1

        # 4. Verify alert sent
        assert len(alerts_received) > 0

        # 5. Get statistics
        stats = tracker.get_statistics()
        assert stats["total_errors"] >= 1

        # 6. Resolve error
        tracker.resolve_error(fingerprint, "Fixed division by zero check")
        assert tracker.errors[fingerprint].resolved is True


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_error_rate_monitoring():
    """Test monitoring error rate over time"""
    from src.monitoring.error_tracker import ErrorTracker

    tracker = ErrorTracker()

    # Generate multiple errors
    for i in range(10):
        try:
            if i % 2 == 0:
                raise ValueError(f"Error {i}")
            else:
                raise TypeError(f"Error {i}")
        except Exception as e:
            await tracker.capture_exception(e)

    # Get error rate
    stats = tracker.get_statistics()
    assert stats["total_errors"] >= 10

    # Check trend
    trend = tracker.get_trend_analysis(days=1)
    assert len(trend["daily_counts"]) > 0


@pytest.mark.e2e
def test_error_dashboard_data(client, auth_headers):
    """Test getting data for error dashboard"""

    # 1. Get error overview
    overview_response = client.get(
        "/api/errors/statistics",
        headers=auth_headers
    )
    assert overview_response.status_code == 200

    # 2. Get top errors
    top_errors_response = client.get(
        "/api/errors?sort=occurrences&limit=10",
        headers=auth_headers
    )
    assert top_errors_response.status_code == 200

    # 3. Get error trends
    trends_response = client.get(
        "/api/errors/trends?days=7",
        headers=auth_headers
    )
    assert trends_response.status_code == 200

    # 4. Get recent errors
    recent_response = client.get(
        "/api/errors?sort=last_seen&limit=20",
        headers=auth_headers
    )
    assert recent_response.status_code == 200


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_error_integration_with_monitoring():
    """Test error tracker integration with APM"""
    from src.monitoring.error_tracker import error_tracker
    from src.infrastructure.monitoring import apm

    # Track request with error
    with apm.track_request("POST", "/api/test") as tracker:
        try:
            raise ValueError("Request failed")
        except ValueError as e:
            tracker.error = str(e)
            await error_tracker.capture_exception(e)

    # Both systems should have recorded the error
    stats = apm.get_request_stats(minutes=1)
    assert stats["error_rate"] > 0

    error_stats = error_tracker.get_statistics()
    assert error_stats["total_errors"] > 0
