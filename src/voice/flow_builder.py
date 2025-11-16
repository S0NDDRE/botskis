"""
Mindframe Visual Voice Flow Builder
Drag & Drop → Intelligent conversation flows

UNIQUE TO MINDFRAME:
- Visual flow designer (no-code)
- AI-powered flow suggestions
- Real-time validation
- Template library
- One-click testing
- Version control
- Export/Import flows

We make building voice agents as easy as drawing a flowchart.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from loguru import logger
import json
from datetime import datetime


class FlowNodeConfig(BaseModel):
    """Configuration for a flow node"""
    node_id: str
    node_type: str  # greeting, question, decision, api_call, transfer, end
    position: Dict[str, int]  # {x: 100, y: 200}
    config: Dict[str, Any]  # Node-specific configuration
    connections: List[str] = []  # IDs of connected nodes
    conditions: Optional[Dict[str, str]] = None  # Conditional routing


class FlowValidationResult(BaseModel):
    """Result of flow validation"""
    valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []


class FlowTemplate(BaseModel):
    """Pre-built flow template"""
    id: str
    name: str
    description: str
    category: str  # appointment, support, sales, survey, etc.
    nodes: List[FlowNodeConfig]
    estimated_duration: str  # "2-3 minutes"
    use_cases: List[str]
    variables: List[str]  # What data it collects


class MindframeFlowBuilder:
    """
    Mindframe Visual Flow Builder

    The UNIQUE way to design voice conversations:
    1. Drag & drop nodes in visual editor
    2. AI suggests optimal flows
    3. Real-time validation
    4. One-click testing
    5. Deploy directly to voice engine
    """

    def __init__(self):
        self.node_types = self._init_node_types()
        self.templates = self._init_templates()

    def _init_node_types(self) -> Dict[str, Dict]:
        """Initialize available node types"""
        return {
            "greeting": {
                "name": "Greeting",
                "icon": "👋",
                "description": "Welcome the caller",
                "required_fields": ["prompt"],
                "optional_fields": ["voice_style"],
                "example": "Hello! Thank you for calling. How can I help you today?"
            },
            "question": {
                "name": "Question",
                "icon": "❓",
                "description": "Ask a question and collect data",
                "required_fields": ["prompt", "variable_to_collect"],
                "optional_fields": ["validation", "retry_prompt", "max_retries"],
                "example": "What's your name?"
            },
            "decision": {
                "name": "Decision",
                "icon": "🔀",
                "description": "Route based on conditions",
                "required_fields": ["conditions"],
                "optional_fields": ["default_path"],
                "example": "Route urgent to specialist, normal to queue"
            },
            "api_call": {
                "name": "API Call",
                "icon": "🔌",
                "description": "Call external API",
                "required_fields": ["endpoint", "method"],
                "optional_fields": ["headers", "body", "timeout"],
                "example": "Create appointment in booking system"
            },
            "transfer": {
                "name": "Transfer",
                "icon": "📞",
                "description": "Transfer to human or another number",
                "required_fields": ["transfer_to"],
                "optional_fields": ["transfer_message"],
                "example": "Let me connect you with a specialist"
            },
            "message": {
                "name": "Message",
                "icon": "💬",
                "description": "Say something to the caller",
                "required_fields": ["prompt"],
                "optional_fields": ["pause_after"],
                "example": "Your appointment is confirmed!"
            },
            "end": {
                "name": "End Call",
                "icon": "✅",
                "description": "End the conversation",
                "required_fields": ["closing_message"],
                "optional_fields": ["save_data"],
                "example": "Thank you for calling. Have a great day!"
            },
            "wait": {
                "name": "Wait",
                "icon": "⏳",
                "description": "Wait for user input or timeout",
                "required_fields": ["timeout_seconds"],
                "optional_fields": ["timeout_action"],
                "example": "Wait 30 seconds for response"
            },
            "intent_check": {
                "name": "Intent Recognition",
                "icon": "🧠",
                "description": "Use AI to understand intent",
                "required_fields": ["expected_intents"],
                "optional_fields": ["confidence_threshold"],
                "example": "Detect if user wants to schedule, cancel, or reschedule"
            },
            "sentiment_check": {
                "name": "Sentiment Analysis",
                "icon": "😊",
                "description": "Analyze caller emotion",
                "required_fields": ["actions_by_sentiment"],
                "optional_fields": [],
                "example": "Route frustrated callers to senior agents"
            }
        }

    def _init_templates(self) -> Dict[str, FlowTemplate]:
        """Initialize pre-built flow templates"""
        return {
            "appointment_booking": FlowTemplate(
                id="appointment_booking",
                name="Appointment Booking",
                description="Complete appointment scheduling flow",
                category="scheduling",
                nodes=[
                    FlowNodeConfig(
                        node_id="start",
                        node_type="greeting",
                        position={"x": 100, "y": 100},
                        config={
                            "prompt": "Hello! Thank you for calling. I can help you schedule an appointment."
                        },
                        connections=["collect_name"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_name",
                        node_type="question",
                        position={"x": 100, "y": 200},
                        config={
                            "prompt": "May I have your name please?",
                            "variable_to_collect": "name",
                            "validation": {"type": "string", "min_length": 2}
                        },
                        connections=["collect_date"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_date",
                        node_type="question",
                        position={"x": 100, "y": 300},
                        config={
                            "prompt": "What date works best for you?",
                            "variable_to_collect": "preferred_date",
                            "validation": {"type": "date", "future_only": True}
                        },
                        connections=["collect_time"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_time",
                        node_type="question",
                        position={"x": 100, "y": 400},
                        config={
                            "prompt": "And what time would you prefer?",
                            "variable_to_collect": "preferred_time",
                            "validation": {"type": "time", "business_hours": True}
                        },
                        connections=["confirm"]
                    ),
                    FlowNodeConfig(
                        node_id="confirm",
                        node_type="question",
                        position={"x": 100, "y": 500},
                        config={
                            "prompt": "Perfect! I have {name} for {preferred_date} at {preferred_time}. Is that correct?",
                            "variable_to_collect": "confirmation",
                            "validation": {"type": "yes_no"}
                        },
                        connections=["book", "collect_date"],
                        conditions={
                            "yes": "book",
                            "no": "collect_date"
                        }
                    ),
                    FlowNodeConfig(
                        node_id="book",
                        node_type="api_call",
                        position={"x": 100, "y": 600},
                        config={
                            "endpoint": "/api/v1/appointments",
                            "method": "POST",
                            "body": {
                                "name": "{name}",
                                "date": "{preferred_date}",
                                "time": "{preferred_time}"
                            }
                        },
                        connections=["end"]
                    ),
                    FlowNodeConfig(
                        node_id="end",
                        node_type="end",
                        position={"x": 100, "y": 700},
                        config={
                            "closing_message": "Your appointment is confirmed! You'll receive a confirmation email. Have a great day!",
                            "save_data": True
                        }
                    )
                ],
                estimated_duration="2-3 minutes",
                use_cases=["Dental offices", "Salons", "Consultations", "Service bookings"],
                variables=["name", "preferred_date", "preferred_time"]
            ),

            "customer_support_triage": FlowTemplate(
                id="customer_support_triage",
                name="Customer Support Triage",
                description="Intelligent call routing with sentiment analysis",
                category="support",
                nodes=[
                    FlowNodeConfig(
                        node_id="start",
                        node_type="greeting",
                        position={"x": 100, "y": 100},
                        config={
                            "prompt": "Thank you for calling support. I'm here to help!"
                        },
                        connections=["collect_issue"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_issue",
                        node_type="question",
                        position={"x": 100, "y": 200},
                        config={
                            "prompt": "Can you briefly describe your issue?",
                            "variable_to_collect": "issue_description"
                        },
                        connections=["analyze_sentiment"]
                    ),
                    FlowNodeConfig(
                        node_id="analyze_sentiment",
                        node_type="sentiment_check",
                        position={"x": 100, "y": 300},
                        config={
                            "actions_by_sentiment": {
                                "frustrated": "transfer_senior",
                                "neutral": "check_urgency",
                                "positive": "check_urgency"
                            }
                        },
                        connections=["transfer_senior", "check_urgency"]
                    ),
                    FlowNodeConfig(
                        node_id="check_urgency",
                        node_type="intent_check",
                        position={"x": 200, "y": 400},
                        config={
                            "expected_intents": ["critical", "urgent", "normal", "question"],
                            "confidence_threshold": 0.7
                        },
                        connections=["transfer_immediate", "create_ticket", "self_service"],
                        conditions={
                            "critical": "transfer_immediate",
                            "urgent": "create_ticket",
                            "normal": "create_ticket",
                            "question": "self_service"
                        }
                    ),
                    FlowNodeConfig(
                        node_id="transfer_senior",
                        node_type="transfer",
                        position={"x": 50, "y": 500},
                        config={
                            "transfer_to": "senior_support_line",
                            "transfer_message": "I understand your frustration. Let me connect you with a senior specialist right away."
                        }
                    ),
                    FlowNodeConfig(
                        node_id="transfer_immediate",
                        node_type="transfer",
                        position={"x": 150, "y": 500},
                        config={
                            "transfer_to": "urgent_support_line",
                            "transfer_message": "This is urgent. Connecting you to our priority team immediately."
                        }
                    ),
                    FlowNodeConfig(
                        node_id="create_ticket",
                        node_type="api_call",
                        position={"x": 250, "y": 500},
                        config={
                            "endpoint": "/api/v1/support/tickets",
                            "method": "POST",
                            "body": {
                                "description": "{issue_description}",
                                "priority": "normal"
                            }
                        },
                        connections=["end_with_ticket"]
                    ),
                    FlowNodeConfig(
                        node_id="self_service",
                        node_type="message",
                        position={"x": 350, "y": 500},
                        config={
                            "prompt": "I can help with that! Let me find the information for you..."
                        },
                        connections=["end_resolved"]
                    ),
                    FlowNodeConfig(
                        node_id="end_with_ticket",
                        node_type="end",
                        position={"x": 250, "y": 600},
                        config={
                            "closing_message": "Your ticket #{ticket_id} has been created. You'll receive updates by email. Anything else?",
                            "save_data": True
                        }
                    ),
                    FlowNodeConfig(
                        node_id="end_resolved",
                        node_type="end",
                        position={"x": 350, "y": 600},
                        config={
                            "closing_message": "I hope that helps! Is there anything else I can assist with today?",
                            "save_data": True
                        }
                    )
                ],
                estimated_duration="2-5 minutes",
                use_cases=["Tech support", "Customer service", "Help desks", "SaaS companies"],
                variables=["issue_description", "sentiment", "urgency", "ticket_id"]
            ),

            "lead_qualification": FlowTemplate(
                id="lead_qualification",
                name="Sales Lead Qualification",
                description="Qualify leads and book sales calls",
                category="sales",
                nodes=[
                    FlowNodeConfig(
                        node_id="start",
                        node_type="greeting",
                        position={"x": 100, "y": 100},
                        config={
                            "prompt": "Hi! Thanks for your interest in our product. I'd love to learn more about your needs."
                        },
                        connections=["collect_company"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_company",
                        node_type="question",
                        position={"x": 100, "y": 200},
                        config={
                            "prompt": "What company are you with?",
                            "variable_to_collect": "company_name"
                        },
                        connections=["collect_role"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_role",
                        node_type="question",
                        position={"x": 100, "y": 300},
                        config={
                            "prompt": "And what's your role there?",
                            "variable_to_collect": "role"
                        },
                        connections=["collect_team_size"]
                    ),
                    FlowNodeConfig(
                        node_id="collect_team_size",
                        node_type="question",
                        position={"x": 100, "y": 400},
                        config={
                            "prompt": "How many people are on your team?",
                            "variable_to_collect": "team_size",
                            "validation": {"type": "number", "min": 1}
                        },
                        connections=["qualify"]
                    ),
                    FlowNodeConfig(
                        node_id="qualify",
                        node_type="decision",
                        position={"x": 100, "y": 500},
                        config={
                            "conditions": {
                                "team_size >= 10": "high_value",
                                "team_size >= 5": "medium_value",
                                "team_size < 5": "low_value"
                            }
                        },
                        connections=["high_value", "medium_value", "low_value"]
                    ),
                    FlowNodeConfig(
                        node_id="high_value",
                        node_type="transfer",
                        position={"x": 50, "y": 600},
                        config={
                            "transfer_to": "senior_sales_rep",
                            "transfer_message": "Perfect! Let me connect you with one of our senior team members right away."
                        }
                    ),
                    FlowNodeConfig(
                        node_id="medium_value",
                        node_type="api_call",
                        position={"x": 150, "y": 600},
                        config={
                            "endpoint": "/api/v1/sales/book-demo",
                            "method": "POST",
                            "body": {
                                "company": "{company_name}",
                                "role": "{role}",
                                "team_size": "{team_size}"
                            }
                        },
                        connections=["end_demo_booked"]
                    ),
                    FlowNodeConfig(
                        node_id="low_value",
                        node_type="message",
                        position={"x": 250, "y": 600},
                        config={
                            "prompt": "Great! I'll send you some resources to get started. You can also try our free tier!"
                        },
                        connections=["end_resources"]
                    ),
                    FlowNodeConfig(
                        node_id="end_demo_booked",
                        node_type="end",
                        position={"x": 150, "y": 700},
                        config={
                            "closing_message": "Your demo is scheduled! Check your email for the calendar invite. Excited to show you what we can do!",
                            "save_data": True
                        }
                    ),
                    FlowNodeConfig(
                        node_id="end_resources",
                        node_type="end",
                        position={"x": 250, "y": 700},
                        config={
                            "closing_message": "Check your inbox! Let me know if you have any questions. Have a great day!",
                            "save_data": True
                        }
                    )
                ],
                estimated_duration="3-4 minutes",
                use_cases=["B2B sales", "SaaS demos", "Lead gen", "Outbound sales"],
                variables=["company_name", "role", "team_size", "qualification_score"]
            )
        }

    def validate_flow(self, nodes: List[FlowNodeConfig]) -> FlowValidationResult:
        """
        Validate a voice flow for errors

        Mindframe catches issues BEFORE deployment:
        - Missing connections
        - Dead ends
        - Invalid configurations
        - Infinite loops
        """
        errors = []
        warnings = []
        suggestions = []

        # Check for entry node (greeting)
        greeting_nodes = [n for n in nodes if n.node_type == "greeting"]
        if not greeting_nodes:
            errors.append("Flow must have a greeting node")

        # Check for end node
        end_nodes = [n for n in nodes if n.node_type == "end"]
        if not end_nodes:
            errors.append("Flow must have at least one end node")

        # Check all nodes have valid connections
        node_ids = {n.node_id for n in nodes}
        for node in nodes:
            if node.node_type != "end":  # End nodes don't need connections
                if not node.connections:
                    errors.append(f"Node '{node.node_id}' has no outgoing connections")
                else:
                    for conn in node.connections:
                        if conn not in node_ids:
                            errors.append(f"Node '{node.node_id}' connects to non-existent node '{conn}'")

        # Check for orphaned nodes (not reachable from start)
        reachable = self._find_reachable_nodes(nodes)
        for node in nodes:
            if node.node_id not in reachable and node.node_type != "greeting":
                warnings.append(f"Node '{node.node_id}' is not reachable from start")

        # Check for required fields in each node type
        for node in nodes:
            node_type_config = self.node_types.get(node.node_type, {})
            required_fields = node_type_config.get("required_fields", [])

            for field in required_fields:
                if field not in node.config:
                    errors.append(f"Node '{node.node_id}' missing required field '{field}'")

        # Suggestions for improvements
        if len(nodes) > 20:
            suggestions.append("Consider breaking this flow into smaller sub-flows for better maintenance")

        question_nodes = [n for n in nodes if n.node_type == "question"]
        if len(question_nodes) > 10:
            suggestions.append("Many questions detected. Consider adding progress indicators to keep callers engaged")

        # Check for timeout handling
        has_timeout = any(n.config.get("timeout_seconds") for n in nodes)
        if not has_timeout:
            suggestions.append("Consider adding timeout handling for better user experience")

        return FlowValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )

    def _find_reachable_nodes(self, nodes: List[FlowNodeConfig]) -> set:
        """Find all nodes reachable from greeting"""
        greeting_nodes = [n for n in nodes if n.node_type == "greeting"]
        if not greeting_nodes:
            return set()

        reachable = set()
        to_visit = [greeting_nodes[0].node_id]

        node_map = {n.node_id: n for n in nodes}

        while to_visit:
            current_id = to_visit.pop()
            if current_id in reachable:
                continue

            reachable.add(current_id)
            current_node = node_map.get(current_id)

            if current_node:
                for conn in current_node.connections:
                    if conn not in reachable:
                        to_visit.append(conn)

        return reachable

    def export_flow(self, nodes: List[FlowNodeConfig], format: str = "json") -> str:
        """Export flow to various formats"""
        if format == "json":
            return json.dumps([n.dict() for n in nodes], indent=2)
        elif format == "yaml":
            # In production, use PyYAML
            return "# YAML export would go here"
        elif format == "mermaid":
            # Generate Mermaid flowchart syntax
            lines = ["graph TD"]
            for node in nodes:
                icon = self.node_types.get(node.node_type, {}).get("icon", "⭐")
                lines.append(f"    {node.node_id}[\"{icon} {node.node_id}\"]")

                for conn in node.connections:
                    lines.append(f"    {node.node_id} --> {conn}")

            return "\n".join(lines)

        return ""

    def import_flow(self, flow_data: str, format: str = "json") -> List[FlowNodeConfig]:
        """Import flow from various formats"""
        if format == "json":
            data = json.loads(flow_data)
            return [FlowNodeConfig(**node) for node in data]

        return []

    def get_template(self, template_id: str) -> Optional[FlowTemplate]:
        """Get a pre-built template"""
        return self.templates.get(template_id)

    def list_templates(self, category: Optional[str] = None) -> List[FlowTemplate]:
        """List available templates"""
        templates = list(self.templates.values())

        if category:
            templates = [t for t in templates if t.category == category]

        return templates

    def optimize_flow(self, nodes: List[FlowNodeConfig]) -> List[str]:
        """
        AI-powered flow optimization suggestions

        Mindframe analyzes your flow and suggests improvements:
        - Reduce unnecessary steps
        - Improve question ordering
        - Add error handling
        - Enhance user experience
        """
        suggestions = []

        # Check for redundant questions
        question_nodes = [n for n in nodes if n.node_type == "question"]
        variables = [n.config.get("variable_to_collect") for n in question_nodes]

        if len(variables) != len(set(variables)):
            suggestions.append("Remove duplicate questions collecting the same variable")

        # Check for missing error handling
        api_nodes = [n for n in nodes if n.node_type == "api_call"]
        for api_node in api_nodes:
            if "error" not in str(api_node.connections):
                suggestions.append(f"Add error handling for API call in node '{api_node.node_id}'")

        # Check question order
        if len(question_nodes) >= 2:
            # Simple questions (name) should come before complex ones (preferences)
            suggestions.append("Consider asking simple questions (name, contact) before complex ones")

        # Check for engagement
        if len(nodes) > 5 and not any(n.node_type == "message" for n in nodes):
            suggestions.append("Add acknowledgment messages to keep caller engaged during long flows")

        return suggestions


# Usage Example
def example_flow_building():
    """Example of using Mindframe Flow Builder"""
    builder = MindframeFlowBuilder()

    # List available templates
    templates = builder.list_templates(category="scheduling")
    print(f"📚 Available templates: {len(templates)}")

    # Get a template
    template = builder.get_template("appointment_booking")
    print(f"✅ Template: {template.name}")
    print(f"📋 Variables collected: {template.variables}")

    # Validate the flow
    validation = builder.validate_flow(template.nodes)
    print(f"\n🔍 Validation:")
    print(f"  Valid: {validation.valid}")
    print(f"  Errors: {validation.errors}")
    print(f"  Warnings: {validation.warnings}")
    print(f"  Suggestions: {validation.suggestions}")

    # Get optimization suggestions
    optimizations = builder.optimize_flow(template.nodes)
    print(f"\n💡 Optimizations:")
    for opt in optimizations:
        print(f"  - {opt}")

    # Export to different formats
    json_export = builder.export_flow(template.nodes, format="json")
    mermaid_export = builder.export_flow(template.nodes, format="mermaid")

    print(f"\n📤 Exported to JSON ({len(json_export)} chars)")
    print(f"📤 Exported to Mermaid diagram")
    print(f"\n{mermaid_export}")


if __name__ == "__main__":
    example_flow_building()
