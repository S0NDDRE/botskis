"""
Income Tracker - Centralized Income Tracking System
Tracks earnings across all income bots in real-time

Features:
- Real-time earnings tracking
- Per-bot statistics
- Daily/weekly/monthly reports
- Income forecasting
- Performance analytics
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import asyncio

Base = declarative_base()


class IncomeTransaction(Base):
    """Income transaction model"""
    __tablename__ = "income_transactions"

    id = Column(Integer, primary_key=True)
    bot_type = Column(String)  # freelance, testing, survey, writing
    platform = Column(String)  # upwork, usertesting, swagbucks, etc.
    job_id = Column(String)
    job_title = Column(String)
    amount_nok = Column(Float)
    currency = Column(String, default="NOK")
    status = Column(String)  # pending, completed, paid
    earned_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    metadata = Column(String, nullable=True)  # JSON metadata


class IncomeStats(BaseModel):
    """Income statistics model"""
    total_earnings_nok: float
    earnings_today: float
    earnings_this_week: float
    earnings_this_month: float
    by_bot_type: Dict[str, float]
    by_platform: Dict[str, float]
    total_jobs_completed: int
    average_per_job: float
    best_performing_bot: str
    hourly_rate_estimate: float


class IncomeTracker:
    """
    Centralized Income Tracking System

    Tracks all income across:
    - Freelance Bot
    - Testing Bot
    - Survey Bot
    - Writing Bot
    """

    def __init__(self, database_url: str = "sqlite:///income.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        logger.info("Income Tracker initialized")

    def record_income(
        self,
        bot_type: str,
        platform: str,
        job_id: str,
        job_title: str,
        amount_nok: float,
        status: str = "completed",
        metadata: Optional[str] = None
    ) -> IncomeTransaction:
        """
        Record income from any bot

        Args:
            bot_type: freelance, testing, survey, writing
            platform: upwork, usertesting, swagbucks, etc.
            job_id: Unique job identifier
            job_title: Job title/description
            amount_nok: Amount earned in NOK
            status: completed, paid
            metadata: Additional JSON metadata
        """
        transaction = IncomeTransaction(
            bot_type=bot_type,
            platform=platform,
            job_id=job_id,
            job_title=job_title,
            amount_nok=amount_nok,
            status=status,
            earned_at=datetime.utcnow(),
            paid_at=datetime.utcnow() if status == "paid" else None,
            metadata=metadata
        )

        self.session.add(transaction)
        self.session.commit()

        logger.info(f"✅ Recorded {amount_nok} NOK from {bot_type} ({platform})")
        return transaction

    def get_total_earnings(self) -> float:
        """Get total earnings across all bots"""
        total = self.session.query(
            IncomeTransaction
        ).with_entities(
            IncomeTransaction.amount_nok
        ).all()

        return sum(t[0] for t in total)

    def get_earnings_today(self) -> float:
        """Get today's earnings"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        earnings = self.session.query(
            IncomeTransaction
        ).filter(
            IncomeTransaction.earned_at >= today_start
        ).with_entities(
            IncomeTransaction.amount_nok
        ).all()

        return sum(e[0] for e in earnings)

    def get_earnings_this_week(self) -> float:
        """Get this week's earnings"""
        week_start = datetime.utcnow() - timedelta(days=7)

        earnings = self.session.query(
            IncomeTransaction
        ).filter(
            IncomeTransaction.earned_at >= week_start
        ).with_entities(
            IncomeTransaction.amount_nok
        ).all()

        return sum(e[0] for e in earnings)

    def get_earnings_this_month(self) -> float:
        """Get this month's earnings"""
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        earnings = self.session.query(
            IncomeTransaction
        ).filter(
            IncomeTransaction.earned_at >= month_start
        ).with_entities(
            IncomeTransaction.amount_nok
        ).all()

        return sum(e[0] for e in earnings)

    def get_earnings_by_bot_type(self) -> Dict[str, float]:
        """Get earnings breakdown by bot type"""
        transactions = self.session.query(IncomeTransaction).all()

        by_bot = {}
        for t in transactions:
            if t.bot_type not in by_bot:
                by_bot[t.bot_type] = 0
            by_bot[t.bot_type] += t.amount_nok

        return by_bot

    def get_earnings_by_platform(self) -> Dict[str, float]:
        """Get earnings breakdown by platform"""
        transactions = self.session.query(IncomeTransaction).all()

        by_platform = {}
        for t in transactions:
            if t.platform not in by_platform:
                by_platform[t.platform] = 0
            by_platform[t.platform] += t.amount_nok

        return by_platform

    def get_stats(self) -> IncomeStats:
        """
        Get comprehensive income statistics
        """
        total_earnings = self.get_total_earnings()
        earnings_today = self.get_earnings_today()
        earnings_week = self.get_earnings_this_week()
        earnings_month = self.get_earnings_this_month()

        by_bot = self.get_earnings_by_bot_type()
        by_platform = self.get_earnings_by_platform()

        total_jobs = self.session.query(IncomeTransaction).count()
        average_per_job = total_earnings / total_jobs if total_jobs > 0 else 0

        # Find best performing bot
        best_bot = max(by_bot.items(), key=lambda x: x[1])[0] if by_bot else "none"

        # Estimate hourly rate (assume 8 hours/day work)
        days_active = (datetime.utcnow() - self.get_first_transaction_date()).days or 1
        total_hours = days_active * 8
        hourly_rate = total_earnings / total_hours if total_hours > 0 else 0

        return IncomeStats(
            total_earnings_nok=total_earnings,
            earnings_today=earnings_today,
            earnings_this_week=earnings_week,
            earnings_this_month=earnings_month,
            by_bot_type=by_bot,
            by_platform=by_platform,
            total_jobs_completed=total_jobs,
            average_per_job=average_per_job,
            best_performing_bot=best_bot,
            hourly_rate_estimate=hourly_rate
        )

    def get_first_transaction_date(self) -> datetime:
        """Get date of first transaction"""
        first = self.session.query(
            IncomeTransaction
        ).order_by(
            IncomeTransaction.earned_at.asc()
        ).first()

        return first.earned_at if first else datetime.utcnow()

    def get_recent_transactions(self, limit: int = 10) -> List[IncomeTransaction]:
        """Get recent transactions"""
        return self.session.query(
            IncomeTransaction
        ).order_by(
            IncomeTransaction.earned_at.desc()
        ).limit(limit).all()

    def get_daily_earnings_chart(self, days: int = 30) -> Dict[str, float]:
        """
        Get daily earnings for chart

        Returns dict: {"2024-01-15": 250.0, "2024-01-16": 180.0, ...}
        """
        start_date = datetime.utcnow() - timedelta(days=days)

        transactions = self.session.query(
            IncomeTransaction
        ).filter(
            IncomeTransaction.earned_at >= start_date
        ).all()

        daily_earnings = {}
        for t in transactions:
            date_key = t.earned_at.strftime("%Y-%m-%d")
            if date_key not in daily_earnings:
                daily_earnings[date_key] = 0
            daily_earnings[date_key] += t.amount_nok

        return daily_earnings

    def forecast_monthly_income(self) -> float:
        """
        Forecast monthly income based on current performance
        """
        earnings_this_month = self.get_earnings_this_month()
        day_of_month = datetime.utcnow().day
        days_in_month = 30  # Simplified

        if day_of_month == 0:
            return 0

        # Calculate daily average
        daily_average = earnings_this_month / day_of_month

        # Forecast for full month
        forecasted = daily_average * days_in_month

        return forecasted

    def export_to_json(self) -> List[Dict]:
        """Export all transactions to JSON"""
        transactions = self.session.query(IncomeTransaction).all()

        return [
            {
                "id": t.id,
                "bot_type": t.bot_type,
                "platform": t.platform,
                "job_id": t.job_id,
                "job_title": t.job_title,
                "amount_nok": t.amount_nok,
                "status": t.status,
                "earned_at": t.earned_at.isoformat(),
                "paid_at": t.paid_at.isoformat() if t.paid_at else None
            }
            for t in transactions
        ]

    def close(self):
        """Close database connection"""
        self.session.close()


# Example usage
def example_income_tracker():
    """Example of using the income tracker"""
    tracker = IncomeTracker()

    # Record some income
    tracker.record_income(
        bot_type="freelance",
        platform="upwork",
        job_id="upwork_job_001",
        job_title="Write 10 blog articles",
        amount_nok=800.0,
        status="paid"
    )

    tracker.record_income(
        bot_type="testing",
        platform="usertesting",
        job_id="test_001",
        job_title="E-commerce usability test",
        amount_nok=25.0,
        status="completed"
    )

    tracker.record_income(
        bot_type="survey",
        platform="swagbucks",
        job_id="survey_001",
        job_title="Consumer shopping habits",
        amount_nok=8.0,
        status="paid"
    )

    # Get stats
    stats = tracker.get_stats()
    print(f"📊 Total Earnings: {stats.total_earnings_nok} NOK")
    print(f"💰 Today: {stats.earnings_today} NOK")
    print(f"📈 Best Bot: {stats.best_performing_bot}")
    print(f"⏰ Hourly Rate: {stats.hourly_rate_estimate:.2f} NOK/hour")

    # Get recent transactions
    recent = tracker.get_recent_transactions(5)
    print(f"\n📋 Recent Transactions:")
    for t in recent:
        print(f"  - {t.job_title}: {t.amount_nok} NOK ({t.bot_type})")

    # Forecast
    forecast = tracker.forecast_monthly_income()
    print(f"\n🔮 Forecasted Monthly Income: {forecast:.2f} NOK")

    tracker.close()


if __name__ == "__main__":
    example_income_tracker()
