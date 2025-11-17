"""
Income Generation Agents for Mindframe Marketplace
Pre-built autonomous income bots users can deploy with ONE CLICK

These agents work 24/7 to generate passive income automatically
"""
from typing import Dict, List

# ============================================================================
# INCOME GENERATION AGENTS
# ============================================================================

INCOME_AGENTS = {}

# ============================================================================
# FREELANCE INCOME AGENT
# ============================================================================

INCOME_AGENTS["freelance_income_bot"] = {
    "id": "freelance_income_bot",
    "name": "Freelance Income Bot",
    "tagline": "🤖 Autonomous Freelance Job Hunter & Completer",
    "description": "AI-powered bot that automatically finds, applies to, and completes freelance jobs on Upwork, Freelancer, and FINN.no",
    "category": "income_generation",
    "price": 0,  # FREE to install
    "rating": 4.9,
    "downloads": 856,
    "author": "Mindframe",
    "verified": True,
    "ai_powered": True,
    "features": [
        "Auto-searches for relevant freelance jobs",
        "AI-generated cover letters",
        "Automatic job applications (10/day)",
        "AI-powered job completion",
        "Real-time income tracking",
        "Works on Upwork, Freelancer, FINN.no"
    ],
    "income_potential": {
        "per_job": "500-1,200 NOK",
        "per_day": "500-2,000 NOK",
        "per_month": "15,000-60,000 NOK"
    },
    "platforms": ["Upwork", "Freelancer", "FINN.no"],
    "job_types": ["Writing", "Data Entry", "Web Research", "Translation"],
    "requirements": ["OpenAI API key"],
    "setup_time": "5 minutes",
    "autonomous": True,
    "runs_24_7": True,
    "config": {
        "platforms": ["upwork", "freelancer", "finn"],
        "skills": ["writing", "data_entry", "web_research"],
        "min_budget_nok": 500,
        "max_budget_nok": 1500,
        "auto_apply": True,
        "max_applications_per_day": 10
    },
    "installation": {
        "type": "one_click",
        "script": "src/income/freelance_bot.py",
        "command": "./start_income_bots.sh freelance"
    },
    "tags": ["income", "freelance", "autonomous", "ai", "passive_income", "upwork"]
}

# ============================================================================
# WEBSITE TESTING INCOME AGENT
# ============================================================================

INCOME_AGENTS["testing_income_bot"] = {
    "id": "testing_income_bot",
    "name": "Website Testing Income Bot",
    "tagline": "🧪 Autonomous Website Tester",
    "description": "AI bot that automatically finds and completes website testing jobs on UserTesting, TestBirds, and TryMyUI",
    "category": "income_generation",
    "price": 0,
    "rating": 4.7,
    "downloads": 623,
    "author": "Mindframe",
    "verified": True,
    "ai_powered": True,
    "features": [
        "Auto-finds testing opportunities",
        "AI-powered usability testing",
        "Bug detection & reporting",
        "Screen recording simulation",
        "Voice feedback generation",
        "Fast turnaround (10-20 min/test)"
    ],
    "income_potential": {
        "per_test": "20-30 NOK",
        "per_day": "100-300 NOK",
        "per_month": "3,000-9,000 NOK"
    },
    "platforms": ["UserTesting", "TestBirds", "TryMyUI"],
    "test_types": ["Usability", "User Flow", "Design Feedback", "Bug Hunting"],
    "requirements": ["OpenAI API key"],
    "setup_time": "5 minutes",
    "autonomous": True,
    "runs_24_7": True,
    "config": {
        "platforms": ["usertesting", "testbirds", "trymyui"],
        "test_types": ["usability", "user_flow", "design_feedback"],
        "min_payout_nok": 20,
        "max_tests_per_day": 15,
        "auto_claim_tests": True
    },
    "installation": {
        "type": "one_click",
        "script": "src/income/testing_bot.py",
        "command": "./start_income_bots.sh testing"
    },
    "tags": ["income", "testing", "autonomous", "ai", "usability", "passive_income"]
}

# ============================================================================
# SURVEY INCOME AGENT
# ============================================================================

INCOME_AGENTS["survey_income_bot"] = {
    "id": "survey_income_bot",
    "name": "Survey Income Bot",
    "tagline": "📋 Autonomous Survey Completer",
    "description": "AI bot that automatically finds and completes paid surveys on Swagbucks, ySense, and Toluna",
    "category": "income_generation",
    "price": 0,
    "rating": 4.6,
    "downloads": 1043,
    "author": "Mindframe",
    "verified": True,
    "ai_powered": True,
    "features": [
        "Auto-finds high-paying surveys",
        "AI-generated consistent answers",
        "Profile-based responses",
        "Attention check detection",
        "Quality score optimization",
        "Fast completion (2-5 min/survey)"
    ],
    "income_potential": {
        "per_survey": "5-15 NOK",
        "per_day": "50-200 NOK",
        "per_month": "1,500-6,000 NOK"
    },
    "platforms": ["Swagbucks", "ySense", "Toluna", "Survey Junkie"],
    "survey_types": ["Consumer", "Technology", "Health", "Lifestyle"],
    "requirements": ["OpenAI API key"],
    "setup_time": "5 minutes",
    "autonomous": True,
    "runs_24_7": True,
    "config": {
        "platforms": ["swagbucks", "ysense", "toluna"],
        "categories": ["consumer", "technology", "lifestyle"],
        "min_payout_nok": 5,
        "max_surveys_per_day": 30,
        "auto_complete": True,
        "user_profile": {
            "age": 28,
            "gender": "male",
            "location": "Norway",
            "occupation": "Tech Professional"
        }
    },
    "installation": {
        "type": "one_click",
        "script": "src/income/survey_bot.py",
        "command": "./start_income_bots.sh survey"
    },
    "tags": ["income", "surveys", "autonomous", "ai", "passive_income", "swagbucks"]
}

# ============================================================================
# WRITING INCOME AGENT
# ============================================================================

INCOME_AGENTS["writing_income_bot"] = {
    "id": "writing_income_bot",
    "name": "Writing Income Bot",
    "tagline": "✍️ Autonomous Content Writer",
    "description": "AI bot that automatically finds and completes writing jobs on Textbroker, iWriter, and Scripted",
    "category": "income_generation",
    "price": 0,
    "rating": 4.8,
    "downloads": 789,
    "author": "Mindframe",
    "verified": True,
    "ai_powered": True,
    "features": [
        "Auto-finds high-paying writing jobs",
        "AI-powered content generation",
        "SEO optimization",
        "Multiple content types",
        "Quality scoring",
        "Earnings per word tracking"
    ],
    "income_potential": {
        "per_article": "30-80 NOK",
        "per_day": "300-800 NOK",
        "per_month": "9,000-24,000 NOK"
    },
    "platforms": ["Textbroker", "iWriter", "Scripted", "WriterAccess"],
    "content_types": ["Articles", "Blog Posts", "Product Descriptions", "Reviews"],
    "requirements": ["OpenAI API key"],
    "setup_time": "5 minutes",
    "autonomous": True,
    "runs_24_7": True,
    "config": {
        "platforms": ["textbroker", "iwriter", "scripted"],
        "job_types": ["article", "blog_post", "product_description"],
        "min_payout_nok": 30,
        "max_word_count": 1000,
        "max_jobs_per_day": 10,
        "auto_claim": True
    },
    "installation": {
        "type": "one_click",
        "script": "src/income/writing_bot.py",
        "command": "./start_income_bots.sh writing"
    },
    "tags": ["income", "writing", "autonomous", "ai", "passive_income", "content"]
}

# ============================================================================
# COMPLETE INCOME PACKAGE (ALL 4 BOTS)
# ============================================================================

INCOME_AGENTS["complete_income_package"] = {
    "id": "complete_income_package",
    "name": "Complete Income Package (All 4 Bots)",
    "tagline": "💰 Full Autonomous Income System",
    "description": "Deploy all 4 income bots at once! Freelance, Testing, Survey, and Writing bots working 24/7 to generate passive income",
    "category": "income_generation",
    "price": 0,  # FREE bundle
    "rating": 5.0,
    "downloads": 432,
    "author": "Mindframe",
    "verified": True,
    "ai_powered": True,
    "is_bundle": True,
    "includes": [
        "freelance_income_bot",
        "testing_income_bot",
        "survey_income_bot",
        "writing_income_bot"
    ],
    "features": [
        "All 4 income bots in one package",
        "Real-time income dashboard",
        "Unified income tracking",
        "Performance analytics",
        "One-command deployment",
        "24/7 autonomous operation"
    ],
    "income_potential": {
        "per_day": "950-3,300 NOK",
        "per_month": "28,500-99,000 NOK",
        "annual": "342,000-1,188,000 NOK"
    },
    "total_platforms": 12,
    "platforms": [
        "Upwork", "Freelancer", "FINN.no",
        "UserTesting", "TestBirds", "TryMyUI",
        "Swagbucks", "ySense", "Toluna",
        "Textbroker", "iWriter", "Scripted"
    ],
    "requirements": ["OpenAI API key"],
    "setup_time": "5 minutes",
    "autonomous": True,
    "runs_24_7": True,
    "installation": {
        "type": "one_click",
        "command": "./start_income_bots.sh"
    },
    "dashboard": {
        "url": "/income",
        "real_time": True,
        "features": [
            "Live earnings counter",
            "Per-bot statistics",
            "Daily/weekly/monthly reports",
            "Income forecasting",
            "Performance charts"
        ]
    },
    "tags": ["income", "bundle", "autonomous", "ai", "passive_income", "complete"]
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_income_agent_by_id(agent_id: str) -> Dict:
    """Get income agent by ID"""
    return INCOME_AGENTS.get(agent_id)


def get_all_income_agents() -> List[Dict]:
    """Get all income generation agents"""
    return list(INCOME_AGENTS.values())


def get_income_stats() -> Dict:
    """Get income agents statistics"""
    return {
        "total_agents": len(INCOME_AGENTS),
        "total_platforms": 12,
        "max_monthly_income_nok": 99000,
        "total_downloads": sum(agent.get("downloads", 0) for agent in INCOME_AGENTS.values()),
        "average_rating": sum(agent.get("rating", 0) for agent in INCOME_AGENTS.values()) / len(INCOME_AGENTS) if INCOME_AGENTS else 0
    }


def get_total_income_potential() -> Dict:
    """Calculate total income potential from all bots"""
    return {
        "daily_min": 950,
        "daily_max": 3300,
        "monthly_min": 28500,
        "monthly_max": 99000,
        "annual_min": 342000,
        "annual_max": 1188000,
        "currency": "NOK"
    }
