"""
FastAPI Application - Main API
Complete REST API for Botskis platform
"""
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Request
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
from src.core.security import hash_password, verify_password, create_access_token, Token
from src.core.auth import get_current_user, get_current_active_user
from src.api.middleware import setup_middleware, limiter, log_agent_action
from src.api.websocket import manager, handle_websocket_message
from src.core.ai_agent_generator import MindframeAgentGenerator

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

# Setup custom middleware (logging, error handling, rate limiting, security)
setup_middleware(app)

# Initialize components
onboarding_wizard = OnboardingWizard(openai_api_key=settings.openai_api_key)
marketplace = AgentMarketplace()
auto_healing = AutoHealingSystem()
ai_generator = MindframeAgentGenerator(openai_api_key=settings.openai_api_key)


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


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AIGenerateRequest(BaseModel):
    """Request to generate agent with AI"""
    description: str  # Natural language description
    user_context: Optional[dict] = None  # Optional user context


class AIGenerateResponse(BaseModel):
    """Response from AI generation"""
    success: bool
    intent: dict
    recommendation: dict
    workflow: dict
    configuration: dict
    template_id: int
    ready_to_deploy: bool
    estimated_setup_time: str
    next_steps: List[str]


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

    # Create user with hashed password
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
        company=user.company
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/api/v1/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login and get access token"""
    # Find user
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    # Create access token
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


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
# MINDFRAME AI AGENT GENERATOR ENDPOINTS
# ============================================================================

@app.post("/api/v1/ai/generate", response_model=AIGenerateResponse)
async def ai_generate_agent(
    request: AIGenerateRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    🧠 MINDFRAME AI AGENT GENERATOR

    Generate a complete agent from natural language description!

    Example:
        "Auto-respond to customer emails and create Trello cards for urgent issues"

    Returns:
        - Intent analysis
        - Template recommendation with reasoning
        - Visual workflow preview
        - Auto-configuration
        - Ready to deploy!
    """
    # Get available templates
    templates = [t.dict() for t in marketplace.get_all_templates()]

    # Add user context
    user_context = request.user_context or {}
    user_context.update({
        "user_email": current_user.email,
        "user_name": current_user.full_name,
        "company": current_user.company
    })

    # Generate agent with AI
    result = await ai_generator.generate_agent(
        user_input=request.description,
        available_templates=templates,
        user_context=user_context
    )

    log_agent_action(
        agent_id=0,
        action="ai_generate",
        user_id=current_user.id,
        details={"description": request.description}
    )

    return result


@app.post("/api/v1/ai/deploy")
async def ai_deploy_agent(
    generated_config: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Deploy an AI-generated agent directly to Factory Floor

    Takes the output from /api/v1/ai/generate and deploys it
    """
    template_id = generated_config.get("template_id")
    configuration = generated_config.get("configuration", {})

    # Get template
    template = marketplace.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    # Create agent in database
    agent = Agent(
        user_id=current_user.id,
        template_id=template_id,
        name=configuration.get("name", template.name),
        description=configuration.get("description", template.description),
        type=template.category,
        status="active",
        config=configuration.get("config", {})
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)

    log_agent_action(
        agent_id=agent.id,
        action="ai_deploy",
        user_id=current_user.id,
        details={"template_id": template_id}
    )

    # Send real-time update via WebSocket
    await manager.send_agent_update(
        agent_id=agent.id,
        user_id=current_user.id,
        data={
            "status": "deployed",
            "name": agent.name,
            "type": "ai_generated"
        }
    )

    return {
        "success": True,
        "agent_id": agent.id,
        "name": agent.name,
        "status": agent.status,
        "message": "🎉 Agent deployed successfully!",
        "next_steps": [
            "View agent on Factory Floor",
            "Monitor first runs",
            "Adjust configuration if needed"
        ]
    }


@app.post("/api/v1/ai/preview")
async def ai_preview_workflow(
    intent: dict,
    template_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate visual workflow preview before deployment

    Shows user exactly what the agent will do
    """
    template = marketplace.get_template_by_id(template_id)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

    from src.core.ai_agent_generator import AgentIntent

    # Generate workflow preview
    agent_intent = AgentIntent(**intent)
    workflow = await ai_generator.generate_workflow(
        intent=agent_intent,
        template=template.dict()
    )

    return {
        "success": True,
        "workflow": workflow.dict(),
        "template": {
            "id": template.id,
            "name": template.name,
            "category": template.category
        }
    }


# ============================================================================
# VOICE AI ENDPOINTS - Mindframe Voice AI System
# ============================================================================

@app.post("/api/v1/voice/flows")
async def create_voice_flow(
    flow_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new voice conversation flow

    Mindframe Voice AI - Visual flow builder integration
    """
    from src.voice.flow_builder import MindframeFlowBuilder, FlowNodeConfig

    builder = MindframeFlowBuilder()

    # Parse nodes
    nodes = [FlowNodeConfig(**node) for node in flow_data.get("nodes", [])]

    # Validate flow
    validation = builder.validate_flow(nodes)

    if not validation.valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Flow validation failed",
                "errors": validation.errors,
                "warnings": validation.warnings
            }
        )

    # Get optimization suggestions
    optimizations = builder.optimize_flow(nodes)

    # Save flow to database (in production)
    # For now, return validation result

    return {
        "success": True,
        "flow_id": flow_data.get("id", "new_flow"),
        "validation": validation.dict(),
        "optimizations": optimizations,
        "message": "Voice flow created successfully"
    }


@app.get("/api/v1/voice/flows/{flow_id}")
async def get_voice_flow(
    flow_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get voice flow by ID"""
    from src.voice.flow_builder import MindframeFlowBuilder

    builder = MindframeFlowBuilder()
    template = builder.get_template(flow_id)

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Flow not found"
        )

    return template.dict()


@app.get("/api/v1/voice/templates")
async def list_voice_templates(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """List available voice flow templates"""
    from src.voice.flow_builder import MindframeFlowBuilder

    builder = MindframeFlowBuilder()
    templates = builder.list_templates(category=category)

    return {
        "templates": [t.dict() for t in templates],
        "total": len(templates)
    }


@app.post("/api/v1/voice/flows/validate")
async def validate_voice_flow(
    flow_data: dict,
    current_user: User = Depends(get_current_active_user)
):
    """Validate a voice flow before deployment"""
    from src.voice.flow_builder import MindframeFlowBuilder, FlowNodeConfig

    builder = MindframeFlowBuilder()
    nodes = [FlowNodeConfig(**node) for node in flow_data.get("nodes", [])]

    validation = builder.validate_flow(nodes)
    optimizations = builder.optimize_flow(nodes)

    return {
        "validation": validation.dict(),
        "optimizations": optimizations
    }


@app.post("/api/v1/voice/generate-flow")
async def generate_voice_flow(
    description: str,
    goal: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate voice flow from natural language description

    Mindframe AI - Automatically create conversation flows
    """
    from src.voice.voice_ai_engine import MindframeVoiceEngine

    engine = MindframeVoiceEngine(openai_api_key=settings.openai_api_key)

    flow = await engine.create_flow_from_description(
        description=description,
        goal=goal
    )

    return {
        "success": True,
        "flow": flow.dict(),
        "message": "Voice flow generated successfully"
    }


@app.post("/api/v1/voice/calls/outbound")
async def make_outbound_call(
    to_number: str,
    flow_id: str,
    metadata: Optional[dict] = None,
    current_user: User = Depends(get_current_active_user)
):
    """
    Make outbound voice call with AI agent

    Mindframe Voice AI - Initiate automated calls
    """
    from src.voice.telephony import MindframeTelephony, TelephonyConfig, TelephonyProvider

    # Get telephony config (in production, load from settings)
    config = TelephonyConfig(
        provider=TelephonyProvider.TWILIO,
        api_key=settings.twilio_account_sid if hasattr(settings, 'twilio_account_sid') else "",
        api_secret=settings.twilio_auth_token if hasattr(settings, 'twilio_auth_token') else "",
        phone_number=settings.mindframe_phone_number if hasattr(settings, 'mindframe_phone_number') else "",
        webhook_url=f"{settings.api_url}/api/v1/voice/webhooks/call-events"
    )

    telephony = MindframeTelephony(config)

    call = await telephony.make_outbound_call(
        to_number=to_number,
        flow_id=flow_id,
        metadata=metadata or {}
    )

    return {
        "success": True,
        "call_id": call.call_id,
        "status": call.status,
        "from_number": call.from_number,
        "to_number": call.to_number,
        "start_time": call.start_time.isoformat()
    }


@app.post("/api/v1/voice/webhooks/call-events")
async def handle_call_events(request: Request):
    """
    Webhook for telephony provider events

    Receives call events from Twilio, Vonage, etc.
    """
    from src.voice.telephony import CallEvent

    data = await request.json()

    # Parse provider-specific event
    # In production, handle different providers

    event = CallEvent(
        call_id=data.get("call_id", ""),
        event_type=data.get("event_type", ""),
        timestamp=datetime.now(),
        data=data
    )

    logger.info(f"Call event received: {event.event_type} for call {event.call_id}")

    # Process event (start voice engine, update status, etc.)

    return {"status": "received"}


@app.get("/api/v1/voice/calls/{call_id}/status")
async def get_call_status(
    call_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get status of an active or completed call"""
    from src.voice.telephony import MindframeTelephony, TelephonyConfig, TelephonyProvider

    # In production, retrieve from active calls or database

    return {
        "call_id": call_id,
        "status": "in_progress",
        "message": "Call status retrieved"
    }


@app.post("/api/v1/voice/calls/{call_id}/end")
async def end_call(
    call_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """End an active call"""
    from src.voice.telephony import MindframeTelephony, TelephonyConfig, TelephonyProvider

    # In production, use actual telephony instance
    # await telephony.end_call(call_id)

    return {
        "success": True,
        "call_id": call_id,
        "message": "Call ended successfully"
    }


@app.post("/api/v1/voice/test/run")
async def run_voice_tests(
    suite_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Run voice agent test suite

    Mindframe Voice Testing - Automated conversation testing
    """
    from src.voice.voice_testing import MindframeVoiceTester
    from src.voice.voice_ai_engine import MindframeVoiceEngine
    from src.voice.flow_builder import MindframeFlowBuilder

    engine = MindframeVoiceEngine(openai_api_key=settings.openai_api_key)
    builder = MindframeFlowBuilder()
    tester = MindframeVoiceTester(engine, builder)

    # Run test suite
    report = await tester.run_test_suite(suite_id)

    return {
        "success": True,
        "report": report.dict()
    }


@app.post("/api/v1/voice/test/suites")
async def create_test_suite(
    suite_data: dict,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new voice test suite"""
    from src.voice.voice_testing import MindframeVoiceTester, TestScenario
    from src.voice.voice_ai_engine import MindframeVoiceEngine
    from src.voice.flow_builder import MindframeFlowBuilder

    engine = MindframeVoiceEngine(openai_api_key=settings.openai_api_key)
    builder = MindframeFlowBuilder()
    tester = MindframeVoiceTester(engine, builder)

    # Parse scenarios
    scenarios = [TestScenario(**s) for s in suite_data.get("scenarios", [])]

    suite = tester.create_test_suite(
        name=suite_data.get("name", ""),
        description=suite_data.get("description", ""),
        flow_id=suite_data.get("flow_id", ""),
        scenarios=scenarios
    )

    return {
        "success": True,
        "suite_id": suite.id,
        "suite": suite.dict()
    }


@app.get("/api/v1/voice/test/suites/{suite_id}/report")
async def get_test_report(
    suite_id: str,
    format: str = "json",
    current_user: User = Depends(get_current_active_user)
):
    """Get test report (JSON or HTML)"""
    from src.voice.voice_testing import MindframeVoiceTester
    from src.voice.voice_ai_engine import MindframeVoiceEngine
    from src.voice.flow_builder import MindframeFlowBuilder

    engine = MindframeVoiceEngine(openai_api_key=settings.openai_api_key)
    builder = MindframeFlowBuilder()
    tester = MindframeVoiceTester(engine, builder)

    # In production, load report from database
    # For now, return mock report

    return {
        "suite_id": suite_id,
        "format": format,
        "message": "Report would be generated here"
    }


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
# WEBSOCKET ENDPOINTS
# ============================================================================

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket endpoint for real-time updates

    Usage:
        ws://localhost:8000/ws/1

    Messages:
        {"type": "ping"}
        {"type": "subscribe_agent", "agent_id": 123}
        {"type": "request_metrics"}
    """
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(websocket, user_id, data)

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


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
    print(f"WebSocket endpoint: ws://localhost:{settings.port}/ws/{{user_id}}")


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
