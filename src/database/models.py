"""
Database models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    company = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    agents = relationship("Agent", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    onboarding = relationship("OnboardingSession", back_populates="user", uselist=False)


class Agent(Base):
    """Agent model"""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("agent_templates.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String)  # email, sales, support, etc.
    status = Column(String, default="active")  # active, paused, error
    config = Column(JSON)
    metrics = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="agents")
    template = relationship("AgentTemplate", back_populates="agents")
    runs = relationship("AgentRun", back_populates="agent")


class AgentTemplate(Base):
    """Agent marketplace templates"""
    __tablename__ = "agent_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # email, sales, support, marketing, productivity
    icon = Column(String)
    config_schema = Column(JSON)
    deployment_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agents = relationship("Agent", back_populates="template")


class OnboardingSession(Base):
    """Onboarding wizard sessions"""
    __tablename__ = "onboarding_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="started")  # started, in_progress, completed
    current_step = Column(Integer, default=1)
    total_steps = Column(Integer, default=5)
    answers = Column(JSON)
    recommendations = Column(JSON)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="onboarding")


class AgentRun(Base):
    """Agent execution runs"""
    __tablename__ = "agent_runs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    status = Column(String)  # running, success, failed, healing
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration = Column(Float)
    error_message = Column(Text)
    metrics = Column(JSON)
    auto_healed = Column(Boolean, default=False)

    # Relationships
    agent = relationship("Agent", back_populates="runs")


class Subscription(Base):
    """User subscriptions"""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    plan = Column(String)  # starter, professional, enterprise
    status = Column(String)  # active, cancelled, past_due
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscriptions")


class HealthCheck(Base):
    """System health monitoring"""
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String, nullable=False)  # api, database, redis, agents
    status = Column(String, nullable=False)  # healthy, degraded, down
    response_time = Column(Float)
    error_count = Column(Integer, default=0)
    last_error = Column(Text)
    checked_at = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON)
