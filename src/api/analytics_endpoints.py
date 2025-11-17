"""
Analytics API Endpoints
REST API for Predictive Sales Engine and Advanced Dashboard
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from datetime import datetime

from src.analytics.predictive_sales_engine import (
    PredictiveSalesEngine,
    CustomerHealthMetrics,
    ChurnPrediction,
    LeadScoringResult,
    UpsellRecommendation,
    RevenueForecast
)
from src.analytics.advanced_dashboard import (
    AdvancedDashboard,
    TimeRange,
    KPIMetric
)
from src.auth.auth import get_current_user
from loguru import logger


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
sales_engine = PredictiveSalesEngine()
dashboard = AdvancedDashboard()


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@router.get("/dashboard")
async def get_dashboard_overview(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Get complete analytics dashboard overview

    Returns:
    - Key KPIs (MRR, growth, churn, etc.)
    - Revenue metrics
    - Customer metrics
    - Usage analytics
    - Sales performance
    - Top insights
    - Alerts
    """
    try:
        overview = await dashboard.get_dashboard_overview(time_range)
        logger.info(f"Dashboard accessed by user {current_user.get('id')}")
        return overview
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to load dashboard")


@router.get("/dashboard/kpis")
async def get_key_kpis(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Get key performance indicators

    Returns top-level KPIs:
    - MRR
    - Customer growth rate
    - Net revenue retention
    - Churn rate
    - LTV:CAC ratio
    - Active agents
    """
    try:
        kpis = await dashboard._get_key_kpis(time_range)
        return {"kpis": kpis, "time_range": time_range}
    except Exception as e:
        logger.error(f"KPI fetch error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch KPIs")


@router.get("/dashboard/revenue")
async def get_revenue_metrics(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed revenue metrics

    Returns:
    - MRR & ARR
    - New MRR, expansion, churn
    - NRR & GRR
    - ARPA
    - CAC & LTV:CAC ratio
    """
    try:
        revenue = await dashboard._get_revenue_metrics(time_range)
        return revenue
    except Exception as e:
        logger.error(f"Revenue metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch revenue metrics")


@router.get("/dashboard/customers")
async def get_customer_metrics(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Get customer health and growth metrics

    Returns:
    - Total customers
    - New & churned customers
    - Churn rate & growth rate
    - Customers by tier
    - At-risk customers
    """
    try:
        customers = await dashboard._get_customer_metrics(time_range)
        return customers
    except Exception as e:
        logger.error(f"Customer metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch customer metrics")


@router.get("/dashboard/usage")
async def get_usage_metrics(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Get platform usage analytics

    Returns:
    - Agent deployment stats
    - API call volume
    - Feature adoption rates
    - Most popular agents
    - DAU/WAU/MAU
    """
    try:
        usage = await dashboard._get_usage_metrics(time_range)
        return usage
    except Exception as e:
        logger.error(f"Usage metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch usage metrics")


@router.get("/dashboard/sales")
async def get_sales_metrics(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Get sales pipeline and performance

    Returns:
    - Lead funnel metrics
    - Conversion rates
    - Pipeline value
    - Win rate
    - Sales cycle duration
    """
    try:
        sales = await dashboard._get_sales_metrics(time_range)
        return sales
    except Exception as e:
        logger.error(f"Sales metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch sales metrics")


@router.get("/dashboard/realtime")
async def get_realtime_metrics(
    current_user: dict = Depends(get_current_user)
):
    """
    Get real-time metrics for live dashboard

    Returns:
    - Active users & agents
    - API calls per minute
    - System health
    - Recent activity
    """
    try:
        realtime = await dashboard.get_realtime_metrics()
        return realtime
    except Exception as e:
        logger.error(f"Realtime metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch realtime metrics")


# ============================================================================
# PREDICTIVE SALES ENDPOINTS
# ============================================================================

@router.post("/predict/churn")
async def predict_customer_churn(
    customer_id: int,
    health_metrics: CustomerHealthMetrics,
    current_user: dict = Depends(get_current_user)
) -> ChurnPrediction:
    """
    Predict customer churn probability

    Analyzes customer health metrics to predict:
    - Churn probability (0-100%)
    - Risk level (critical/high/medium/low/minimal)
    - Risk factors
    - Recommended prevention actions
    - Estimated revenue at risk
    """
    try:
        prediction = sales_engine.predict_churn(customer_id, health_metrics)
        logger.info(
            f"Churn prediction for customer {customer_id}: "
            f"{prediction.churn_probability:.1%} ({prediction.churn_risk})"
        )
        return prediction
    except Exception as e:
        logger.error(f"Churn prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to predict churn")


@router.get("/predict/churn/batch")
async def predict_churn_batch(
    customer_ids: List[int] = Query(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Batch churn prediction for multiple customers

    Returns churn predictions for all specified customers
    """
    try:
        # In production, fetch health metrics from database
        predictions = []
        for customer_id in customer_ids:
            # Mock health metrics - replace with actual DB fetch
            health = CustomerHealthMetrics(
                customer_id=customer_id,
                days_since_signup=180,
                days_since_last_login=5,
                total_logins=87,
                agents_deployed=3,
                agents_active=2,
                total_api_calls=12547,
                avg_daily_usage=125,
                feature_adoption_rate=0.65,
                support_tickets=2,
                billing_issues=0,
                subscription_tier="pro",
                mrr=99,
                ltv=4752,
                health_score=78.5
            )
            prediction = sales_engine.predict_churn(customer_id, health)
            predictions.append(prediction)

        return {"predictions": predictions, "total": len(predictions)}
    except Exception as e:
        logger.error(f"Batch churn prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to predict churn batch")


@router.post("/predict/lead-score")
async def score_lead(
    lead_id: int,
    company_size: int,
    industry: str,
    budget: float,
    pain_points: List[str],
    engagement_score: float,
    job_title: str,
    company_revenue: Optional[float] = None,
    current_user: dict = Depends(get_current_user)
) -> LeadScoringResult:
    """
    Score lead quality and conversion probability

    Analyzes lead attributes to calculate:
    - Lead score (0-100)
    - Lead quality (hot/warm/lukewarm/cold/frozen)
    - Conversion probability
    - Estimated LTV
    - Recommended nurture actions
    """
    try:
        score = sales_engine.score_lead(
            lead_id=lead_id,
            company_size=company_size,
            industry=industry,
            budget=budget,
            pain_points=pain_points,
            engagement_score=engagement_score,
            job_title=job_title,
            company_revenue=company_revenue
        )
        logger.info(
            f"Lead scored: {lead_id} = {score.lead_score:.0f}/100 "
            f"({score.lead_quality}, {score.conversion_probability:.0%} conversion)"
        )
        return score
    except Exception as e:
        logger.error(f"Lead scoring error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to score lead")


@router.get("/predict/upsell/{customer_id}")
async def get_upsell_opportunities(
    customer_id: int,
    current_user: dict = Depends(get_current_user)
) -> List[UpsellRecommendation]:
    """
    Identify upsell opportunities for customer

    Analyzes usage patterns to recommend:
    - Tier upgrades (Free -> Pro, Pro -> Enterprise)
    - Agent expansion
    - Multi-year commitments
    - Premium features

    Returns opportunities ranked by expected value
    """
    try:
        # In production, fetch from database
        # Mock data for demo
        usage_metrics = {
            "agents_deployed": 8,
            "agents_active": 7,
            "days_since_signup": 240,
            "feature_requests": ["custom_integrations", "white_label"]
        }

        opportunities = sales_engine.identify_upsell_opportunities(
            customer_id=customer_id,
            current_tier="pro",
            mrr=99,
            usage_metrics=usage_metrics
        )

        logger.info(f"Found {len(opportunities)} upsell opportunities for customer {customer_id}")
        return opportunities
    except Exception as e:
        logger.error(f"Upsell opportunity error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to identify upsell opportunities")


@router.get("/predict/revenue-forecast")
async def forecast_revenue(
    months: int = Query(6, ge=1, le=24),
    current_user: dict = Depends(get_current_user)
) -> List[RevenueForecast]:
    """
    Forecast future revenue

    Generates monthly revenue forecasts based on:
    - Historical growth trends
    - Churn rate patterns
    - Pipeline analysis
    - Seasonality

    Returns forecasts with confidence intervals
    """
    try:
        # In production, fetch historical data from database
        # Mock historical data
        historical_data = [
            {"period": "2024-08", "mrr": 350000, "total_customers": 1420, "churned": 45},
            {"period": "2024-09", "mrr": 380000, "total_customers": 1520, "churned": 48},
            {"period": "2024-10", "mrr": 410000, "total_customers": 1640, "churned": 52},
            {"period": "2024-11", "mrr": 445000, "total_customers": 1780, "churned": 57},
            {"period": "2024-12", "mrr": 487500, "total_customers": 1989, "churned": 63}
        ]

        forecasts = sales_engine.forecast_revenue(
            historical_data=historical_data,
            forecast_months=months
        )

        logger.info(f"Generated {months} month revenue forecast")
        return forecasts
    except Exception as e:
        logger.error(f"Revenue forecast error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to forecast revenue")


@router.get("/predict/ltv")
async def calculate_customer_ltv(
    monthly_revenue: float,
    avg_lifespan_months: int = 24,
    gross_margin: float = 0.80,
    current_user: dict = Depends(get_current_user)
):
    """
    Calculate Customer Lifetime Value (LTV)

    Formula: (Monthly Revenue × Customer Lifespan) × Gross Margin
    """
    try:
        ltv = sales_engine.calculate_ltv(
            monthly_revenue=monthly_revenue,
            avg_customer_lifespan_months=avg_lifespan_months,
            gross_margin=gross_margin
        )
        return {
            "ltv": ltv,
            "monthly_revenue": monthly_revenue,
            "lifespan_months": avg_lifespan_months,
            "gross_margin": gross_margin
        }
    except Exception as e:
        logger.error(f"LTV calculation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate LTV")


@router.get("/predict/roi")
async def calculate_sales_engine_roi(
    current_user: dict = Depends(get_current_user)
):
    """
    Calculate ROI of Predictive Sales Engine

    Shows value generated from:
    - Churn prevention
    - Upsell revenue
    - Sales efficiency gains

    Target: 450% ROI
    """
    try:
        from src.analytics.predictive_sales_engine import get_example_roi_metrics

        roi = get_example_roi_metrics()
        return roi
    except Exception as e:
        logger.error(f"ROI calculation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to calculate ROI")


# ============================================================================
# REPORTS ENDPOINTS
# ============================================================================

@router.get("/reports/executive")
async def generate_executive_report(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate executive summary report

    High-level overview for C-suite:
    - MRR & growth
    - Customer metrics
    - Key insights
    - Concerns & recommendations
    """
    try:
        report = await dashboard.generate_executive_report(time_range)
        logger.info(f"Executive report generated by user {current_user.get('id')}")
        return report
    except Exception as e:
        logger.error(f"Executive report error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate executive report")


@router.get("/reports/sales")
async def generate_sales_report(
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate sales team performance report

    Detailed sales metrics:
    - Pipeline value
    - Win rates
    - Sales cycle
    - Lead conversion
    - Quota attainment
    """
    try:
        report = await dashboard.generate_sales_report(time_range)
        logger.info(f"Sales report generated by user {current_user.get('id')}")
        return report
    except Exception as e:
        logger.error(f"Sales report error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate sales report")


@router.get("/reports/export")
async def export_dashboard_data(
    format: str = Query("json", regex="^(json|csv|pdf)$"),
    time_range: TimeRange = TimeRange.LAST_30_DAYS,
    current_user: dict = Depends(get_current_user)
):
    """
    Export dashboard data

    Supported formats:
    - json: JSON format
    - csv: CSV format (future)
    - pdf: PDF report (future)
    """
    try:
        export_data = await dashboard.export_dashboard_data(format, time_range)
        logger.info(f"Dashboard exported as {format} by user {current_user.get('id')}")
        return {"format": format, "data": export_data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to export dashboard data")


# ============================================================================
# MARKETPLACE ANALYTICS
# ============================================================================

@router.get("/marketplace")
async def get_marketplace_analytics(
    current_user: dict = Depends(get_current_user)
):
    """
    Get marketplace performance metrics

    Returns:
    - Total agents & downloads
    - Top performing agents
    - Category breakdown
    - Trending agents
    """
    try:
        analytics = await dashboard.get_marketplace_analytics()
        return analytics
    except Exception as e:
        logger.error(f"Marketplace analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch marketplace analytics")


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def analytics_health_check():
    """Check analytics engine health"""
    return {
        "status": "healthy",
        "service": "analytics",
        "sales_engine_version": sales_engine.model_version,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = ['router']
