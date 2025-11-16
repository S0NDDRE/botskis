"""
Mindframe Marketplace - Pre-built AI Agents Library
Ready-to-use agents that customers can install with one click
"""
from typing import Dict, List
from src.marketplace.industry_agents import INDUSTRY_AGENTS
from src.marketplace.income_agents import INCOME_AGENTS

# ============================================================================
# MARKETPLACE AGENTS LIBRARY
# ============================================================================

MARKETPLACE_AGENTS = {}

# ============================================================================
# FREE AGENTS (Customer Acquisition)
# ============================================================================

MARKETPLACE_AGENTS["email_auto_responder"] = {
    "id": "email_auto_responder",
    "name": "Email Auto-Responder",
    "description": "Automatically respond to customer emails with helpful, context-aware responses",
    "category": "customer_support",
    "price": "free",
    "rating": 4.8,
    "downloads": 12547,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Analyzes incoming email content",
        "Generates professional responses",
        "Customizable tone and style",
        "Auto-categorizes emails",
        "Escalates complex issues to humans"
    ],
    "use_cases": [
        "Customer support automation",
        "Sales inquiry responses",
        "FAQ handling",
        "Order confirmations"
    ],
    "config": {
        "email_provider": "gmail",  # or "outlook", "smtp"
        "tone": "professional",  # or "friendly", "casual"
        "response_time": "instant",
        "escalation_keywords": ["urgent", "complaint", "refund"]
    }
}

MARKETPLACE_AGENTS["meeting_scheduler"] = {
    "id": "meeting_scheduler",
    "name": "AI Meeting Scheduler",
    "description": "Schedule meetings automatically via email or chat",
    "category": "productivity",
    "price": "free",
    "rating": 4.7,
    "downloads": 9834,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Reads availability from calendar",
        "Suggests meeting times",
        "Sends calendar invites",
        "Handles rescheduling",
        "Time zone aware"
    ],
    "integrations": ["Google Calendar", "Outlook", "Zoom"]
}

MARKETPLACE_AGENTS["social_media_responder"] = {
    "id": "social_media_responder",
    "name": "Social Media Comment Responder",
    "description": "Automatically engage with comments on social media",
    "category": "marketing",
    "price": "free",
    "rating": 4.6,
    "downloads": 7623,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Monitors Facebook, Instagram, LinkedIn",
        "Responds to comments",
        "Filters spam",
        "Escalates negative comments",
        "Brand voice consistency"
    ]
}

# ============================================================================
# PREMIUM AGENTS ($19-49)
# ============================================================================

MARKETPLACE_AGENTS["lead_qualifier"] = {
    "id": "lead_qualifier",
    "name": "AI Lead Qualifier",
    "description": "Automatically qualify and score inbound leads",
    "category": "sales",
    "price": 19,
    "rating": 4.9,
    "downloads": 5432,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Analyzes lead information",
        "Scores leads 0-100",
        "Categorizes by ICP fit",
        "Updates CRM automatically",
        "Sends notifications for hot leads"
    ],
    "integrations": ["HubSpot", "Salesforce", "Pipedrive"],
    "roi_example": {
        "time_saved": "15 hours/week",
        "cost_savings": "$3,000/month",
        "conversion_increase": "23%"
    }
}

MARKETPLACE_AGENTS["content_generator"] = {
    "id": "content_generator",
    "name": "Content Creation Agent",
    "description": "Generate blog posts, social media content, and marketing copy",
    "category": "marketing",
    "price": 29,
    "rating": 4.8,
    "downloads": 4521,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Blog post generation",
        "Social media posts",
        "Email campaigns",
        "SEO optimization",
        "Multi-language support"
    ]
}

MARKETPLACE_AGENTS["invoice_processor"] = {
    "id": "invoice_processor",
    "name": "AI Invoice Processor",
    "description": "Automatically process invoices and update accounting",
    "category": "finance",
    "price": 39,
    "rating": 4.9,
    "downloads": 3876,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Extracts invoice data",
        "Validates against PO",
        "Updates accounting software",
        "Flags discrepancies",
        "Generates reports"
    ],
    "integrations": ["QuickBooks", "Xero", "Sage"]
}

# ============================================================================
# ENTERPRISE AGENTS ($99-299)
# ============================================================================

MARKETPLACE_AGENTS["crm_auto_updater"] = {
    "id": "crm_auto_updater",
    "name": "CRM Auto-Updater Pro",
    "description": "Keep your CRM always up-to-date automatically",
    "category": "sales",
    "price": 99,
    "rating": 5.0,
    "downloads": 1243,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Updates contact information",
        "Logs all interactions",
        "Enriches data from LinkedIn",
        "Creates tasks and reminders",
        "AI-powered lead scoring"
    ],
    "integrations": ["Salesforce", "HubSpot", "Pipedrive", "Zoho"]
}

MARKETPLACE_AGENTS["customer_churn_predictor"] = {
    "id": "customer_churn_predictor",
    "name": "Churn Prediction Agent",
    "description": "Predict and prevent customer churn before it happens",
    "category": "customer_success",
    "price": 149,
    "rating": 4.9,
    "downloads": 892,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Analyzes usage patterns",
        "Predicts churn risk",
        "Triggers retention campaigns",
        "Personalized interventions",
        "ROI tracking"
    ],
    "roi_example": {
        "churn_reduction": "35%",
        "revenue_saved": "$50,000/month",
        "roi": "3,350%"
    }
}

MARKETPLACE_AGENTS["voice_sales_agent"] = {
    "id": "voice_sales_agent",
    "name": "AI Sales Call Agent",
    "description": "Make outbound sales calls and qualify prospects",
    "category": "sales",
    "price": 299,
    "rating": 4.8,
    "downloads": 654,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Natural conversation",
        "Handles objections",
        "Qualifies prospects",
        "Books meetings",
        "CRM integration",
        "Call recording & transcription"
    ],
    "integrations": ["Salesforce", "HubSpot", "Twilio"]
}

# ============================================================================
# INDUSTRY-SPECIFIC AGENTS
# ============================================================================

MARKETPLACE_AGENTS["restaurant_reservation"] = {
    "id": "restaurant_reservation",
    "name": "Restaurant Reservation Agent",
    "description": "Handle restaurant bookings via phone and web",
    "category": "hospitality",
    "price": 79,
    "rating": 4.7,
    "downloads": 543,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Takes reservations 24/7",
        "Manages waiting list",
        "Sends confirmations",
        "Handles cancellations",
        "Multi-language support"
    ]
}

MARKETPLACE_AGENTS["ecommerce_support"] = {
    "id": "ecommerce_support",
    "name": "E-commerce Support Agent",
    "description": "Complete customer support for online stores",
    "category": "ecommerce",
    "price": 59,
    "rating": 4.8,
    "downloads": 2341,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Order tracking",
        "Return/refund processing",
        "Product recommendations",
        "FAQ automation",
        "Live chat integration"
    ],
    "integrations": ["Shopify", "WooCommerce", "Magento"]
}

MARKETPLACE_AGENTS["real_estate_qualifier"] = {
    "id": "real_estate_qualifier",
    "name": "Real Estate Lead Qualifier",
    "description": "Qualify and nurture real estate leads",
    "category": "real_estate",
    "price": 129,
    "rating": 4.9,
    "downloads": 432,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Qualifies buyer/seller leads",
        "Schedules property viewings",
        "Sends property listings",
        "Nurtures leads over time",
        "CRM integration"
    ]
}

# ============================================================================
# INTEGRATION AGENTS
# ============================================================================

MARKETPLACE_AGENTS["slack_assistant"] = {
    "id": "slack_assistant",
    "name": "Slack Team Assistant",
    "description": "AI assistant for Slack that helps your team",
    "category": "productivity",
    "price": 49,
    "rating": 4.7,
    "downloads": 3245,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Answers team questions",
        "Summarizes channels",
        "Creates tasks from messages",
        "Finds information",
        "Reminds about deadlines"
    ]
}

MARKETPLACE_AGENTS["google_sheets_automator"] = {
    "id": "google_sheets_automator",
    "name": "Google Sheets Automation Agent",
    "description": "Automate data entry and analysis in Google Sheets",
    "category": "productivity",
    "price": 39,
    "rating": 4.6,
    "downloads": 2876,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Auto-populates sheets",
        "Data validation",
        "Report generation",
        "Chart creation",
        "Email notifications"
    ]
}

MARKETPLACE_AGENTS["trello_task_manager"] = {
    "id": "trello_task_manager",
    "name": "Trello AI Task Manager",
    "description": "Intelligent task management for Trello boards",
    "category": "productivity",
    "price": 29,
    "rating": 4.5,
    "downloads": 1987,
    "author": "Mindframe",
    "verified": True,
    "features": [
        "Auto-creates tasks from emails",
        "Prioritizes tasks",
        "Assigns to team members",
        "Tracks progress",
        "Sends updates"
    ]
}

# ============================================================================
# COMMUNITY AGENTS (User-created)
# ============================================================================

MARKETPLACE_AGENTS["linkedin_connection_manager"] = {
    "id": "linkedin_connection_manager",
    "name": "LinkedIn Connection Manager",
    "description": "Manage LinkedIn connections and outreach",
    "category": "sales",
    "price": 69,
    "rating": 4.4,
    "downloads": 876,
    "author": "SalesGuru",
    "verified": False,
    "community_created": True,
    "features": [
        "Personalized connection requests",
        "Follow-up messages",
        "Engagement tracking",
        "Lead export to CRM"
    ]
}

MARKETPLACE_AGENTS["hr_candidate_screener"] = {
    "id": "hr_candidate_screener",
    "name": "HR Candidate Screening Agent",
    "description": "Screen job applicants automatically",
    "category": "hr",
    "price": 99,
    "rating": 4.6,
    "downloads": 543,
    "author": "HRTech Solutions",
    "verified": False,
    "community_created": True,
    "features": [
        "Reviews resumes",
        "Conducts initial screening",
        "Schedules interviews",
        "Sends rejection emails",
        "ATS integration"
    ]
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_agent_by_id(agent_id: str) -> Dict:
    """Get agent by ID"""
    return MARKETPLACE_AGENTS.get(agent_id)


def get_agents_by_category(category: str) -> List[Dict]:
    """Get all agents in a category"""
    return [
        agent for agent in MARKETPLACE_AGENTS.values()
        if agent.get("category") == category
    ]


def get_free_agents() -> List[Dict]:
    """Get all free agents"""
    return [
        agent for agent in MARKETPLACE_AGENTS.values()
        if agent.get("price") == "free"
    ]


def get_premium_agents() -> List[Dict]:
    """Get all premium agents"""
    return [
        agent for agent in MARKETPLACE_AGENTS.values()
        if isinstance(agent.get("price"), int) and agent.get("price") > 0
    ]


def search_agents(query: str) -> List[Dict]:
    """Search agents by name or description"""
    query_lower = query.lower()
    return [
        agent for agent in MARKETPLACE_AGENTS.values()
        if query_lower in agent.get("name", "").lower() or
           query_lower in agent.get("description", "").lower()
    ]


def get_top_rated_agents(limit: int = 10) -> List[Dict]:
    """Get top rated agents"""
    sorted_agents = sorted(
        MARKETPLACE_AGENTS.values(),
        key=lambda x: x.get("rating", 0),
        reverse=True
    )
    return sorted_agents[:limit]


def get_most_downloaded_agents(limit: int = 10) -> List[Dict]:
    """Get most downloaded agents"""
    sorted_agents = sorted(
        MARKETPLACE_AGENTS.values(),
        key=lambda x: x.get("downloads", 0),
        reverse=True
    )
    return sorted_agents[:limit]


# ============================================================================
# MERGE INDUSTRY-SPECIFIC AGENTS
# ============================================================================
# Add all 40 industry-specific agents to marketplace
MARKETPLACE_AGENTS.update(INDUSTRY_AGENTS)

# ============================================================================
# MERGE INCOME GENERATION AGENTS
# ============================================================================
# Add all 5 income generation agents to marketplace
MARKETPLACE_AGENTS.update(INCOME_AGENTS)


# Statistics
def get_marketplace_stats() -> Dict:
    """Get marketplace statistics"""
    return {
        "total_agents": len(MARKETPLACE_AGENTS),
        "free_agents": len(get_free_agents()),
        "premium_agents": len(get_premium_agents()),
        "total_downloads": sum(agent.get("downloads", 0) for agent in MARKETPLACE_AGENTS.values()),
        "average_rating": sum(agent.get("rating", 0) for agent in MARKETPLACE_AGENTS.values()) / len(MARKETPLACE_AGENTS) if len(MARKETPLACE_AGENTS) > 0 else 0,
        "categories": list(set(agent.get("category") for agent in MARKETPLACE_AGENTS.values())),
        "industries": list(set(agent.get("industry") for agent in MARKETPLACE_AGENTS.values() if agent.get("industry")))
    }
