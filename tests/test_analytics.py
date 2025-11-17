"""
Analytics Tests
Test predictive sales engine, dashboards, metrics
"""
import pytest
from datetime import datetime, timedelta


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
def test_calculate_lead_score():
    """Test lead scoring algorithm"""
    from src.analytics.predictive_sales import calculate_lead_score

    lead_data = {
        "email_opens": 5,
        "page_views": 10,
        "demo_requested": True,
        "company_size": "enterprise",
        "budget": "high"
    }

    score = calculate_lead_score(lead_data)

    assert 0 <= score <= 100
    assert isinstance(score, (int, float))


@pytest.mark.unit
def test_predict_churn_probability():
    """Test churn prediction"""
    from src.analytics.predictive_sales import predict_churn

    customer_data = {
        "last_login": datetime.now() - timedelta(days=30),
        "support_tickets": 5,
        "usage_decline": 0.4,  # 40% decline
        "payment_delays": 2
    }

    churn_prob = predict_churn(customer_data)

    assert 0 <= churn_prob <= 1.0
    assert churn_prob > 0.5  # High risk


@pytest.mark.unit
def test_revenue_forecast():
    """Test revenue forecasting"""
    from src.analytics.predictive_sales import forecast_revenue

    historical_data = [
        {"month": "2024-01", "revenue": 10000},
        {"month": "2024-02", "revenue": 12000},
        {"month": "2024-03", "revenue": 15000},
        {"month": "2024-04", "revenue": 18000},
    ]

    forecast = forecast_revenue(historical_data, months_ahead=3)

    assert len(forecast) == 3
    assert all(f["revenue"] > 0 for f in forecast)
    # Revenue should be trending upward
    assert forecast[2]["revenue"] > forecast[0]["revenue"]


@pytest.mark.unit
def test_conversion_funnel_analysis():
    """Test conversion funnel calculation"""
    from src.analytics.conversion_funnel import analyze_funnel

    funnel_data = {
        "visits": 1000,
        "signups": 200,
        "trials": 100,
        "paid": 25
    }

    analysis = analyze_funnel(funnel_data)

    assert analysis["signup_rate"] == 0.2  # 20%
    assert analysis["trial_rate"] == 0.5  # 50%
    assert analysis["conversion_rate"] == 0.25  # 25%


@pytest.mark.unit
def test_cohort_retention_calculation():
    """Test cohort retention analysis"""
    from src.analytics.cohort_analysis import calculate_retention

    cohort_data = {
        "cohort": "2024-01",
        "month_0": 100,  # Initial users
        "month_1": 80,   # 80% retained
        "month_2": 65,   # 65% retained
        "month_3": 55    # 55% retained
    }

    retention = calculate_retention(cohort_data)

    assert retention["month_1"] == 0.80
    assert retention["month_2"] == 0.65
    assert retention["month_3"] == 0.55


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
def test_get_dashboard_metrics(client, auth_headers):
    """Test getting dashboard metrics"""
    response = client.get(
        "/api/analytics/dashboard",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    # Check key metrics present
    assert "total_users" in data
    assert "active_users" in data
    assert "revenue" in data
    assert "growth_rate" in data


@pytest.mark.integration
def test_get_sales_forecast(client, auth_headers):
    """Test getting sales forecast"""
    response = client.get(
        "/api/analytics/forecast?months=6",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "forecast" in data
    assert len(data["forecast"]) == 6
    assert all("month" in f and "revenue" in f for f in data["forecast"])


@pytest.mark.integration
def test_get_top_leads(client, auth_headers):
    """Test getting top leads by score"""
    response = client.get(
        "/api/analytics/leads/top?limit=10",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "leads" in data
    assert len(data["leads"]) <= 10

    # Leads should be sorted by score (highest first)
    if len(data["leads"]) > 1:
        scores = [lead["score"] for lead in data["leads"]]
        assert scores == sorted(scores, reverse=True)


@pytest.mark.integration
def test_get_churn_risk_customers(client, auth_headers):
    """Test getting customers at risk of churning"""
    response = client.get(
        "/api/analytics/churn-risk?threshold=0.7",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "customers" in data

    # All customers should have high churn probability
    if data["customers"]:
        assert all(c["churn_probability"] >= 0.7 for c in data["customers"])


@pytest.mark.integration
def test_conversion_funnel_endpoint(client, auth_headers):
    """Test conversion funnel endpoint"""
    response = client.get(
        "/api/analytics/funnel?period=30d",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "funnel" in data
    funnel = data["funnel"]

    # Check funnel stages
    expected_stages = ["visits", "signups", "trials", "paid"]
    for stage in expected_stages:
        assert stage in funnel


@pytest.mark.integration
def test_cohort_analysis_endpoint(client, auth_headers):
    """Test cohort analysis endpoint"""
    response = client.get(
        "/api/analytics/cohorts?months=6",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "cohorts" in data
    assert isinstance(data["cohorts"], list)


@pytest.mark.integration
def test_export_analytics_data(client, auth_headers):
    """Test exporting analytics data"""
    response = client.get(
        "/api/analytics/export?format=csv&metric=revenue",
        headers=auth_headers
    )

    assert response.status_code == 200
    # CSV export
    assert "text/csv" in response.headers.get("content-type", "")


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
def test_complete_analytics_workflow(client, auth_headers):
    """Test complete analytics workflow"""

    # 1. Get overview dashboard
    dashboard_response = client.get(
        "/api/analytics/dashboard",
        headers=auth_headers
    )

    assert dashboard_response.status_code == 200
    dashboard = dashboard_response.json()

    # 2. Drill down into revenue forecast
    forecast_response = client.get(
        "/api/analytics/forecast?months=3",
        headers=auth_headers
    )

    assert forecast_response.status_code == 200
    forecast = forecast_response.json()["forecast"]

    # 3. Check conversion funnel
    funnel_response = client.get(
        "/api/analytics/funnel?period=30d",
        headers=auth_headers
    )

    assert funnel_response.status_code == 200
    funnel = funnel_response.json()["funnel"]

    # 4. Identify top leads
    leads_response = client.get(
        "/api/analytics/leads/top?limit=5",
        headers=auth_headers
    )

    assert leads_response.status_code == 200
    top_leads = leads_response.json()["leads"]

    # 5. Find churn risks
    churn_response = client.get(
        "/api/analytics/churn-risk?threshold=0.6",
        headers=auth_headers
    )

    assert churn_response.status_code == 200
    at_risk = churn_response.json()["customers"]

    # Verify complete workflow
    assert "revenue" in dashboard
    assert len(forecast) == 3
    assert "visits" in funnel


@pytest.mark.e2e
def test_predictive_sales_recommendations(client, auth_headers):
    """Test getting AI-powered sales recommendations"""

    # Get recommendations
    response = client.get(
        "/api/analytics/recommendations",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "recommendations" in data
    recommendations = data["recommendations"]

    # Each recommendation should have:
    # - action (what to do)
    # - reason (why)
    # - impact (expected outcome)
    # - priority (high/medium/low)
    if recommendations:
        rec = recommendations[0]
        assert "action" in rec
        assert "reason" in rec
        assert "priority" in rec


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_real_time_analytics_updates():
    """Test real-time analytics updates"""
    from src.analytics.real_time_tracker import RealTimeTracker

    tracker = RealTimeTracker()

    # Track events
    await tracker.track_event("user.signup", {"user_id": 123})
    await tracker.track_event("page.view", {"page": "/pricing"})
    await tracker.track_event("purchase", {"amount": 99.00})

    # Get real-time stats
    stats = await tracker.get_current_stats()

    assert stats["events_last_minute"] >= 3


@pytest.mark.e2e
def test_ab_test_analysis(client, auth_headers):
    """Test A/B test analysis"""

    # Create A/B test
    create_response = client.post(
        "/api/analytics/ab-tests",
        headers=auth_headers,
        json={
            "name": "Pricing Page Test",
            "variant_a": "original",
            "variant_b": "new_design",
            "metric": "conversion_rate"
        }
    )

    assert create_response.status_code == 201
    test_id = create_response.json()["test_id"]

    # Get test results
    results_response = client.get(
        f"/api/analytics/ab-tests/{test_id}/results",
        headers=auth_headers
    )

    assert results_response.status_code == 200
    results = results_response.json()

    assert "variant_a" in results
    assert "variant_b" in results
    assert "statistical_significance" in results


@pytest.mark.e2e
def test_custom_analytics_query(client, auth_headers):
    """Test custom analytics query builder"""

    response = client.post(
        "/api/analytics/query",
        headers=auth_headers,
        json={
            "metric": "revenue",
            "dimensions": ["country", "product"],
            "filters": {
                "date_range": "last_30_days",
                "country": ["NO", "SE", "DK"]
            },
            "aggregation": "sum"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert "results" in data
    assert isinstance(data["results"], list)
