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
    "awards_certificate": True,
    "certificate_title": "Certified AI Agent Builder",
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

COURSES["platform_basics"] = {
    "title": "Mindframe Platform Mastery",
    "description": "Complete guide to all Mindframe features",
    "category": "platform_basics",
    "level": "laerling",
    "duration_minutes": 120,
    "awards_certificate": True,
    "certificate_title": "Platform Expert Certificate",
    "modules": [
        {
            "title": "Platform Deep Dive",
            "lessons": [
                {"title": "Dashboard Tour", "lesson_type": "interactive", "duration_minutes": 20},
                {"title": "All Features Overview", "lesson_type": "video", "duration_minutes": 30},
                {"title": "Best Practices", "lesson_type": "text", "duration_minutes": 15}
            ]
        }
    ]
}

COURSES["voice_ai_introduction"] = {
    "title": "Voice AI Introduction",
    "description": "Build AI phone agents that can talk to customers",
    "category": "voice_ai",
    "level": "junior",
    "duration_minutes": 150,
    "awards_certificate": True,
    "certificate_title": "Voice AI Specialist",
    "modules": [
        {
            "title": "Voice AI Basics",
            "lessons": [
                {"title": "What is Voice AI?", "lesson_type": "video", "duration_minutes": 15},
                {"title": "Your First Voice Agent", "lesson_type": "project", "duration_minutes": 45},
                {"title": "Voice AI vs Text AI", "lesson_type": "text", "duration_minutes": 10}
            ]
        }
    ]
}

COURSES["workflow_automation"] = {
    "title": "Workflow Automation Mastery",
    "description": "Automate complex business workflows",
    "category": "automation",
    "level": "junior",
    "duration_minutes": 180,
    "awards_certificate": True,
    "certificate_title": "Automation Expert",
    "modules": [
        {
            "title": "Automation Patterns",
            "lessons": [
                {"title": "Common Workflows", "lesson_type": "video", "duration_minutes": 20},
                {"title": "Build: Order Processing", "lesson_type": "project", "duration_minutes": 60},
                {"title": "Error Handling", "lesson_type": "interactive", "duration_minutes": 30}
            ]
        }
    ]
}

# MEDIOR LEVEL
COURSES["advanced_ai_agents"] = {
    "title": "Advanced AI Agent Development",
    "description": "Expert-level agent building techniques",
    "category": "ai_agent_builder",
    "level": "medior",
    "duration_minutes": 240,
    "prerequisites": ["ai_agent_builder_fundamentals"],
    "awards_certificate": True,
    "certificate_title": "Advanced Agent Developer",
    "modules": [
        {
            "title": "Advanced Techniques",
            "lessons": [
                {"title": "Complex Logic Patterns", "lesson_type": "video", "duration_minutes": 30},
                {"title": "Multi-Agent Systems", "lesson_type": "interactive", "duration_minutes": 45},
                {"title": "Build: Smart CRM Agent", "lesson_type": "project", "duration_minutes": 90}
            ]
        }
    ]
}

COURSES["voice_ai_mastery"] = {
    "title": "Voice AI Mastery",
    "description": "Advanced voice AI implementation",
    "category": "voice_ai",
    "level": "medior",
    "duration_minutes": 200,
    "prerequisites": ["voice_ai_introduction"],
    "awards_certificate": True,
    "certificate_title": "Voice AI Master",
    "modules": [
        {
            "title": "Advanced Voice Features",
            "lessons": [
                {"title": "Custom Voice Training", "lesson_type": "video", "duration_minutes": 25},
                {"title": "Multi-language Support", "lesson_type": "interactive", "duration_minutes": 30},
                {"title": "Build: Customer Service Bot", "lesson_type": "project", "duration_minutes": 75}
            ]
        }
    ]
}

COURSES["integrations_deep_dive"] = {
    "title": "Integrations Deep Dive",
    "description": "Connect Mindframe to your entire tech stack",
    "category": "integrations",
    "level": "medior",
    "duration_minutes": 180,
    "awards_certificate": True,
    "certificate_title": "Integration Specialist",
    "modules": [
        {
            "title": "Integration Patterns",
            "lessons": [
                {"title": "API Integrations", "lesson_type": "video", "duration_minutes": 30},
                {"title": "Webhooks Setup", "lesson_type": "interactive", "duration_minutes": 25},
                {"title": "Build: Slack Integration", "lesson_type": "project", "duration_minutes": 60}
            ]
        }
    ]
}

# SENIOR LEVEL
COURSES["meta_ai_guardian_expert"] = {
    "title": "Meta-AI Guardian Expert",
    "description": "Master the self-improving AI system",
    "category": "meta_ai_guardian",
    "level": "senior",
    "duration_minutes": 240,
    "is_premium": True,
    "awards_certificate": True,
    "certificate_title": "Meta-AI Guardian Certified",
    "modules": [
        {
            "title": "Guardian Deep Dive",
            "lessons": [
                {"title": "How Guardian Works", "lesson_type": "video", "duration_minutes": 40},
                {"title": "Optimization Strategies", "lesson_type": "text", "duration_minutes": 30},
                {"title": "Approval Workflows", "lesson_type": "interactive", "duration_minutes": 45},
                {"title": "Build: Custom Guardian Rules", "lesson_type": "project", "duration_minutes": 75}
            ]
        }
    ]
}

COURSES["system_optimization"] = {
    "title": "System Optimization & Performance",
    "description": "Optimize your Mindframe setup for maximum efficiency",
    "category": "technical",
    "level": "senior",
    "duration_minutes": 200,
    "awards_certificate": True,
    "certificate_title": "Optimization Expert",
    "modules": [
        {
            "title": "Performance Tuning",
            "lessons": [
                {"title": "Performance Metrics", "lesson_type": "video", "duration_minutes": 25},
                {"title": "Bottleneck Analysis", "lesson_type": "interactive", "duration_minutes": 40},
                {"title": "Optimization Project", "lesson_type": "project", "duration_minutes": 80}
            ]
        }
    ]
}

COURSES["advanced_automation"] = {
    "title": "Advanced Automation Techniques",
    "description": "Master complex automation scenarios",
    "category": "automation",
    "level": "senior",
    "duration_minutes": 220,
    "awards_certificate": True,
    "certificate_title": "Automation Master",
    "modules": [
        {
            "title": "Complex Automations",
            "lessons": [
                {"title": "State Machines", "lesson_type": "video", "duration_minutes": 30},
                {"title": "Event-Driven Architecture", "lesson_type": "text", "duration_minutes": 25},
                {"title": "Build: E-commerce Automation", "lesson_type": "project", "duration_minutes": 90}
            ]
        }
    ]
}

# LEAD LEVEL
COURSES["team_leadership"] = {
    "title": "Leading AI-First Teams",
    "description": "Lead teams in the AI automation era",
    "category": "leadership",
    "level": "lead",
    "duration_minutes": 180,
    "awards_certificate": True,
    "certificate_title": "AI Team Leader",
    "modules": [
        {
            "title": "Leadership in AI Era",
            "lessons": [
                {"title": "Team Dynamics with AI", "lesson_type": "video", "duration_minutes": 30},
                {"title": "Delegation Strategies", "lesson_type": "interactive", "duration_minutes": 40},
                {"title": "Team Assessment", "lesson_type": "ai_guided", "duration_minutes": 60}
            ]
        }
    ]
}

COURSES["delegate_with_ai"] = {
    "title": "Delegate with AI",
    "description": "Use AI to 10x your team's productivity",
    "category": "leadership",
    "level": "lead",
    "duration_minutes": 160,
    "awards_certificate": True,
    "certificate_title": "AI Delegation Expert",
    "modules": [
        {
            "title": "Smart Delegation",
            "lessons": [
                {"title": "What to Delegate to AI", "lesson_type": "video", "duration_minutes": 25},
                {"title": "Task Assignment Patterns", "lesson_type": "interactive", "duration_minutes": 35},
                {"title": "Build: Team Workflow", "lesson_type": "project", "duration_minutes": 70}
            ]
        }
    ]
}

COURSES["productivity_management"] = {
    "title": "Productivity Management",
    "description": "Maximize team productivity with AI",
    "category": "leadership",
    "level": "lead",
    "duration_minutes": 150,
    "awards_certificate": True,
    "certificate_title": "Productivity Manager",
    "modules": [
        {
            "title": "Productivity Systems",
            "lessons": [
                {"title": "Metrics That Matter", "lesson_type": "video", "duration_minutes": 20},
                {"title": "Productivity Tools", "lesson_type": "interactive", "duration_minutes": 30},
                {"title": "Implement Productivity System", "lesson_type": "project", "duration_minutes": 65}
            ]
        }
    ]
}

# MANAGER LEVEL
COURSES["metrics_and_analytics"] = {
    "title": "Metrics & Analytics for Managers",
    "description": "Data-driven decision making with AI",
    "category": "business",
    "level": "manager",
    "duration_minutes": 140,
    "awards_certificate": True,
    "certificate_title": "Analytics Manager",
    "modules": [
        {
            "title": "Business Analytics",
            "lessons": [
                {"title": "Key Metrics", "lesson_type": "video", "duration_minutes": 25},
                {"title": "Dashboard Creation", "lesson_type": "interactive", "duration_minutes": 35},
                {"title": "Analytics Report", "lesson_type": "project", "duration_minutes": 55}
            ]
        }
    ]
}

COURSES["customer_success"] = {
    "title": "AI-Powered Customer Success",
    "description": "Deliver exceptional customer experience with AI",
    "category": "business",
    "level": "manager",
    "duration_minutes": 160,
    "awards_certificate": True,
    "certificate_title": "Customer Success Manager",
    "modules": [
        {
            "title": "Customer Success with AI",
            "lessons": [
                {"title": "Customer Journey Mapping", "lesson_type": "video", "duration_minutes": 30},
                {"title": "AI Support Systems", "lesson_type": "interactive", "duration_minutes": 40},
                {"title": "Build: Support System", "lesson_type": "project", "duration_minutes": 60}
            ]
        }
    ]
}

# DIRECTOR LEVEL
COURSES["strategic_ai_implementation"] = {
    "title": "Strategic AI Implementation",
    "description": "Implement AI at scale across your organization",
    "category": "business",
    "level": "director",
    "duration_minutes": 200,
    "is_premium": True,
    "awards_certificate": True,
    "certificate_title": "AI Strategy Director",
    "modules": [
        {
            "title": "AI Strategy",
            "lessons": [
                {"title": "Strategic Planning", "lesson_type": "video", "duration_minutes": 35},
                {"title": "Organizational Change", "lesson_type": "text", "duration_minutes": 30},
                {"title": "Create Strategy", "lesson_type": "ai_guided", "duration_minutes": 80}
            ]
        }
    ]
}

COURSES["scaling_operations"] = {
    "title": "Scaling Operations with AI",
    "description": "Scale your business 10x with AI automation",
    "category": "business",
    "level": "director",
    "duration_minutes": 210,
    "is_premium": True,
    "awards_certificate": True,
    "certificate_title": "Operations Director",
    "modules": [
        {
            "title": "Scaling Strategies",
            "lessons": [
                {"title": "Scale Without Hiring", "lesson_type": "video", "duration_minutes": 40},
                {"title": "Infrastructure Planning", "lesson_type": "interactive", "duration_minutes": 50},
                {"title": "Scale Plan", "lesson_type": "ai_guided", "duration_minutes": 75}
            ]
        }
    ]
}

COURSES["competitive_advantage"] = {
    "title": "Competitive Advantage Through AI",
    "description": "Use AI to dominate your market",
    "category": "business",
    "level": "director",
    "duration_minutes": 190,
    "is_premium": True,
    "awards_certificate": True,
    "certificate_title": "Strategic Advantage Director",
    "modules": [
        {
            "title": "Market Domination",
            "lessons": [
                {"title": "AI as Competitive Weapon", "lesson_type": "video", "duration_minutes": 35},
                {"title": "Case Studies", "lesson_type": "text", "duration_minutes": 40},
                {"title": "Your Strategy", "lesson_type": "ai_guided", "duration_minutes": 70}
            ]
        }
    ]
}

# CEO LEVEL
COURSES["market_domination"] = {
    "title": "Market Domination with AI",
    "description": "Become the market leader through AI adoption",
    "category": "business",
    "level": "ceo",
    "duration_minutes": 220,
    "is_premium": True,
    "awards_certificate": True,
    "certificate_title": "Market Leader CEO",
    "modules": [
        {
            "title": "Market Leadership",
            "lessons": [
                {"title": "AI Market Trends", "lesson_type": "video", "duration_minutes": 40},
                {"title": "Competitor Analysis", "lesson_type": "text", "duration_minutes": 35},
                {"title": "Domination Strategy", "lesson_type": "ai_guided", "duration_minutes": 90}
            ]
        }
    ]
}

COURSES["executive_vision"] = {
    "title": "Executive Vision: AI-First Future",
    "description": "Lead your organization into the AI-first future",
    "category": "business",
    "level": "ceo",
    "duration_minutes": 200,
    "is_premium": True,
    "awards_certificate": True,
    "certificate_title": "Visionary CEO",
    "modules": [
        {
            "title": "Future Leadership",
            "lessons": [
                {"title": "AI Future Trends", "lesson_type": "video", "duration_minutes": 45},
                {"title": "Vision Creation", "lesson_type": "ai_guided", "duration_minutes": 90},
                {"title": "Executive Roadmap", "lesson_type": "project", "duration_minutes": 50}
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
