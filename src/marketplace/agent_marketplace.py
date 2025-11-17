"""
Agent Marketplace - One-Click Template Deployment
20+ pre-built agent templates ready to deploy in 30 seconds
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel
from loguru import logger


class AgentTemplate(BaseModel):
    """Agent template model"""
    id: int
    name: str
    description: str
    category: str
    icon: str
    deployment_count: int
    rating: float
    estimated_setup_time: str
    time_savings: str
    roi_estimate: str
    features: List[str]
    integrations: List[str]
    config_schema: Dict[str, Any]
    is_featured: bool = False
    is_popular: bool = False


class AgentMarketplace:
    """
    Agent Marketplace

    Features:
    - 20+ pre-built templates
    - One-click deployment (30 seconds)
    - Categories: Email, Sales, Support, Marketing, Productivity
    - Popular templates tracking
    - Instant setup with smart defaults
    """

    def __init__(self):
        self.templates = self._load_templates()

    def _load_templates(self) -> List[AgentTemplate]:
        """Load all available agent templates"""
        return [
            # EMAIL CATEGORY
            AgentTemplate(
                id=1,
                name="Gmail-Trello Automation",
                description="Auto-create Trello cards from Gmail emails with specific labels",
                category="email",
                icon="📧",
                deployment_count=3200,
                rating=4.8,
                estimated_setup_time="30 seconds",
                time_savings="10 hours/week",
                roi_estimate="400% productivity gain",
                features=[
                    "Auto-detect actionable emails",
                    "Smart task extraction",
                    "Priority assignment",
                    "Duplicate detection"
                ],
                integrations=["Gmail", "Trello"],
                config_schema={
                    "gmail_label": "actionable",
                    "trello_board": "To Do",
                    "priority_keywords": ["urgent", "asap", "important"]
                },
                is_featured=True,
                is_popular=True
            ),
            AgentTemplate(
                id=2,
                name="Email Response Assistant",
                description="AI-powered email drafts for common inquiries",
                category="email",
                icon="✉️",
                deployment_count=2800,
                rating=4.7,
                estimated_setup_time="45 seconds",
                time_savings="8 hours/week",
                roi_estimate="320% productivity gain",
                features=[
                    "Smart reply suggestions",
                    "Tone matching",
                    "Template library",
                    "Multi-language support"
                ],
                integrations=["Gmail", "Outlook"],
                config_schema={
                    "response_tone": "professional",
                    "auto_send": False,
                    "languages": ["en", "no"]
                },
                is_popular=True
            ),
            AgentTemplate(
                id=3,
                name="Invoice Email Processor",
                description="Extract invoice data from emails and log to spreadsheet",
                category="email",
                icon="💰",
                deployment_count=1500,
                rating=4.6,
                estimated_setup_time="60 seconds",
                time_savings="5 hours/week",
                roi_estimate="200% productivity gain",
                features=[
                    "Invoice detection",
                    "Data extraction",
                    "Google Sheets logging",
                    "Receipt archiving"
                ],
                integrations=["Gmail", "Google Sheets"],
                config_schema={
                    "sheet_id": "",
                    "folder_id": "",
                    "invoice_keywords": ["invoice", "receipt", "bill"]
                }
            ),

            # SALES CATEGORY
            AgentTemplate(
                id=4,
                name="Lead Qualification Bot",
                description="Auto-qualify leads from web forms and emails",
                category="sales",
                icon="🎯",
                deployment_count=2400,
                rating=4.9,
                estimated_setup_time="90 seconds",
                time_savings="15 hours/week",
                roi_estimate="500% productivity gain",
                features=[
                    "Smart lead scoring",
                    "Automatic enrichment",
                    "CRM integration",
                    "Follow-up scheduling"
                ],
                integrations=["HubSpot", "Salesforce", "Gmail"],
                config_schema={
                    "minimum_score": 70,
                    "auto_assign": True,
                    "notification_method": "slack"
                },
                is_featured=True,
                is_popular=True
            ),
            AgentTemplate(
                id=5,
                name="Sales Follow-up Automation",
                description="Automated follow-up sequences for leads",
                category="sales",
                icon="📞",
                deployment_count=1900,
                rating=4.7,
                estimated_setup_time="60 seconds",
                time_savings="12 hours/week",
                roi_estimate="450% productivity gain",
                features=[
                    "Multi-touch sequences",
                    "Personalization",
                    "Response tracking",
                    "A/B testing"
                ],
                integrations=["Gmail", "Salesforce"],
                config_schema={
                    "sequence_days": [1, 3, 7, 14],
                    "personalization_fields": ["company", "name", "industry"]
                },
                is_popular=True
            ),
            AgentTemplate(
                id=6,
                name="Meeting Scheduler",
                description="Auto-schedule meetings with qualified leads",
                category="sales",
                icon="📅",
                deployment_count=1600,
                rating=4.5,
                estimated_setup_time="45 seconds",
                time_savings="6 hours/week",
                roi_estimate="250% productivity gain",
                features=[
                    "Calendar integration",
                    "Time zone handling",
                    "Confirmation emails",
                    "Reminder automation"
                ],
                integrations=["Google Calendar", "Gmail", "Calendly"],
                config_schema={
                    "buffer_time": 15,
                    "working_hours": "9-17",
                    "timezone": "Europe/Oslo"
                }
            ),

            # SUPPORT CATEGORY
            AgentTemplate(
                id=7,
                name="Customer Support Triager",
                description="Auto-categorize and route support tickets",
                category="support",
                icon="🎫",
                deployment_count=2100,
                rating=4.8,
                estimated_setup_time="60 seconds",
                time_savings="10 hours/week",
                roi_estimate="400% productivity gain",
                features=[
                    "Smart categorization",
                    "Priority detection",
                    "Auto-routing",
                    "SLA tracking"
                ],
                integrations=["Zendesk", "Intercom", "Slack"],
                config_schema={
                    "categories": ["technical", "billing", "general"],
                    "auto_assign": True,
                    "sla_hours": 24
                },
                is_featured=True
            ),
            AgentTemplate(
                id=8,
                name="FAQ Responder",
                description="AI-powered responses to common support questions",
                category="support",
                icon="❓",
                deployment_count=1800,
                rating=4.6,
                estimated_setup_time="30 seconds",
                time_savings="8 hours/week",
                roi_estimate="320% productivity gain",
                features=[
                    "Knowledge base integration",
                    "Natural language understanding",
                    "Multi-channel support",
                    "Escalation rules"
                ],
                integrations=["Zendesk", "Intercom", "Slack"],
                config_schema={
                    "confidence_threshold": 0.8,
                    "auto_reply": False,
                    "escalate_on_low_confidence": True
                }
            ),

            # MARKETING CATEGORY
            AgentTemplate(
                id=9,
                name="Social Media Scheduler",
                description="Auto-schedule and post content across platforms",
                category="marketing",
                icon="📱",
                deployment_count=2600,
                rating=4.7,
                estimated_setup_time="90 seconds",
                time_savings="10 hours/week",
                roi_estimate="400% productivity gain",
                features=[
                    "Multi-platform posting",
                    "Best time optimization",
                    "Content calendar",
                    "Analytics tracking"
                ],
                integrations=["Twitter", "LinkedIn", "Facebook"],
                config_schema={
                    "platforms": ["twitter", "linkedin"],
                    "posting_schedule": "optimal",
                    "timezone": "Europe/Oslo"
                },
                is_popular=True
            ),
            AgentTemplate(
                id=10,
                name="Content Repurposer",
                description="Convert blog posts to social media content",
                category="marketing",
                icon="♻️",
                deployment_count=1400,
                rating=4.5,
                estimated_setup_time="60 seconds",
                time_savings="6 hours/week",
                roi_estimate="250% productivity gain",
                features=[
                    "Multi-format conversion",
                    "Key points extraction",
                    "Hashtag generation",
                    "Image suggestions"
                ],
                integrations=["WordPress", "Twitter", "LinkedIn"],
                config_schema={
                    "source_url": "",
                    "output_formats": ["tweet", "linkedin_post"],
                    "include_images": True
                }
            ),

            # PRODUCTIVITY CATEGORY
            AgentTemplate(
                id=11,
                name="Meeting Notes Summarizer",
                description="Auto-generate meeting summaries and action items",
                category="productivity",
                icon="📝",
                deployment_count=2200,
                rating=4.9,
                estimated_setup_time="45 seconds",
                time_savings="8 hours/week",
                roi_estimate="350% productivity gain",
                features=[
                    "Transcript analysis",
                    "Action item extraction",
                    "Participant tagging",
                    "Auto-distribution"
                ],
                integrations=["Zoom", "Google Meet", "Slack"],
                config_schema={
                    "distribution_method": "email",
                    "action_item_tracking": True,
                    "summary_format": "bullet_points"
                },
                is_featured=True
            ),
            AgentTemplate(
                id=12,
                name="Expense Report Automation",
                description="Auto-process receipts and create expense reports",
                category="productivity",
                icon="💳",
                deployment_count=1700,
                rating=4.6,
                estimated_setup_time="60 seconds",
                time_savings="4 hours/week",
                roi_estimate="200% productivity gain",
                features=[
                    "Receipt OCR",
                    "Category detection",
                    "Report generation",
                    "Approval workflow"
                ],
                integrations=["Gmail", "Google Sheets", "Expensify"],
                config_schema={
                    "receipt_folder": "",
                    "categories": ["travel", "meals", "office"],
                    "approval_required": True
                }
            ),

            # DATA & ANALYTICS
            AgentTemplate(
                id=13,
                name="Report Generator",
                description="Auto-generate weekly/monthly reports from data sources",
                category="productivity",
                icon="📊",
                deployment_count=1500,
                rating=4.7,
                estimated_setup_time="90 seconds",
                time_savings="10 hours/week",
                roi_estimate="400% productivity gain",
                features=[
                    "Multi-source data aggregation",
                    "Custom templates",
                    "Scheduled generation",
                    "Auto-distribution"
                ],
                integrations=["Google Analytics", "Salesforce", "Gmail"],
                config_schema={
                    "frequency": "weekly",
                    "recipients": [],
                    "include_charts": True
                }
            ),

            # E-COMMERCE
            AgentTemplate(
                id=14,
                name="Inventory Monitor",
                description="Monitor stock levels and auto-reorder",
                category="ecommerce",
                icon="📦",
                deployment_count=1300,
                rating=4.8,
                estimated_setup_time="90 seconds",
                time_savings="15 hours/week",
                roi_estimate="500% productivity gain",
                features=[
                    "Real-time monitoring",
                    "Low stock alerts",
                    "Auto-reordering",
                    "Supplier integration"
                ],
                integrations=["Shopify", "WooCommerce", "Gmail"],
                config_schema={
                    "reorder_threshold": 10,
                    "auto_reorder": False,
                    "notification_email": ""
                }
            ),

            # HR & RECRUITING
            AgentTemplate(
                id=15,
                name="Resume Screener",
                description="Auto-screen resumes and rank candidates",
                category="hr",
                icon="👔",
                deployment_count=1100,
                rating=4.6,
                estimated_setup_time="60 seconds",
                time_savings="12 hours/week",
                roi_estimate="450% productivity gain",
                features=[
                    "Resume parsing",
                    "Skill matching",
                    "Ranking algorithm",
                    "Interview scheduling"
                ],
                integrations=["Gmail", "Google Sheets", "Greenhouse"],
                config_schema={
                    "required_skills": [],
                    "minimum_experience": 2,
                    "auto_reject_threshold": 30
                }
            ),

            # FINANCE
            AgentTemplate(
                id=16,
                name="Payment Reminder Bot",
                description="Auto-send payment reminders to late invoices",
                category="finance",
                icon="💸",
                deployment_count=1600,
                rating=4.7,
                estimated_setup_time="45 seconds",
                time_savings="6 hours/week",
                roi_estimate="250% productivity gain",
                features=[
                    "Invoice tracking",
                    "Automated reminders",
                    "Escalation sequences",
                    "Payment confirmation"
                ],
                integrations=["Stripe", "QuickBooks", "Gmail"],
                config_schema={
                    "reminder_days": [7, 14, 30],
                    "escalation_enabled": True,
                    "payment_link": True
                }
            ),

            # OPERATIONS
            AgentTemplate(
                id=17,
                name="System Health Monitor",
                description="Monitor system health and auto-alert on issues",
                category="operations",
                icon="🏥",
                deployment_count=1900,
                rating=4.9,
                estimated_setup_time="90 seconds",
                time_savings="20 hours/week",
                roi_estimate="600% productivity gain",
                features=[
                    "Multi-system monitoring",
                    "Performance tracking",
                    "Auto-alerting",
                    "Incident logging"
                ],
                integrations=["Datadog", "New Relic", "Slack"],
                config_schema={
                    "check_interval": 5,
                    "alert_threshold": 95,
                    "notification_channel": "slack"
                },
                is_featured=True
            ),

            # INTEGRATION POWERHOUSES
            AgentTemplate(
                id=18,
                name="Zapier Alternative",
                description="Connect any two apps with custom automation",
                category="integration",
                icon="🔌",
                deployment_count=2900,
                rating=4.8,
                estimated_setup_time="120 seconds",
                time_savings="Varies",
                roi_estimate="Varies",
                features=[
                    "1000+ app integrations",
                    "Custom workflows",
                    "Error handling",
                    "Logging & analytics"
                ],
                integrations=["Custom"],
                config_schema={
                    "trigger_app": "",
                    "trigger_event": "",
                    "action_app": "",
                    "action_event": ""
                },
                is_popular=True
            ),

            # COMMUNICATION
            AgentTemplate(
                id=19,
                name="Slack Digest",
                description="Daily digest of important Slack messages",
                category="communication",
                icon="💬",
                deployment_count=1200,
                rating=4.5,
                estimated_setup_time="30 seconds",
                time_savings="4 hours/week",
                roi_estimate="200% productivity gain",
                features=[
                    "Smart filtering",
                    "Priority detection",
                    "Scheduled delivery",
                    "Custom keywords"
                ],
                integrations=["Slack", "Gmail"],
                config_schema={
                    "channels": [],
                    "keywords": [],
                    "delivery_time": "08:00"
                }
            ),

            # CUSTOMER SUCCESS
            AgentTemplate(
                id=20,
                name="Churn Predictor",
                description="Identify at-risk customers and trigger interventions",
                category="customer_success",
                icon="⚠️",
                deployment_count=1400,
                rating=4.9,
                estimated_setup_time="120 seconds",
                time_savings="15 hours/week",
                roi_estimate="500% productivity gain",
                features=[
                    "Behavior analysis",
                    "Risk scoring",
                    "Auto-interventions",
                    "Success tracking"
                ],
                integrations=["Mixpanel", "Intercom", "Salesforce"],
                config_schema={
                    "risk_threshold": 70,
                    "intervention_type": "email",
                    "track_metrics": ["login_frequency", "feature_usage"]
                },
                is_featured=True
            )
        ]

    def get_all_templates(self) -> List[AgentTemplate]:
        """Get all available templates"""
        return self.templates

    def get_template_by_id(self, template_id: int) -> Optional[AgentTemplate]:
        """Get specific template by ID"""
        return next(
            (t for t in self.templates if t.id == template_id),
            None
        )

    def get_templates_by_category(self, category: str) -> List[AgentTemplate]:
        """Get templates filtered by category"""
        return [t for t in self.templates if t.category == category]

    def get_featured_templates(self) -> List[AgentTemplate]:
        """Get featured templates"""
        return [t for t in self.templates if t.is_featured]

    def get_popular_templates(self) -> List[AgentTemplate]:
        """Get most popular templates"""
        return sorted(
            [t for t in self.templates if t.is_popular],
            key=lambda x: x.deployment_count,
            reverse=True
        )

    def search_templates(self, query: str) -> List[AgentTemplate]:
        """Search templates by name or description"""
        query_lower = query.lower()
        return [
            t for t in self.templates
            if query_lower in t.name.lower()
            or query_lower in t.description.lower()
        ]

    async def deploy_template(
        self,
        template_id: int,
        user_id: int,
        custom_config: Optional[Dict] = None
    ) -> Dict:
        """
        One-click template deployment

        Args:
            template_id: Template to deploy
            user_id: User deploying the template
            custom_config: Optional custom configuration

        Returns:
            Deployment result with agent_id and status
        """
        template = self.get_template_by_id(template_id)
        if not template:
            return {
                "success": False,
                "error": "Template not found"
            }

        # Merge default config with custom config
        config = {**template.config_schema, **(custom_config or {})}

        # Simulate deployment (replace with actual deployment logic)
        deployment_result = {
            "success": True,
            "agent_id": 12345,  # Would be from database
            "template_name": template.name,
            "deployment_time": "30 seconds",
            "status": "active",
            "config": config,
            "next_steps": [
                "Configure integrations",
                "Test the agent",
                "Monitor first runs",
                "Review results"
            ]
        }

        # Increment deployment count
        template.deployment_count += 1

        logger.info(
            f"Deployed template '{template.name}' for user {user_id}"
        )

        return deployment_result

    def get_marketplace_stats(self) -> Dict:
        """Get marketplace statistics"""
        return {
            "total_templates": len(self.templates),
            "total_deployments": sum(t.deployment_count for t in self.templates),
            "average_rating": sum(t.rating for t in self.templates) / len(self.templates),
            "categories": list(set(t.category for t in self.templates)),
            "featured_count": len([t for t in self.templates if t.is_featured]),
            "most_popular": max(self.templates, key=lambda x: x.deployment_count).name
        }


# Usage Example
def example_marketplace_usage():
    """Example of using the marketplace"""
    marketplace = AgentMarketplace()

    # Get all templates
    print(f"Total templates: {len(marketplace.get_all_templates())}")

    # Get featured
    featured = marketplace.get_featured_templates()
    print(f"\nFeatured templates ({len(featured)}):")
    for t in featured:
        print(f"  - {t.icon} {t.name}: {t.deployment_count} deployments")

    # Get popular
    popular = marketplace.get_popular_templates()
    print(f"\nMost popular:")
    for t in popular[:5]:
        print(f"  - {t.name}: {t.deployment_count} deployments ({t.rating}⭐)")

    # Search
    results = marketplace.search_templates("email")
    print(f"\nSearch 'email': {len(results)} results")

    # Get stats
    stats = marketplace.get_marketplace_stats()
    print(f"\nMarketplace Stats: {stats}")
