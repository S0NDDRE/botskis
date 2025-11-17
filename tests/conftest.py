"""
Pytest Configuration
Shared fixtures and setup for all tests
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
import os

# Set test environment
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/mindframe_test"


# ============================================================================
# EVENT LOOP FIXTURE
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
async def db():
    """Database session for tests (rolled back after each test)"""
    from src.database import get_db, engine
    from sqlalchemy.orm import sessionmaker

    # Create test database tables
    # Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


# ============================================================================
# APP FIXTURES
# ============================================================================

@pytest.fixture(scope="module")
def app():
    """FastAPI application"""
    from src.main import app
    return app


@pytest.fixture(scope="module")
def client(app) -> Generator:
    """Test client"""
    with TestClient(app) as c:
        yield c


# ============================================================================
# AUTH FIXTURES
# ============================================================================

@pytest.fixture
def test_user():
    """Test user data"""
    return {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User",
        "is_admin": False
    }


@pytest.fixture
def admin_user():
    """Admin user data"""
    return {
        "id": 999,
        "email": "admin@mindframe.no",
        "name": "Admin User",
        "is_admin": True
    }


@pytest.fixture
def auth_token(test_user):
    """Generate auth token for test user"""
    from src.auth.jwt import create_access_token
    return create_access_token(test_user["id"])


@pytest.fixture
def admin_token(admin_user):
    """Generate auth token for admin user"""
    from src.auth.jwt import create_access_token
    return create_access_token(admin_user["id"])


@pytest.fixture
def auth_headers(auth_token):
    """Auth headers for requests"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def admin_headers(admin_token):
    """Admin auth headers"""
    return {"Authorization": f"Bearer {admin_token}"}


# ============================================================================
# DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_agent():
    """Sample AI agent"""
    return {
        "id": "customer_support_bot",
        "name": "24/7 Customer Support Bot",
        "category": "support",
        "price": 29,
        "features": ["24/7 availability", "Multi-language", "Auto-learning"]
    }


@pytest.fixture
def sample_subscription():
    """Sample subscription"""
    return {
        "id": 1,
        "user_id": 1,
        "plan": "professional",
        "status": "active",
        "amount": 149.00,
        "currency": "EUR"
    }


# ============================================================================
# CLEANUP FIXTURES
# ============================================================================

@pytest.fixture(autouse=True)
async def cleanup():
    """Cleanup after each test"""
    yield
    # Cleanup code here (clear caches, reset singletons, etc.)


# ============================================================================
# MOCK FIXTURES
# ============================================================================

@pytest.fixture
def mock_stripe_payment():
    """Mock Stripe payment"""
    class MockPaymentIntent:
        def __init__(self):
            self.id = "pi_test_123"
            self.status = "succeeded"
            self.amount = 14900  # cents
            self.currency = "eur"

    return MockPaymentIntent()


@pytest.fixture
def mock_vipps_payment():
    """Mock Vipps payment"""
    return {
        "orderId": "order_test_123",
        "status": "RESERVED",
        "amount": 14900,  # øre
        "currency": "NOK"
    }


# ============================================================================
# PARAMETRIZE HELPERS
# ============================================================================

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow tests"
    )
