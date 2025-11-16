"""
Income Bot System Training Courses
Complete onboarding and training for income generation bots

Courses:
- Income Bot 101: Introduction
- Freelance Bot Mastery
- Testing Bot Expert
- Survey Bot Optimization
- Writing Bot Professional
- Complete Income System Manager
"""
from typing import Dict, List

# ============================================================================
# INCOME BOT TRAINING COURSES
# ============================================================================

INCOME_COURSES = {}

# ============================================================================
# COURSE 1: INCOME BOT 101 (Beginner)
# ============================================================================

INCOME_COURSES["income_bot_101"] = {
    "title": "Income Bot 101: Start Earning Today",
    "description": "Learn how to set up and run autonomous income bots that generate passive income 24/7",
    "category": "income_generation",
    "level": "beginner",
    "duration_minutes": 45,
    "awards_certificate": True,
    "certificate_title": "Income Bot Certified",
    "income_potential": "500-3,300 NOK/day",
    "learning_outcomes": [
        "Understand how income bots work",
        "Set up your first income bot in 5 minutes",
        "Start generating passive income immediately",
        "Monitor earnings in real-time"
    ],
    "modules": [
        {
            "title": "Module 1: Introduction to Income Bots",
            "duration_minutes": 15,
            "lessons": [
                {
                    "title": "What are Income Bots?",
                    "lesson_type": "video",
                    "duration_minutes": 5,
                    "content": {
                        "video_url": "https://mindframe.ai/courses/income-bots-intro.mp4",
                        "transcript": """
Welcome to Income Bot 101!

Income bots are autonomous AI agents that work 24/7 to generate passive income by:
- Finding freelance jobs
- Completing website tests
- Filling out surveys
- Writing content

All completely automated using AI.

Income Potential:
- 500-3,300 NOK per day
- 15,000-99,000 NOK per month
- 180,000-1,188,000 NOK per year

Best part? Set it up once, earn forever!
"""
                    }
                },
                {
                    "title": "The 4 Income Bots",
                    "lesson_type": "text",
                    "duration_minutes": 5,
                    "content": {
                        "markdown": """
# The 4 Income Bots

## 1. 💼 Freelance Bot
- **Platforms:** Upwork, Freelancer, FINN.no
- **Income:** 500-1,200 NOK/job
- **Tasks:** Writing, data entry, research
- **Monthly Potential:** 15,000-60,000 NOK

## 2. 🧪 Testing Bot
- **Platforms:** UserTesting, TestBirds
- **Income:** 20-30 NOK/test
- **Tasks:** Website testing, bug finding
- **Monthly Potential:** 3,000-9,000 NOK

## 3. 📋 Survey Bot
- **Platforms:** Swagbucks, ySense, Toluna
- **Income:** 5-15 NOK/survey
- **Tasks:** Complete surveys
- **Monthly Potential:** 1,500-6,000 NOK

## 4. ✍️ Writing Bot
- **Platforms:** Textbroker, iWriter
- **Income:** 30-80 NOK/article
- **Tasks:** Articles, blog posts
- **Monthly Potential:** 9,000-24,000 NOK

---

**Combined Monthly Potential:** 28,500-99,000 NOK! 💰
"""
                    }
                },
                {
                    "title": "Quick Quiz: Income Bots Basics",
                    "lesson_type": "quiz",
                    "duration_minutes": 5,
                    "content": {
                        "questions": [
                            {
                                "question": "How many income bots are included in Mindframe?",
                                "type": "multiple_choice",
                                "options": ["2 bots", "4 bots", "6 bots", "10 bots"],
                                "correct_answer": "4 bots"
                            },
                            {
                                "question": "What's the combined monthly income potential?",
                                "type": "multiple_choice",
                                "options": [
                                    "5,000-10,000 NOK",
                                    "15,000-30,000 NOK",
                                    "28,500-99,000 NOK",
                                    "100,000-200,000 NOK"
                                ],
                                "correct_answer": "28,500-99,000 NOK"
                            }
                        ]
                    }
                }
            ]
        },
        {
            "title": "Module 2: Your First Income Bot",
            "duration_minutes": 30,
            "lessons": [
                {
                    "title": "Step 1: Setup",
                    "lesson_type": "interactive",
                    "duration_minutes": 10,
                    "content": {
                        "steps": [
                            {
                                "title": "Install Income Bots",
                                "instruction": "Go to Marketplace → Income Generation → Click 'Install'",
                                "action": "navigate",
                                "target": "/marketplace"
                            },
                            {
                                "title": "Configure OpenAI Key",
                                "instruction": "Add your OpenAI API key in settings",
                                "action": "input",
                                "field": "openai_api_key"
                            },
                            {
                                "title": "Launch Your First Bot",
                                "instruction": "Click 'Start Bot' on Income Dashboard",
                                "action": "click",
                                "target": "start_bot_button"
                            }
                        ]
                    }
                },
                {
                    "title": "Step 2: Monitor Earnings",
                    "lesson_type": "ai_guided",
                    "duration_minutes": 15,
                    "content": {
                        "prompt": "I'll guide you through the Income Dashboard!",
                        "objectives": [
                            "Open Income Dashboard",
                            "View real-time earnings",
                            "Check bot status",
                            "Review recent transactions"
                        ]
                    }
                },
                {
                    "title": "Completion Test",
                    "lesson_type": "quiz",
                    "duration_minutes": 5,
                    "passing_score": 80
                }
            ]
        }
    ]
}

# ============================================================================
# COURSE 2: FREELANCE BOT MASTERY
# ============================================================================

INCOME_COURSES["freelance_bot_mastery"] = {
    "title": "Freelance Bot Mastery",
    "description": "Master the Freelance Income Bot - Earn 15,000-60,000 NOK/month",
    "category": "income_generation",
    "level": "intermediate",
    "duration_minutes": 120,
    "prerequisites": ["income_bot_101"],
    "awards_certificate": True,
    "certificate_title": "Freelance Bot Expert",
    "income_potential": "15,000-60,000 NOK/month",
    "modules": [
        {
            "title": "Freelance Bot Deep Dive",
            "lessons": [
                {
                    "title": "How the Freelance Bot Works",
                    "lesson_type": "video",
                    "duration_minutes": 20,
                    "content": {
                        "topics": [
                            "Job discovery algorithms",
                            "AI cover letter generation",
                            "Auto-application process",
                            "Job completion with AI",
                            "Income tracking"
                        ]
                    }
                },
                {
                    "title": "Optimize Your Settings",
                    "lesson_type": "interactive",
                    "duration_minutes": 30,
                    "content": {
                        "config_options": {
                            "platforms": ["upwork", "freelancer", "finn"],
                            "skills": ["writing", "data_entry", "web_research"],
                            "min_budget_nok": 500,
                            "max_applications_per_day": 10
                        }
                    }
                },
                {
                    "title": "Case Study: 50,000 NOK/Month",
                    "lesson_type": "text",
                    "duration_minutes": 15,
                    "content": {
                        "markdown": """
# Real User Results: 50,000 NOK/Month

**User:** Anonymous Beta Tester
**Period:** 30 days
**Platforms:** Upwork, Freelancer

## Results:
- **Jobs Applied:** 287
- **Jobs Accepted:** 43 (15% acceptance rate)
- **Jobs Completed:** 41 (95% completion rate)
- **Total Earnings:** 51,240 NOK
- **Average per Job:** 1,250 NOK

## Key Success Factors:
1. Ran bot 24/7
2. Targeted high-value jobs (800-1,500 NOK)
3. Focused on writing & research
4. Maintained 4.9★ rating
5. Quick turnaround times

## Tip:
Focus on QUALITY over quantity. 10 high-paying jobs > 50 low-paying jobs!
"""
                    }
                }
            ]
        }
    ]
}

# ============================================================================
# COURSE 3: TESTING BOT EXPERT
# ============================================================================

INCOME_COURSES["testing_bot_expert"] = {
    "title": "Website Testing Bot Expert",
    "description": "Become an expert at running the Testing Bot - Earn 3,000-9,000 NOK/month",
    "category": "income_generation",
    "level": "intermediate",
    "duration_minutes": 90,
    "prerequisites": ["income_bot_101"],
    "awards_certificate": True,
    "certificate_title": "Testing Bot Professional",
    "income_potential": "3,000-9,000 NOK/month",
    "modules": [
        {
            "title": "Testing Bot Mastery",
            "lessons": [
                {
                    "title": "Website Testing Fundamentals",
                    "lesson_type": "video",
                    "duration_minutes": 15
                },
                {
                    "title": "Maximize Tests Per Day",
                    "lesson_type": "interactive",
                    "duration_minutes": 25,
                    "content": {
                        "tips": [
                            "Claim tests quickly (first-come-first-served)",
                            "Run bot during peak hours (9am-5pm US time)",
                            "Target high-paying tests (25-30 NOK)",
                            "Maintain quality score >90%",
                            "Complete tests fast (10-15 min avg)"
                        ]
                    }
                }
            ]
        }
    ]
}

# ============================================================================
# COURSE 4: SURVEY BOT OPTIMIZATION
# ============================================================================

INCOME_COURSES["survey_bot_optimization"] = {
    "title": "Survey Bot Optimization",
    "description": "Optimize the Survey Bot for maximum earnings - 1,500-6,000 NOK/month",
    "category": "income_generation",
    "level": "intermediate",
    "duration_minutes": 75,
    "prerequisites": ["income_bot_101"],
    "awards_certificate": True,
    "certificate_title": "Survey Bot Optimizer",
    "income_potential": "1,500-6,000 NOK/month",
    "modules": [
        {
            "title": "Survey Bot Strategy",
            "lessons": [
                {
                    "title": "Profile Optimization",
                    "lesson_type": "interactive",
                    "duration_minutes": 20,
                    "content": {
                        "profile_setup": {
                            "age": "25-35 (highest demand)",
                            "location": "Norway",
                            "occupation": "Professional",
                            "interests": "Technology, Shopping, Travel"
                        }
                    }
                },
                {
                    "title": "Avoid Disqualification",
                    "lesson_type": "text",
                    "duration_minutes": 15,
                    "content": {
                        "tips": [
                            "Be consistent with answers",
                            "Pass attention checks",
                            "Don't rush (quality > speed)",
                            "Profile matches survey requirements",
                            "Realistic response times"
                        ]
                    }
                }
            ]
        }
    ]
}

# ============================================================================
# COURSE 5: WRITING BOT PROFESSIONAL
# ============================================================================

INCOME_COURSES["writing_bot_professional"] = {
    "title": "Writing Bot Professional",
    "description": "Master content writing with AI - Earn 9,000-24,000 NOK/month",
    "category": "income_generation",
    "level": "advanced",
    "duration_minutes": 150,
    "prerequisites": ["income_bot_101", "freelance_bot_mastery"],
    "awards_certificate": True,
    "certificate_title": "AI Writing Professional",
    "income_potential": "9,000-24,000 NOK/month",
    "modules": [
        {
            "title": "AI Content Creation Mastery",
            "lessons": [
                {
                    "title": "Writing High-Quality Content",
                    "lesson_type": "video",
                    "duration_minutes": 30
                },
                {
                    "title": "SEO Optimization",
                    "lesson_type": "text",
                    "duration_minutes": 25,
                    "content": {
                        "seo_checklist": [
                            "Keyword research",
                            "Natural keyword integration",
                            "Readability optimization",
                            "Proper heading structure (H1, H2, H3)",
                            "Meta descriptions"
                        ]
                    }
                },
                {
                    "title": "Practice: Write 5 Articles",
                    "lesson_type": "project",
                    "duration_minutes": 60,
                    "deliverables": [
                        "Article 1: AI Trends (600 words)",
                        "Article 2: Remote Work (500 words)",
                        "Article 3: Product Description (200 words)",
                        "Article 4: Blog Post (700 words)",
                        "Article 5: Review (400 words)"
                    ]
                }
            ]
        }
    ]
}

# ============================================================================
# COURSE 6: COMPLETE INCOME SYSTEM MANAGER
# ============================================================================

INCOME_COURSES["income_system_manager"] = {
    "title": "Complete Income System Manager",
    "description": "Run all 4 income bots like a pro - Maximize 28,500-99,000 NOK/month",
    "category": "income_generation",
    "level": "expert",
    "duration_minutes": 240,
    "prerequisites": [
        "income_bot_101",
        "freelance_bot_mastery",
        "testing_bot_expert",
        "survey_bot_optimization",
        "writing_bot_professional"
    ],
    "awards_certificate": True,
    "certificate_title": "Income System Manager - Master Level",
    "income_potential": "28,500-99,000 NOK/month",
    "is_premium": True,
    "modules": [
        {
            "title": "Running All 4 Bots Simultaneously",
            "lessons": [
                {
                    "title": "Resource Management",
                    "lesson_type": "video",
                    "duration_minutes": 30,
                    "topics": [
                        "CPU/Memory optimization",
                        "OpenAI API quota management",
                        "Parallel bot execution",
                        "Error handling & recovery",
                        "24/7 uptime strategies"
                    ]
                },
                {
                    "title": "Income Optimization Strategy",
                    "lesson_type": "ai_guided",
                    "duration_minutes": 60,
                    "objectives": [
                        "Analyze which bots perform best for YOU",
                        "Allocate resources to highest ROI bots",
                        "Create daily schedule",
                        "Set realistic income goals",
                        "Track and improve performance"
                    ]
                },
                {
                    "title": "Scaling to 100,000 NOK/Month",
                    "lesson_type": "text",
                    "duration_minutes": 45,
                    "content": {
                        "markdown": """
# Scaling Strategy: 100,000 NOK/Month

## Phase 1: Foundation (Month 1)
**Goal:** 28,500 NOK
- Run all 4 bots 24/7
- Learn platform patterns
- Optimize configs
- Track what works

## Phase 2: Optimization (Month 2-3)
**Goal:** 50,000 NOK
- Focus on highest-earning bots
- Increase daily limits
- Improve quality scores
- Faster turnaround times

## Phase 3: Scale (Month 4-6)
**Goal:** 75,000+ NOK
- Deploy multiple instances
- Cloud hosting for 24/7
- Advanced configs
- Platform expansion

## Phase 4: Mastery (Month 6+)
**Goal:** 100,000+ NOK
- Multiple accounts (where allowed)
- Team management
- Reinvest earnings
- Business entity setup

## Key Metrics to Track:
- ✅ Earnings per hour
- ✅ Job acceptance rate
- ✅ Completion rate
- ✅ Quality scores
- ✅ Platform diversity

**Remember:** 100K/month = 3,300 NOK/day. Absolutely achievable!
"""
                    }
                },
                {
                    "title": "Final Exam: Income System Manager",
                    "lesson_type": "quiz",
                    "duration_minutes": 30,
                    "passing_score": 90,
                    "questions_count": 50
                }
            ]
        }
    ]
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_income_course_by_id(course_id: str) -> Dict:
    """Get income course by ID"""
    return INCOME_COURSES.get(course_id)


def get_all_income_courses() -> List[Dict]:
    """Get all income courses"""
    return list(INCOME_COURSES.values())


def get_income_learning_path() -> Dict:
    """Get complete income bot learning path"""
    return {
        "title": "Income Bot Master Path",
        "description": "Fra 0 til 100,000 NOK/month med AI Income Bots",
        "duration_hours": 12,
        "income_potential": "28,500-99,000 NOK/month",
        "courses": [
            "income_bot_101",
            "freelance_bot_mastery",
            "testing_bot_expert",
            "survey_bot_optimization",
            "writing_bot_professional",
            "income_system_manager"
        ],
        "certification": "Income System Manager - Master Level"
    }
