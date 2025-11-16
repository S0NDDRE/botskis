"""
FastAPI Application - Main API
Complete REST API for Botskis platform
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from config.settings import settings
from src.database.connection import get_db, init_db
from src.database.models import User, Agent, AgentTemplate, OnboardingSession
from src.core.onboarding_wizard import OnboardingWizard, OnboardingAnswer
from src.marketplace.agent_marketplace import AgentMarketplace
from src.monitoring.auto_healing import AutoHealingSystem

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Agent Automation Platform",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
onboarding_wizard = OnboardingWizard(openai_api_key=settings.openai_api_key)
marketplace = AgentMarketplace()
auto_healing = AutoHealingSystem()


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    company: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    company: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OnboardingStartRequest(BaseModel):
    user_id: int


class OnboardingAnswerRequest(BaseModel):
    question_id: str
    answer: str | List[str]


class OnboardingSubmitRequest(BaseModel):
    user_id: int
    answers: List[OnboardingAnswerRequest]


class AgentDeployRequest(BaseModel):
    template_id: int
    custom_config: Optional[dict] = None


class AgentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.api_version,
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """System health check"""
    health = await auto_healing.monitor_system_health()
    summary = auto_healing.get_system_health_summary()

    return {
        "status": summary["overall_status"],
        "timestamp": datetime.utcnow().isoformat(),
        "components": summary["components"],
        "average_response_time_ms": summary["average_response_time_ms"]
    }


@app.get("/metrics")
async def get_metrics():
    """Prometheus-compatible metrics"""
    summary = auto_healing.get_system_health_summary()
    analytics = auto_healing.get_error_analytics()

    return {
        "system_health": summary,
        "errors": analytics,
        "marketplace_stats": marketplace.get_marketplace_stats()
    }


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create new user account"""
    # Check if user exists
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user (hash password in production)
    new_user = User(
        email=user.email,
        hashed_password=user.password,  # Hash this!
        full_name=user.full_name,
        company=user.company
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ============================================================================
# ONBOARDING ENDPOINTS
# ============================================================================

@app.post("/api/v1/onboarding/start")
async def start_onboarding(
    request: OnboardingStartRequest,
    db: Session = Depends(get_db)
):
    """Start onboarding process"""
    # Check if user exists
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create onboarding session
    session = OnboardingSession(
        user_id=request.user_id,
        status="started",
        current_step=1,
        total_steps=len(onboarding_wizard.questions)
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "questions": [q.dict() for q in onboarding_wizard.questions],
        "total_steps": session.total_steps,
        "estimated_time": "5 minutes"
    }


@app.post("/api/v1/onboarding/submit")
async def submit_onboarding(
    request: OnboardingSubmitRequest,
    db: Session = Depends(get_db)
):
    """Submit onboarding answers and get recommendations"""
    # Get onboarding session
    session = db.query(OnboardingSession).filter(
        OnboardingSession.user_id == request.user_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Onboarding session not found"
        )

    # Convert answers
    answers = [
        OnboardingAnswer(
            question_id=a.question_id,
            answer=a.answer
        )
        for a in request.answers
    ]

    # Analyze user needs
    analysis = await onboarding_wizard.analyze_user_needs(answers)

    # Get agent recommendations
    templates = [t.dict() for t in marketplace.get_all_templates()]
    recommendations = await onboarding_wizard.recommend_agents(
        analysis,
        templates
    )

    # Update session
    session.status = "completed"
    session.current_step = session.total_steps
    session.completed_at = datetime.utcnow()
    session.answers = [a.dict() for a in answers]
    session.recommendations = [r.dict() for r in recommendations]
    db.commit()

    return {
        "session_id": session.id,
        "analysis": analysis,
        "recommendations": [r.dict() for r in recommendations],
        "next_step": "Deploy your first agent!"
    }


# ============================================================================
# MARKETPLACE ENDPOINTS
# ============================================================================

@app.get("/api/v1/marketplace/templates")
async def get_all_templates():
    """Get all agent templates"""
    templates = marketplace.get_all_templates()
    return {
        "total": len(templates),
        "templates": [t.dict() for t in templates]
    }


@app.get("/api/v1/marketplace/templates/{template_id}")
async def get_template(template_id: int):
    """Get specific template"""
    template = marketplace.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    return template.dict()


@app.get("/api/v1/marketplace/featured")
async def get_featured_templates():
    """Get featured templates"""
    templates = marketplace.get_featured_templates()
    return {
        "total": len(templates),
        "templates": [t.dict() for t in templates]
    }


@app.get("/api/v1/marketplace/popular")
async def get_popular_templates():
    """Get most popular templates"""
    templates = marketplace.get_popular_templates()
    return {
        "total": len(templates),
        "templates": [t.dict() for t in templates]
    }


@app.get("/api/v1/marketplace/category/{category}")
async def get_templates_by_category(category: str):
    """Get templates by category"""
    templates = marketplace.get_templates_by_category(category)
    return {
        "category": category,
        "total": len(templates),
        "templates": [t.dict() for t in templates]
    }


@app.get("/api/v1/marketplace/search")
async def search_templates(q: str):
    """Search templates"""
    templates = marketplace.search_templates(q)
    return {
        "query": q,
        "total": len(templates),
        "templates": [t.dict() for t in templates]
    }


@app.get("/api/v1/marketplace/stats")
async def get_marketplace_stats():
    """Get marketplace statistics"""
    return marketplace.get_marketplace_stats()


# ============================================================================
# AGENT ENDPOINTS
# ============================================================================

@app.post("/api/v1/agents/deploy", status_code=status.HTTP_201_CREATED)
async def deploy_agent(
    request: AgentDeployRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Deploy agent from template"""
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Deploy from marketplace
    result = await marketplace.deploy_template(
        template_id=request.template_id,
        user_id=user_id,
        custom_config=request.custom_config
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Deployment failed")
        )

    # Get template
    template = marketplace.get_template_by_id(request.template_id)

    # Create agent in database
    agent = Agent(
        user_id=user_id,
        template_id=request.template_id,
        name=template.name,
        description=template.description,
        type=template.category,
        status="active",
        config=result["config"]
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "success": True,
        "agent_id": agent.id,
        "template_name": template.name,
        "deployment_time": result["deployment_time"],
        "status": agent.status,
        "next_steps": result["next_steps"]
    }


@app.get("/api/v1/agents", response_model=List[AgentResponse])
async def get_user_agents(user_id: int, db: Session = Depends(get_db)):
    """Get all agents for a user"""
    agents = db.query(Agent).filter(Agent.user_id == user_id).all()
    return agents


@app.get("/api/v1/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get specific agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent


@app.post("/api/v1/agents/{agent_id}/pause")
async def pause_agent(agent_id: int, db: Session = Depends(get_db)):
    """Pause an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    agent.status = "paused"
    db.commit()

    return {
        "success": True,
        "agent_id": agent_id,
        "status": agent.status
    }


@app.post("/api/v1/agents/{agent_id}/resume")
async def resume_agent(agent_id: int, db: Session = Depends(get_db)):
    """Resume a paused agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    agent.status = "active"
    db.commit()

    return {
        "success": True,
        "agent_id": agent_id,
        "status": agent.status
    }


@app.delete("/api/v1/agents/{agent_id}")
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )

    db.delete(agent)
    db.commit()

    return {
        "success": True,
        "message": f"Agent {agent_id} deleted"
    }


# ============================================================================
# MONITORING ENDPOINTS
# ============================================================================

@app.get("/api/v1/monitoring/health")
async def get_system_health():
    """Get detailed system health"""
    return auto_healing.get_system_health_summary()


@app.get("/api/v1/monitoring/errors")
async def get_error_analytics():
    """Get error analytics"""
    return auto_healing.get_error_analytics()


@app.get("/api/v1/monitoring/agents/{agent_id}/health")
async def get_agent_health(agent_id: int):
    """Get health status for specific agent"""
    # This would check agent-specific health
    return {
        "agent_id": agent_id,
        "status": "healthy",
        "last_run": datetime.utcnow().isoformat(),
        "error_count": 0,
        "success_rate": 100.0
    }


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print(f"Starting {settings.app_name}...")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")

    # Initialize database
    if settings.debug:
        print("Initializing database...")
        init_db()

    print("API ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print(f"Shutting down {settings.app_name}...")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers
    )
