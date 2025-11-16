"""
Mindframe Academy - Learning Management System
Complete course system with AI assistance
"""
from .models import (
    Course,
    CourseModule,
    Lesson,
    CourseEnrollment,
    LessonProgress,
    LearningPath,
    Certificate,
    AICourseAssistant as AICourseInteraction,
    CourseLevel,
    CourseCategory,
    LessonType
)
from .ai_course_assistant import (
    MindframeAICourseAssistant,
    AssistantMessage,
    LearningContext
)
from .course_content import (
    COURSES,
    LEARNING_PATHS,
    get_course_by_id,
    get_learning_path,
    get_all_courses,
    get_courses_by_level,
    get_next_course_in_path
)

__all__ = [
    # Models
    "Course",
    "CourseModule",
    "Lesson",
    "CourseEnrollment",
    "LessonProgress",
    "LearningPath",
    "Certificate",
    "AICourseInteraction",
    "CourseLevel",
    "CourseCategory",
    "LessonType",
    # AI Assistant
    "MindframeAICourseAssistant",
    "AssistantMessage",
    "LearningContext",
    # Content
    "COURSES",
    "LEARNING_PATHS",
    "get_course_by_id",
    "get_learning_path",
    "get_all_courses",
    "get_courses_by_level",
    "get_next_course_in_path"
]
