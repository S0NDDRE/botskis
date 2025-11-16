"""
Mindframe Academy - Learning Management System Models
Complete course system with AI assistance

Features:
- Courses from Lærling (Apprentice) to CEO
- AI Course Assistant guides users
- Interactive lessons with quizzes
- Progress tracking
- Certification system
- Drag & drop course builder
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, JSON, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum

# Base for SQLAlchemy models
Base = declarative_base()


class CourseLevel(str, Enum):
    """Course difficulty levels"""
    LAERLING = "laerling"  # Apprentice - Basics
    JUNIOR = "junior"  # Junior - Intermediate
    MEDIOR = "medior"  # Mid-level - Advanced
    SENIOR = "senior"  # Senior - Expert
    LEAD = "lead"  # Team Lead - Leadership
    MANAGER = "manager"  # Manager - Management
    DIRECTOR = "director"  # Director - Strategy
    CEO = "ceo"  # CEO - Executive


class CourseCategory(str, Enum):
    """Course categories"""
    PLATFORM_BASICS = "platform_basics"  # How to use Mindframe
    AI_AGENT_BUILDER = "ai_agent_builder"  # AI Agent Generator
    VOICE_AI = "voice_ai"  # Voice AI System
    META_AI_GUARDIAN = "meta_ai_guardian"  # Self-improving AI
    AUTOMATION = "automation"  # Workflow automation
    INTEGRATIONS = "integrations"  # External integrations
    LEADERSHIP = "leadership"  # Leadership skills
    BUSINESS = "business"  # Business strategy
    SALES = "sales"  # Sales & Marketing
    TECHNICAL = "technical"  # Technical deep-dive


class LessonType(str, Enum):
    """Types of lessons"""
    VIDEO = "video"  # Video lesson
    TEXT = "text"  # Text/reading
    INTERACTIVE = "interactive"  # Interactive tutorial
    QUIZ = "quiz"  # Quiz/test
    EXERCISE = "exercise"  # Hands-on exercise
    PROJECT = "project"  # Build something
    AI_GUIDED = "ai_guided"  # AI assistant guides you


class Course(Base):
    """
    A complete course (e.g., "Mindframe for Beginners")
    """
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(SQLEnum(CourseCategory), nullable=False)
    level = Column(SQLEnum(CourseLevel), nullable=False)

    # Course metadata
    duration_minutes = Column(Integer, nullable=False)  # Total time
    thumbnail_url = Column(String(500))
    is_published = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)  # Requires Pro/Enterprise

    # Prerequisites
    prerequisites = Column(JSON, default=[])  # List of course IDs

    # Learning outcomes
    learning_outcomes = Column(JSON, default=[])  # What you'll learn

    # Certification
    awards_certificate = Column(Boolean, default=False)
    certificate_title = Column(String(200))  # e.g., "Mindframe Certified Professional"

    # Ordering
    order = Column(Integer, default=0)  # Display order

    # Stats
    enrolled_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("CourseEnrollment", back_populates="course")


class CourseModule(Base):
    """
    A module within a course (e.g., "Module 1: Getting Started")
    """
    __tablename__ = "course_modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text)
    order = Column(Integer, default=0)

    # Duration
    duration_minutes = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")


class Lesson(Base):
    """
    A single lesson within a module
    """
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text)
    lesson_type = Column(SQLEnum(LessonType), nullable=False)
    order = Column(Integer, default=0)

    # Content
    content = Column(JSON)  # Flexible content structure
    """
    Content structure examples:

    TEXT:
    {
        "markdown": "# Lesson content...",
        "estimated_reading_time": 10
    }

    VIDEO:
    {
        "video_url": "https://...",
        "transcript": "...",
        "duration_seconds": 300
    }

    INTERACTIVE:
    {
        "steps": [
            {
                "title": "Step 1",
                "instruction": "Click here...",
                "action": "click_button",
                "validation": {...}
            }
        ]
    }

    QUIZ:
    {
        "questions": [
            {
                "question": "What is...?",
                "type": "multiple_choice",
                "options": ["A", "B", "C"],
                "correct_answer": "B",
                "explanation": "..."
            }
        ]
    }

    AI_GUIDED:
    {
        "prompt": "AI will guide you through...",
        "objectives": ["Learn X", "Build Y"],
        "ai_personality": "friendly_mentor"
    }
    """

    # Duration
    duration_minutes = Column(Integer, default=0)

    # Resources
    resources = Column(JSON, default=[])  # Additional resources

    # Requirements
    requires_completion = Column(Boolean, default=True)  # Must complete to progress
    passing_score = Column(Integer, default=70)  # For quizzes (%)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    module = relationship("CourseModule", back_populates="lessons")
    progress = relationship("LessonProgress", back_populates="lesson")


class CourseEnrollment(Base):
    """
    User enrollment in a course
    """
    __tablename__ = "course_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    # Status
    status = Column(String(50), default="enrolled")  # enrolled, in_progress, completed, dropped

    # Progress
    progress_percentage = Column(Float, default=0.0)
    current_module_id = Column(Integer, ForeignKey("course_modules.id"), nullable=True)
    current_lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)

    # Time tracking
    total_time_spent_minutes = Column(Integer, default=0)

    # Completion
    completed_at = Column(DateTime, nullable=True)
    certificate_issued = Column(Boolean, default=False)
    certificate_id = Column(String(100), nullable=True)  # Unique cert ID

    # Timestamps
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="enrollments")


class LessonProgress(Base):
    """
    User progress on individual lessons
    """
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)

    # Status
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed, failed

    # Progress
    progress_percentage = Column(Float, default=0.0)

    # Quiz/Exercise results
    score = Column(Float, nullable=True)  # For quizzes (%)
    attempts = Column(Integer, default=0)
    answers = Column(JSON, default={})  # User's answers

    # Time tracking
    time_spent_minutes = Column(Integer, default=0)

    # Completion
    completed_at = Column(DateTime, nullable=True)

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    lesson = relationship("Lesson", back_populates="progress")


class LearningPath(Base):
    """
    A curated path of courses (e.g., "Lærling to CEO")
    """
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    level_start = Column(SQLEnum(CourseLevel), nullable=False)
    level_end = Column(SQLEnum(CourseLevel), nullable=False)

    # Path metadata
    thumbnail_url = Column(String(500))
    duration_hours = Column(Integer, default=0)

    # Courses in this path
    course_ids = Column(JSON, default=[])  # Ordered list of course IDs

    # Requirements
    is_premium = Column(Boolean, default=False)

    # Stats
    enrolled_count = Column(Integer, default=0)
    completion_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)


class Certificate(Base):
    """
    Course completion certificates
    """
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(String(100), unique=True, nullable=False)  # Unique ID

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    # Certificate details
    title = Column(String(200), nullable=False)
    description = Column(Text)

    # Verification
    verification_url = Column(String(500))  # Public URL to verify

    # PDF
    pdf_url = Column(String(500), nullable=True)

    # Issued
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration


class AICourseAssistant(Base):
    """
    AI Assistant interactions during courses
    Tracks conversations and helps users learn
    """
    __tablename__ = "ai_course_interactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)

    # Conversation
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)

    # Context
    context = Column(JSON, default={})  # What user was working on

    # Sentiment
    was_helpful = Column(Boolean, nullable=True)  # User feedback

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
