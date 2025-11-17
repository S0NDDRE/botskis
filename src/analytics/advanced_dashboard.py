"""
Advanced Analytics Dashboard
Real-time business intelligence and KPI tracking
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from enum import Enum
import json


# ============================================================================
# DASHBOARD METRICS
# ============================================================================

class MetricTrend(str, Enum):
    """Metric trend direction"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


class TimeRange(str, Enum):
    """Time range for analytics"""
    TODAY = "today"
    YESTERDAY = "yesterday"
    LAST_7_DAYS = "last_7_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"
    THIS_MONTH = "this_month"
    LAST_MONTH = "last_month"
    THIS_QUARTER = "this_quarter"
    THIS_YEAR = "this_year"
    ALL_TIME = "all_time"


class KPIMetric(BaseModel):
    """Key Performance Indicator metric"""
    name: str
    value: float
    previous_value: float
    change_percentage: float
    trend: MetricTrend
    target: Optional[float] = None
    unit: str = ""  # "$", "%", "users", etc.
    description: str


class RevenueMetrics(BaseModel):
    """Revenue and financial metrics"""
    mrr: float  # Monthly Recurring Revenue
    arr: float  # Annual Recurring Revenue
    new_mrr: float  # New MRR this period
    expansion_mrr: float  # Upsells/cross-sells
    churned_mrr: float  # Lost MRR
    net_new_mrr: float  # Net change
    net_revenue_retention: float  # NRR %
    gross_revenue_retention: float  # GRR %
    average_revenue_per_account: float  # ARPA
    customer_acquisition_cost: float  # CAC
    ltv_cac_ratio: float  # LTV:CAC ratio
    months_to_recover_cac: int


class CustomerMetrics(BaseModel):
    """Customer growth and health metrics"""
    total_customers: int
    new_customers: int
    churned_customers: int
    active_customers: int
    inactive_customers: int
    customer_churn_rate: float  # %
    customer_growth_rate: float  # %
    average_customer_age_days: int
    customers_by_tier: Dict[str, int]
    customers_at_risk: int  # High churn risk


class UsageMetrics(BaseModel):
    """Platform usage and engagement metrics"""
    total_agents_deployed: int
    active_agents: int
    total_api_calls: int
    average_api_calls_per_customer: float
    total_automations_executed: int
    total_hours_saved: float
    feature_adoption_rates: Dict[str, float]
    most_popular_agents: List[Dict[str, any]]
    daily_active_users: int
    weekly_active_users: int
    monthly_active_users: int


class SalesMetrics(BaseModel):
    """Sales pipeline and performance metrics"""
    total_leads: int
    qualified_leads: int
    hot_leads: int
    conversion_rate: float  # %
    average_deal_size: float
    sales_cycle_days: int
    win_rate: float  # %
    pipeline_value: float
    weighted_pipeline: float
    quota_attainment: float  # %


# ============================================================================
# ANALYTICS DASHBOARD
# ============================================================================

class AdvancedDashboard:
    """
    Advanced Analytics Dashboard

    Real-time business intelligence with:
    - Revenue metrics (MRR, ARR, NRR)
    - Customer health & growth
    - Usage analytics
    - Sales performance
    - Agent marketplace stats
    - Predictive insights
    """

    def __init__(self):
        self.cache_ttl = 300  # 5 minutes cache
        self._cache = {}

    # ========================================================================
    # MAIN DASHBOARD
    # ========================================================================

    async def get_dashboard_overview(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS
    ) -> Dict:
        """
        Get complete dashboard overview

        Returns all KPIs and metrics for executive dashboard
        """
        return {
            "generated_at": datetime.now().isoformat(),
            "time_range": time_range,
            "kpis": await self._get_key_kpis(time_range),
            "revenue": await self._get_revenue_metrics(time_range),
            "customers": await self._get_customer_metrics(time_range),
            "usage": await self._get_usage_metrics(time_range),
            "sales": await self._get_sales_metrics(time_range),
            "top_insights": await self._get_top_insights(),
            "alerts": await self._get_alerts()
        }

    async def _get_key_kpis(self, time_range: TimeRange) -> List[KPIMetric]:
        """Get top-level KPIs for dashboard"""
        # In production, fetch from database
        # This is sample data structure
        return [
            KPIMetric(
                name="Monthly Recurring Revenue",
                value=487500,
                previous_value=425000,
                change_percentage=14.7,
                trend=MetricTrend.UP,
                target=500000,
                unit="$",
                description="Total MRR from all active subscriptions"
            ),
            KPIMetric(
                name="Customer Growth Rate",
                value=12.5,
                previous_value=9.8,
                change_percentage=27.6,
                trend=MetricTrend.UP,
                target=15.0,
                unit="%",
                description="Month-over-month customer growth"
            ),
            KPIMetric(
                name="Net Revenue Retention",
                value=118,
                previous_value=112,
                change_percentage=5.4,
                trend=MetricTrend.UP,
                target=120,
                unit="%",
                description="Revenue retention including expansion"
            ),
            KPIMetric(
                name="Customer Churn Rate",
                value=3.2,
                previous_value=4.5,
                change_percentage=-28.9,
                trend=MetricTrend.DOWN,  # Down is good for churn
                target=3.0,
                unit="%",
                description="Monthly customer churn rate"
            ),
            KPIMetric(
                name="LTV:CAC Ratio",
                value=4.8,
                previous_value=4.2,
                change_percentage=14.3,
                trend=MetricTrend.UP,
                target=5.0,
                unit="x",
                description="Customer lifetime value to acquisition cost"
            ),
            KPIMetric(
                name="Active Agents",
                value=3847,
                previous_value=3201,
                change_percentage=20.2,
                trend=MetricTrend.UP,
                target=5000,
                unit="agents",
                description="Total active AI agents deployed"
            )
        ]

    async def _get_revenue_metrics(self, time_range: TimeRange) -> RevenueMetrics:
        """Get detailed revenue metrics"""
        # Sample data - in production, calculate from database
        mrr = 487500
        return RevenueMetrics(
            mrr=mrr,
            arr=mrr * 12,
            new_mrr=62500,
            expansion_mrr=28700,
            churned_mrr=15200,
            net_new_mrr=62500 + 28700 - 15200,
            net_revenue_retention=1.18,
            gross_revenue_retention=0.96,
            average_revenue_per_account=245,
            customer_acquisition_cost=650,
            ltv_cac_ratio=4.8,
            months_to_recover_cac=3
        )

    async def _get_customer_metrics(self, time_range: TimeRange) -> CustomerMetrics:
        """Get customer health and growth metrics"""
        return CustomerMetrics(
            total_customers=1989,
            new_customers=247,
            churned_customers=63,
            active_customers=1842,
            inactive_customers=147,
            customer_churn_rate=3.2,
            customer_growth_rate=12.5,
            average_customer_age_days=187,
            customers_by_tier={
                "free": 891,
                "pro": 847,
                "enterprise": 251
            },
            customers_at_risk=142
        )

    async def _get_usage_metrics(self, time_range: TimeRange) -> UsageMetrics:
        """Get platform usage analytics"""
        return UsageMetrics(
            total_agents_deployed=8547,
            active_agents=3847,
            total_api_calls=12847653,
            average_api_calls_per_customer=6462,
            total_automations_executed=2847653,
            total_hours_saved=487234.5,
            feature_adoption_rates={
                "marketplace": 0.87,
                "academy": 0.62,
                "analytics": 0.78,
                "integrations": 0.54,
                "custom_agents": 0.41
            },
            most_popular_agents=[
                {"name": "Email Auto-Responder", "deployments": 1247, "category": "communication"},
                {"name": "Lead Qualifier", "deployments": 982, "category": "sales"},
                {"name": "Meeting Scheduler", "deployments": 871, "category": "productivity"},
                {"name": "Customer Support Bot", "deployments": 743, "category": "support"},
                {"name": "Content Generator", "deployments": 687, "category": "marketing"}
            ],
            daily_active_users=1247,
            weekly_active_users=1689,
            monthly_active_users=1842
        )

    async def _get_sales_metrics(self, time_range: TimeRange) -> SalesMetrics:
        """Get sales pipeline and performance"""
        return SalesMetrics(
            total_leads=1847,
            qualified_leads=824,
            hot_leads=187,
            conversion_rate=22.7,
            average_deal_size=2450,
            sales_cycle_days=21,
            win_rate=0.68,
            pipeline_value=1247800,
            weighted_pipeline=848500,
            quota_attainment=112.4
        )

    # ========================================================================
    # INSIGHTS & ALERTS
    # ========================================================================

    async def _get_top_insights(self) -> List[Dict]:
        """Get AI-generated insights from data"""
        return [
            {
                "type": "success",
                "title": "Strong Upsell Performance",
                "description": "Expansion MRR up 34% this month. Pro -> Enterprise conversions at all-time high.",
                "impact": "high",
                "action": "Continue targeted upsell campaigns for Pro users with 5+ agents"
            },
            {
                "type": "warning",
                "title": "Churn Risk Detected",
                "description": "142 customers showing high churn risk signals. 78% are Free tier with low engagement.",
                "impact": "medium",
                "action": "Launch re-engagement campaign for inactive Free users"
            },
            {
                "type": "info",
                "title": "Feature Adoption Opportunity",
                "description": "Only 41% of Pro customers using custom agents. Significant value untapped.",
                "impact": "medium",
                "action": "Create targeted Academy course on custom agent development"
            },
            {
                "type": "success",
                "title": "Sales Efficiency Gains",
                "description": "Sales cycle decreased from 28 to 21 days. Lead scoring AI improving qualification.",
                "impact": "high",
                "action": "Share best practices with entire sales team"
            }
        ]

    async def _get_alerts(self) -> List[Dict]:
        """Get urgent alerts requiring attention"""
        return [
            {
                "severity": "critical",
                "title": "Payment Failures Spike",
                "description": "47 payment failures in last 24 hours (3x normal). Investigate immediately.",
                "timestamp": datetime.now().isoformat(),
                "action_required": True
            },
            {
                "severity": "warning",
                "title": "API Rate Limits Hit",
                "description": "12 enterprise customers hitting rate limits. Consider infrastructure scaling.",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "action_required": True
            }
        ]

    # ========================================================================
    # AGENT MARKETPLACE ANALYTICS
    # ========================================================================

    async def get_marketplace_analytics(self) -> Dict:
        """Get marketplace performance metrics"""
        return {
            "overview": {
                "total_agents": 57,
                "total_downloads": 28947,
                "total_revenue": 487234,
                "average_rating": 4.7,
                "verified_publishers": 23
            },
            "top_agents": [
                {
                    "name": "Email Auto-Responder",
                    "category": "communication",
                    "downloads": 1247,
                    "revenue": 0,  # Free
                    "rating": 4.8,
                    "growth": "12%"
                },
                {
                    "name": "Lead Qualifier",
                    "category": "sales",
                    "downloads": 982,
                    "revenue": 78560,  # $80/agent
                    "rating": 4.9,
                    "growth": "18%"
                },
                {
                    "name": "Healthcare Appointment Booking",
                    "category": "healthcare",
                    "downloads": 342,
                    "revenue": 16758,  # $49/agent
                    "rating": 4.9,
                    "growth": "45%"
                }
            ],
            "categories": {
                "communication": {"agents": 8, "downloads": 3847},
                "sales": {"agents": 9, "downloads": 2941},
                "healthcare": {"agents": 8, "downloads": 1247},
                "education": {"agents": 8, "downloads": 847},
                "legal": {"agents": 8, "downloads": 634},
                "construction": {"agents": 8, "downloads": 521},
                "logistics": {"agents": 8, "downloads": 487}
            },
            "trending": [
                {"name": "AI Legal Research Assistant", "growth": "124%"},
                {"name": "Patient Follow-Up Care", "growth": "89%"},
                {"name": "Route Optimization Agent", "growth": "67%"}
            ]
        }

    # ========================================================================
    # CUSTOM REPORTS
    # ========================================================================

    async def generate_executive_report(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS
    ) -> Dict:
        """Generate executive summary report"""
        dashboard = await self.get_dashboard_overview(time_range)

        return {
            "report_type": "Executive Summary",
            "generated_at": datetime.now().isoformat(),
            "time_range": time_range,
            "summary": {
                "mrr": dashboard["revenue"].mrr,
                "mrr_growth": dashboard["revenue"].net_new_mrr,
                "customer_count": dashboard["customers"].total_customers,
                "customer_growth": dashboard["customers"].new_customers,
                "churn_rate": dashboard["customers"].customer_churn_rate,
                "nrr": dashboard["revenue"].net_revenue_retention,
                "ltv_cac": dashboard["revenue"].ltv_cac_ratio
            },
            "highlights": [
                f"MRR grew {dashboard['revenue'].net_new_mrr:,.0f} to ${dashboard['revenue'].mrr:,.0f}",
                f"Added {dashboard['customers'].new_customers} new customers",
                f"NRR at {dashboard['revenue'].net_revenue_retention:.0%} (expansion > churn)",
                f"LTV:CAC ratio healthy at {dashboard['revenue'].ltv_cac_ratio:.1f}x"
            ],
            "concerns": [
                f"{dashboard['customers'].customers_at_risk} customers at churn risk",
                "Need to improve Free -> Pro conversion rate"
            ],
            "recommendations": dashboard["top_insights"]
        }

    async def generate_sales_report(
        self,
        time_range: TimeRange = TimeRange.LAST_30_DAYS
    ) -> Dict:
        """Generate sales team performance report"""
        sales = await self._get_sales_metrics(time_range)

        return {
            "report_type": "Sales Performance",
            "generated_at": datetime.now().isoformat(),
            "metrics": {
                "pipeline_value": sales.pipeline_value,
                "weighted_pipeline": sales.weighted_pipeline,
                "win_rate": sales.win_rate,
                "average_deal_size": sales.average_deal_size,
                "sales_cycle_days": sales.sales_cycle_days,
                "quota_attainment": sales.quota_attainment
            },
            "lead_funnel": {
                "total_leads": sales.total_leads,
                "qualified": sales.qualified_leads,
                "hot": sales.hot_leads,
                "conversion_rate": sales.conversion_rate
            },
            "recommendations": [
                "Focus on hot leads (187) for quick wins",
                "Improve qualification process to reduce sales cycle",
                "Leverage AI lead scoring to prioritize outreach"
            ]
        }

    # ========================================================================
    # EXPORT FUNCTIONALITY
    # ========================================================================

    async def export_dashboard_data(
        self,
        format: str = "json",
        time_range: TimeRange = TimeRange.LAST_30_DAYS
    ) -> str:
        """
        Export dashboard data

        Formats:
        - json: JSON format
        - csv: CSV format (future)
        - pdf: PDF report (future)
        """
        dashboard = await self.get_dashboard_overview(time_range)

        if format == "json":
            return json.dumps(dashboard, indent=2, default=str)
        else:
            raise ValueError(f"Export format '{format}' not supported yet")

    # ========================================================================
    # REAL-TIME METRICS
    # ========================================================================

    async def get_realtime_metrics(self) -> Dict:
        """Get real-time metrics for live dashboard"""
        return {
            "timestamp": datetime.now().isoformat(),
            "active_users": 247,
            "active_agents": 1847,
            "api_calls_per_minute": 1247,
            "automations_running": 847,
            "system_health": {
                "status": "healthy",
                "uptime": 99.97,
                "response_time_ms": 142,
                "error_rate": 0.02
            },
            "recent_signups": 3,
            "recent_upgrades": 2,
            "revenue_today": 12847
        }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'AdvancedDashboard',
    'KPIMetric',
    'RevenueMetrics',
    'CustomerMetrics',
    'UsageMetrics',
    'SalesMetrics',
    'MetricTrend',
    'TimeRange'
]
