#!/bin/bash
#
# start_income_bots.sh - Start All Income Generation Bots
# One-command setup for autonomous income generation
#
# Usage: ./start_income_bots.sh
#

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💰 MINDFRAME INCOME GENERATION SYSTEM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🤖 Starting Autonomous Income Bots..."
echo ""

# Check if running in project directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.11+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
fi

echo "✅ Environment ready"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file - Please add your OpenAI API key!"
        echo ""
    else
        echo "❌ No .env.example found"
        exit 1
    fi
fi

# Check OpenAI API key
if ! grep -q "OPENAI_API_KEY=sk-" .env; then
    echo "⚠️  OpenAI API key not configured in .env"
    echo "   Please add: OPENAI_API_KEY=sk-your-key-here"
    echo ""
    read -p "Do you want to enter it now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter OpenAI API key: " api_key
        sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$api_key/" .env
        echo "✅ API key saved"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 LAUNCHING INCOME BOTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create income bot runner script
cat > run_income_bots.py << 'EOF'
"""
Income Bots Runner
Starts all 4 income bots in parallel
"""
import asyncio
import os
from dotenv import load_dotenv
from loguru import logger

# Import all income bots
from src.income.freelance_bot import FreelanceBot, FreelanceBotConfig
from src.income.testing_bot import WebsiteTestingBot, TestingBotConfig
from src.income.survey_bot import SurveyBot, SurveyBotConfig
from src.income.writing_bot import WritingBot, WritingBotConfig
from src.income.income_tracker import IncomeTracker

# Load environment
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    logger.error("OPENAI_API_KEY not found in .env")
    exit(1)

# Initialize income tracker
tracker = IncomeTracker()

async def run_freelance_bot():
    """Run freelance bot"""
    logger.info("🚀 Starting Freelance Bot...")
    bot = FreelanceBot(
        openai_api_key=openai_key,
        config=FreelanceBotConfig(
            platforms=["upwork", "freelancer", "finn"],
            skills=["writing", "data_entry", "web_research"],
            min_budget_nok=500,
            max_budget_nok=1500,
            auto_apply=True,
            max_applications_per_day=10
        )
    )
    await bot.auto_run(duration_hours=24)
    stats = bot.get_stats()
    logger.success(f"💼 Freelance Bot: {stats['jobs_completed']} jobs, {stats['total_earnings_nok']} NOK")

async def run_testing_bot():
    """Run testing bot"""
    logger.info("🚀 Starting Testing Bot...")
    bot = WebsiteTestingBot(
        openai_api_key=openai_key,
        config=TestingBotConfig(
            platforms=["usertesting", "testbirds"],
            min_payout_nok=20,
            max_tests_per_day=15,
            auto_claim_tests=True
        )
    )
    await bot.auto_run(duration_hours=24)
    stats = bot.get_stats()
    logger.success(f"🧪 Testing Bot: {stats['tests_completed']} tests, {stats['total_earnings_nok']} NOK")

async def run_survey_bot():
    """Run survey bot"""
    logger.info("🚀 Starting Survey Bot...")
    bot = SurveyBot(
        openai_api_key=openai_key,
        config=SurveyBotConfig(
            platforms=["swagbucks", "ysense", "toluna"],
            min_payout_nok=5,
            max_surveys_per_day=30,
            auto_complete=True
        )
    )
    await bot.auto_run(duration_hours=24)
    stats = bot.get_stats()
    logger.success(f"📋 Survey Bot: {stats['surveys_completed']} surveys, {stats['total_earnings_nok']} NOK")

async def run_writing_bot():
    """Run writing bot"""
    logger.info("🚀 Starting Writing Bot...")
    bot = WritingBot(
        openai_api_key=openai_key,
        config=WritingBotConfig(
            platforms=["textbroker", "iwriter"],
            min_payout_nok=30,
            max_word_count=1000,
            max_jobs_per_day=10,
            auto_claim=True
        )
    )
    await bot.auto_run(duration_hours=24)
    stats = bot.get_stats()
    logger.success(f"✍️  Writing Bot: {stats['jobs_completed']} jobs, {stats['total_earnings_nok']} NOK")

async def main():
    """Run all bots in parallel"""
    logger.info("💰 Starting All Income Bots...")
    logger.info("=" * 60)

    # Run all bots concurrently
    await asyncio.gather(
        run_freelance_bot(),
        run_testing_bot(),
        run_survey_bot(),
        run_writing_bot()
    )

    # Get final stats
    logger.info("=" * 60)
    logger.info("📊 Final Income Report:")

    stats = tracker.get_stats()
    logger.info(f"   Total Earnings: {stats.total_earnings_nok:.2f} NOK")
    logger.info(f"   Jobs Completed: {stats.total_jobs_completed}")
    logger.info(f"   Average per Job: {stats.average_per_job:.2f} NOK")
    logger.info(f"   Hourly Rate: {stats.hourly_rate_estimate:.2f} NOK/hr")
    logger.info(f"   Best Bot: {stats.best_performing_bot}")

    logger.success("✅ All Income Bots Completed!")

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo "💼 Freelance Bot (Upwork, Freelancer, FINN.no)"
echo "   └─ Income Potential: 500-1,200 kr/job"
echo ""

echo "🧪 Testing Bot (UserTesting, TestBirds)"
echo "   └─ Income Potential: 20-30 kr/test"
echo ""

echo "📋 Survey Bot (Swagbucks, ySense)"
echo "   └─ Income Potential: 5-15 kr/survey"
echo ""

echo "✍️  Writing Bot (Textbroker, iWriter)"
echo "   └─ Income Potential: 30-80 kr/article"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ask user for duration
read -p "How many hours should the bots run? (default: 24): " hours
hours=${hours:-24}

echo ""
echo "🤖 Starting all 4 income bots for $hours hours..."
echo ""

# Run the bots
python3 run_income_bots.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ INCOME BOTS COMPLETED"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 View detailed income stats in the dashboard:"
echo "   http://localhost:5173/income"
echo ""
echo "💡 Tip: Run this script daily for continuous income generation!"
echo ""
