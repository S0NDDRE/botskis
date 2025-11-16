"""
Mindframe Income Generation System

Autonomous income bots that generate revenue 24/7:
- Freelance Bot (Upwork, Freelancer, FINN.no)
- Testing Bot (UserTesting, TestBirds)
- Survey Bot (Swagbucks, ySense)
- Writing Bot (Textbroker, iWriter)

Income Potential: 500-2,000 NOK/day fully automated
"""
from src.income.freelance_bot import FreelanceBot, FreelanceBotConfig
from src.income.testing_bot import WebsiteTestingBot, TestingBotConfig
from src.income.survey_bot import SurveyBot, SurveyBotConfig
from src.income.writing_bot import WritingBot, WritingBotConfig
from src.income.income_tracker import IncomeTracker, IncomeStats

__all__ = [
    "FreelanceBot",
    "FreelanceBotConfig",
    "WebsiteTestingBot",
    "TestingBotConfig",
    "SurveyBot",
    "SurveyBotConfig",
    "WritingBot",
    "WritingBotConfig",
    "IncomeTracker",
    "IncomeStats",
]

__version__ = "1.0.0"
