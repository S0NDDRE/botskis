"""
AI Agent Tests
Test agent marketplace, activation, deactivation, execution
"""
import pytest
from fastapi.testclient import TestClient


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
def test_agent_registration():
    """Test registering a new agent"""
    from src.agents.agent_registry import AgentRegistry

    registry = AgentRegistry()

    agent_def = {
        "id": "test-agent",
        "name": "Test Agent",
        "description": "Test description",
        "category": "customer_support",
        "capabilities": ["chat", "email"],
        "price_tier": "basic"
    }

    registry.register_agent(**agent_def)

    assert "test-agent" in registry.agents
    assert registry.agents["test-agent"]["name"] == "Test Agent"


@pytest.mark.unit
def test_agent_execution():
    """Test agent execution logic"""
    from src.agents.base_agent import BaseAgent

    class TestAgent(BaseAgent):
        async def execute(self, input_data):
            return {"result": f"Processed: {input_data}"}

    agent = TestAgent(agent_id="test", name="Test")
    result = agent.execute({"message": "Hello"})

    assert "result" in result


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
def test_list_available_agents(client: TestClient, auth_headers):
    """Test listing all available agents"""
    response = client.get("/api/agents", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["agents"], list)
    assert len(data["agents"]) > 0

    # Check agent structure
    agent = data["agents"][0]
    assert "id" in agent
    assert "name" in agent
    assert "description" in agent
    assert "category" in agent


@pytest.mark.integration
def test_activate_agent(client: TestClient, auth_headers):
    """Test activating an agent for user"""
    response = client.post(
        "/api/agents/customer-support-basic/activate",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["agent"]["id"] == "customer-support-basic"
    assert data["agent"]["status"] == "active"


@pytest.mark.integration
def test_activate_nonexistent_agent(client: TestClient, auth_headers):
    """Test activating agent that doesn't exist"""
    response = client.post(
        "/api/agents/nonexistent-agent/activate",
        headers=auth_headers
    )

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False


@pytest.mark.integration
def test_deactivate_agent(client: TestClient, auth_headers):
    """Test deactivating an agent"""
    # First activate
    client.post(
        "/api/agents/customer-support-basic/activate",
        headers=auth_headers
    )

    # Then deactivate
    response = client.post(
        "/api/agents/customer-support-basic/deactivate",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["agent"]["status"] == "inactive"


@pytest.mark.integration
def test_get_my_agents(client: TestClient, auth_headers):
    """Test getting user's activated agents"""
    # Activate an agent first
    client.post(
        "/api/agents/customer-support-basic/activate",
        headers=auth_headers
    )

    # Get my agents
    response = client.get("/api/agents/my-agents", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["agents"], list)
    assert len(data["agents"]) > 0
    assert data["agents"][0]["id"] == "customer-support-basic"


@pytest.mark.integration
def test_agent_execution_endpoint(client: TestClient, auth_headers):
    """Test executing an agent via API"""
    # Activate agent
    client.post(
        "/api/agents/customer-support-basic/activate",
        headers=auth_headers
    )

    # Execute agent
    response = client.post(
        "/api/agents/customer-support-basic/execute",
        headers=auth_headers,
        json={
            "input": {
                "message": "I need help with my order",
                "context": {"order_id": "12345"}
            }
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "result" in data


@pytest.mark.integration
def test_agent_filtering_by_category(client: TestClient, auth_headers):
    """Test filtering agents by category"""
    response = client.get(
        "/api/agents?category=customer_support",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert all(
        agent["category"] == "customer_support"
        for agent in data["agents"]
    )


@pytest.mark.integration
def test_agent_filtering_by_price_tier(client: TestClient, auth_headers):
    """Test filtering agents by price tier"""
    response = client.get(
        "/api/agents?price_tier=basic",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert all(
        agent["price_tier"] == "basic"
        for agent in data["agents"]
    )


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
def test_complete_agent_lifecycle(client: TestClient, auth_headers):
    """Test complete agent lifecycle: browse → activate → use → deactivate"""

    # 1. Browse available agents
    browse_response = client.get("/api/agents", headers=auth_headers)
    assert browse_response.status_code == 200
    agents = browse_response.json()["agents"]
    assert len(agents) > 0

    # Pick first agent
    agent_id = agents[0]["id"]

    # 2. Activate agent
    activate_response = client.post(
        f"/api/agents/{agent_id}/activate",
        headers=auth_headers
    )
    assert activate_response.status_code == 200
    assert activate_response.json()["agent"]["status"] == "active"

    # 3. Execute agent
    execute_response = client.post(
        f"/api/agents/{agent_id}/execute",
        headers=auth_headers,
        json={"input": {"message": "Test execution"}}
    )
    assert execute_response.status_code == 200
    assert "result" in execute_response.json()

    # 4. Check my agents
    my_agents_response = client.get(
        "/api/agents/my-agents",
        headers=auth_headers
    )
    assert my_agents_response.status_code == 200
    my_agents = my_agents_response.json()["agents"]
    assert any(a["id"] == agent_id for a in my_agents)

    # 5. Deactivate agent
    deactivate_response = client.post(
        f"/api/agents/{agent_id}/deactivate",
        headers=auth_headers
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["agent"]["status"] == "inactive"

    # 6. Verify removed from my agents
    final_response = client.get(
        "/api/agents/my-agents",
        headers=auth_headers
    )
    assert final_response.status_code == 200
    final_agents = final_response.json()["agents"]
    assert not any(a["id"] == agent_id and a["status"] == "active" for a in final_agents)


@pytest.mark.e2e
def test_multiple_agents_activation(client: TestClient, auth_headers):
    """Test activating multiple agents simultaneously"""

    # Get available agents
    response = client.get("/api/agents", headers=auth_headers)
    agents = response.json()["agents"][:3]  # Take first 3

    # Activate all 3
    for agent in agents:
        activate_response = client.post(
            f"/api/agents/{agent['id']}/activate",
            headers=auth_headers
        )
        assert activate_response.status_code == 200

    # Verify all are in my agents
    my_agents_response = client.get(
        "/api/agents/my-agents",
        headers=auth_headers
    )
    my_agents = my_agents_response.json()["agents"]

    activated_ids = {a["id"] for a in agents}
    my_agent_ids = {a["id"] for a in my_agents}

    assert activated_ids.issubset(my_agent_ids)
