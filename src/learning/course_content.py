"""
Mindframe Academy - Complete Course Content
From Lærling (Apprentice) to CEO

All courses, modules, and lessons predefined
"""
from typing import Dict, List, Optional

# ============================================================================
# LEARNING PATH: LÆRLING → CEO
# ============================================================================

LEARNING_PATHS = {
    "laerling_to_ceo": {
        "title": "Mindframe Mastery: Fra Lærling til CEO",
        "description": "Komplett læringsvei fra nybegynner til executive-nivå",
        "level_start": "laerling",
        "level_end": "ceo",
        "duration_hours": 120,
        "courses": [
            # LÆRLING LEVEL (Basics)
            "mindframe_101",
            "first_ai_agent",
            "platform_basics",

            # JUNIOR LEVEL (Intermediate)
            "ai_agent_builder_fundamentals",
            "voice_ai_introduction",
            "workflow_automation",

            # MEDIOR LEVEL (Advanced)
            "advanced_ai_agents",
            "voice_ai_mastery",
            "integrations_deep_dive",

            # SENIOR LEVEL (Expert)
            "meta_ai_guardian_expert",
            "system_optimization",
            "advanced_automation",

            # LEAD LEVEL (Leadership)
            "team_leadership",
            "delegate_with_ai",
            "productivity_management",

            # MANAGER LEVEL (Management)
            "roi_optimization",
            "metrics_and_analytics",
            "customer_success",

            # DIRECTOR LEVEL (Strategy)
            "strategic_ai_implementation",
            "scaling_operations",
            "competitive_advantage",

            # CEO LEVEL (Executive)
            "ai_transformation",
            "market_domination",
            "executive_vision"
        ]
    }
}

# ============================================================================
# COURSES: LÆRLING LEVEL (Basics)
# ============================================================================

COURSES = {}

# Course 1: Mindframe 101
COURSES["mindframe_101"] = {
    "title": "Mindframe 101: Getting Started",
    "description": "Learn the absolute basics of Mindframe platform",
    "category": "platform_basics",
    "level": "laerling",
    "duration_minutes": 60,
    "awards_certificate": True,
    "certificate_title": "Mindframe Fundamentals Certificate",
    "learning_outcomes": [
        "Understand what Mindframe is and what it can do",
        "Navigate the Mindframe platform",
        "Create your first account and workspace",
        "Know the key features and where to find them"
    ],
    "modules": [
        {
            "title": "Module 1: Welcome to Mindframe",
            "duration_minutes": 20,
            "lessons": [
                {
                    "title": "What is Mindframe?",
                    "lesson_type": "video",
                    "duration_minutes": 5,
                    "content": {
                        "video_url": "https://example.com/intro.mp4",
                        "transcript": "Welcome to Mindframe...",
                        "duration_seconds": 300
                    }
                },
                {
                    "title": "Platform Tour",
                    "lesson_type": "interactive",
                    "duration_minutes": 10,
                    "content": {
                        "steps": [
                            {
                                "title": "Dashboard",
                                "instruction": "This is your dashboard. Click to explore.",
                                "action": "click",
                                "target": "dashboard_button"
                            },
                            {
                                "title": "Agent Marketplace",
                                "instruction": "Here you find pre-built AI agents.",
                                "action": "navigate",
                                "target": "/marketplace"
                            }
                        ]
                    }
                },
                {
                    "title": "Quick Quiz: Platform Basics",
                    "lesson_type": "quiz",
                    "duration_minutes": 5,
                    "content": {
                        "questions": [
                            {
                                "question": "What can Mindframe help you automate?",
                                "type": "multiple_choice",
                                "options": [
                                    "Only emails",
                                    "Workflows, voice calls, and AI agents",
                                    "Just phone calls",
                                    "Nothing"
                                ],
                                "correct_answer": "Workflows, voice calls, and AI agents",
                                "explanation": "Mindframe is a complete AI automation platform with agents, voice AI, and workflows!"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "title": "Module 2: Your First Steps",
            "duration_minutes": 40,
            "lessons": [
                {
                    "title": "Setting Up Your Account",
                    "lesson_type": "ai_guided",
                    "duration_minutes": 15,
                    "content": {
                        "prompt": "I'll guide you through setting up your Mindframe account step by step!",
                        "objectives": [
                            "Create account",
                            "Choose package",
                            "Set up profile",
                            "Explore dashboard"
                        ],
                        "ai_personality": "friendly_mentor"
                    }
                },
                {
                    "title": "Build Your First AI Agent",
                    "lesson_type": "project",
                    "duration_minutes": 20,
                    "content": {
                        "project_title": "Email Auto-Responder",
                        "description": "Build an AI agent that automatically responds to customer emails",
                        "steps": [
                            "Go to AI Agent Generator",
                            "Type: 'Auto-respond to customer emails'",
                            "Review the generated agent",
                            "Deploy it!",
                            "Test by sending an email"
                        ],
                        "validation": {
                            "agent_created": True,
                            "agent_deployed": True
                        }
                    }
                },
                {
                    "title": "Completion Quiz",
                    "lesson_type": "quiz",
                    "duration_minutes": 5,
                    "passing_score": 80
                }
            ]
        }
    ]
}

# Course 2: Your First AI Agent
COURSES["first_ai_agent"] = {
    "title": "Your First AI Agent",
    "description": "Master the AI Agent Generator",
    "category": "ai_agent_builder",
    "level": "laerling",
    "duration_minutes": 90,
    "awards_certificate": True,
    "certificate_title": "AI Agent Builder Certificate",
    "modules": [
        {
            "title": "Understanding AI Agents",
            "lessons": [
                {
                    "title": "What is an AI Agent?",
                    "lesson_type": "text",
                    "content": {
                        "markdown": """
# What is an AI Agent?

An AI Agent is like a **smart assistant** that can:
- Read and understand messages
- Make decisions
- Take actions automatically
- Work 24/7 without breaks

## Examples:
- Email responder
- Customer support bot
- Task scheduler
- Data analyzer

## How it works:
1. You tell Mindframe what you want (in plain English/Norwegian)
2. AI creates the agent for you
3. Agent starts working immediately

**No coding needed!** 🚀
""",
                        "estimated_reading_time": 5
                    }
                }
            ]
        }
    ]
}

# ============================================================================
# COURSES: JUNIOR LEVEL
# ============================================================================

COURSES["ai_agent_builder_fundamentals"] = {
    "title": "AI Agent Builder Fundamentals",
    "description": "Deep dive into building powerful AI agents",
    "category": "ai_agent_builder",
    "level": "junior",
    "duration_minutes": 180,
    "prerequisites": ["mindframe_101", "first_ai_agent"],
    "modules": [
        {
            "title": "Advanced Agent Patterns",
            "lessons": [
                {
                    "title": "Multi-step Workflows",
                    "lesson_type": "video",
                    "duration_minutes": 15
                },
                {
                    "title": "Conditional Logic",
                    "lesson_type": "interactive",
                    "duration_minutes": 20
                },
                {
                    "title": "Build: Smart Email Triage",
                    "lesson_type": "project",
                    "duration_minutes": 30
                }
            ]
        }
    ]
}

# ============================================================================
# COURSES: MANAGER/CEO LEVEL
# ============================================================================

COURSES["roi_optimization"] = {
    "title": "ROI Optimization with AI",
    "description": "Maximize return on investment using Mindframe",
    "category": "business",
    "level": "manager",
    "duration_minutes": 120,
    "learning_outcomes": [
        "Calculate ROI of AI automation",
        "Identify high-impact automation opportunities",
        "Measure and track cost savings",
        "Present results to stakeholders"
    ],
    "modules": [
        {
            "title": "Measuring AI Impact",
            "lessons": [
                {
                    "title": "ROI Calculation Framework",
                    "lesson_type": "text",
                    "content": {
                        "markdown": """
# ROI Calculation Framework

## Formula:
```
ROI = (Savings - Cost) / Cost × 100%
```

## Example:
**Before Mindframe:**
- 5 employees handling emails
- 40 hours/week each
- $50/hour average cost
- Total: $10,000/week

**After Mindframe:**
- 1 employee monitoring AI
- 8 hours/week
- $50/hour
- Total: $400/week
- Mindframe cost: $99/month

**Savings:**
- Weekly: $10,000 - $400 = $9,600
- Monthly: $38,400
- Cost: $99
- ROI: 38,700%!

## Your Task:
Calculate ROI for YOUR use case
"""
                    }
                }
            ]
        }
    ]
}

COURSES["ai_transformation"] = {
    "title": "AI-Driven Business Transformation",
    "description": "Transform your entire organization with AI",
    "category": "business",
    "level": "ceo",
    "duration_minutes": 240,
    "is_premium": True,
    "learning_outcomes": [
        "Develop AI transformation strategy",
        "Lead organizational change",
        "Create competitive advantage through AI",
        "Build AI-first culture",
        "Scale AI across all departments"
    ],
    "modules": [
        {
            "title": "Executive AI Strategy",
            "lessons": [
                {
                    "title": "Vision: AI-First Organization",
                    "lesson_type": "video",
                    "duration_minutes": 20
                },
                {
                    "title": "Case Study: Mindframe Success Stories",
                    "lesson_type": "text",
                    "duration_minutes": 30
                },
                {
                    "title": "Your Transformation Roadmap",
                    "lesson_type": "ai_guided",
                    "duration_minutes": 60,
                    "content": {
                        "prompt": "Let's create a customized AI transformation roadmap for YOUR company",
                        "objectives": [
                            "Define vision",
                            "Identify opportunities",
                            "Create 90-day plan",
                            "Set success metrics"
                        ]
                    }
                }
            ]
        },
        {
            "title": "Market Domination Strategy",
            "lessons": [
                {
                    "title": "Competitive Advantage Through AI",
                    "lesson_type": "text",
                    "content": {
                        "markdown": """
# Market Domination with Mindframe

## The Unfair Advantage:

### What Your Competitors Have:
- Manual processes
- Human limitations
- 9-5 operations
- Slow response times
- High error rates
- Limited scalability

### What YOU Have with Mindframe:
- ✅ 24/7 AI automation
- ✅ Instant responses
- ✅ Perfect accuracy
- ✅ Unlimited scale
- ✅ Self-improving systems
- ✅ Meta-AI Guardian (UNIQUE!)

## Your Strategy:

### Phase 1: Internal Transformation (Month 1-3)
- Automate all repetitive work
- Deploy AI agents across departments
- Train team on Mindframe

### Phase 2: Customer Excellence (Month 4-6)
- AI-powered customer support
- Instant response times
- Personalized experiences
- Customers love you!

### Phase 3: Market Domination (Month 7-12)
- Operate at 10x efficiency
- Undercut competitors on price
- Outperform on quality
- Scale faster than anyone

### The Result:
**You become the market leader while competitors struggle to keep up.**

This is how you dominate! 🚀
"""
                    }
                }
            ]
        }
    ]
}

# ============================================================================
# DRAG & DROP COURSE BUILDER STRUCTURE
# ============================================================================

COURSE_BUILDER_COMPONENTS = {
    "lesson_types": [
        {
            "type": "video",
            "icon": "🎥",
            "label": "Video Lesson",
            "draggable": True,
            "fields": ["title", "video_url", "duration", "transcript"]
        },
        {
            "type": "text",
            "icon": "📝",
            "label": "Text/Reading",
            "draggable": True,
            "fields": ["title", "markdown_content", "estimated_reading_time"]
        },
        {
            "type": "interactive",
            "icon": "🎮",
            "label": "Interactive Tutorial",
            "draggable": True,
            "fields": ["title", "steps", "validation_rules"]
        },
        {
            "type": "quiz",
            "icon": "❓",
            "label": "Quiz/Test",
            "draggable": True,
            "fields": ["title", "questions", "passing_score"]
        },
        {
            "type": "exercise",
            "icon": "💪",
            "label": "Hands-on Exercise",
            "draggable": True,
            "fields": ["title", "instructions", "validation"]
        },
        {
            "type": "project",
            "icon": "🏗️",
            "label": "Build Project",
            "draggable": True,
            "fields": ["title", "description", "steps", "deliverables"]
        },
        {
            "type": "ai_guided",
            "icon": "🤖",
            "label": "AI-Guided Lesson",
            "draggable": True,
            "fields": ["title", "prompt", "objectives", "ai_personality"]
        }
    ],
    "question_types": [
        {
            "type": "multiple_choice",
            "label": "Multiple Choice",
            "example": {
                "question": "What is...?",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "B"
            }
        },
        {
            "type": "true_false",
            "label": "True/False",
            "example": {
                "question": "Is this correct?",
                "correct_answer": True
            }
        },
        {
            "type": "fill_in_blank",
            "label": "Fill in the Blank",
            "example": {
                "question": "The capital of Norway is ____",
                "correct_answer": "Oslo"
            }
        },
        {
            "type": "code",
            "label": "Code Exercise",
            "example": {
                "question": "Write a function that...",
                "starter_code": "def my_function():\n    pass",
                "test_cases": []
            }
        }
    ]
}


def get_course_by_id(course_id: str) -> Dict:
    """Get course by ID"""
    return COURSES.get(course_id)


def get_learning_path(path_id: str) -> Dict:
    """Get learning path by ID"""
    return LEARNING_PATHS.get(path_id)


def get_all_courses() -> List[Dict]:
    """Get all courses"""
    return list(COURSES.values())


def get_courses_by_level(level: str) -> List[Dict]:
    """Get courses for specific level"""
    return [c for c in COURSES.values() if c.get("level") == level]


def get_next_course_in_path(current_course_id: str, path_id: str = "laerling_to_ceo") -> Optional[str]:
    """Get next course in learning path"""
    path = LEARNING_PATHS.get(path_id)
    if not path:
        return None

    courses = path.get("courses", [])
    try:
        current_index = courses.index(current_course_id)
        if current_index < len(courses) - 1:
            return courses[current_index + 1]
    except ValueError:
        pass

    return None
