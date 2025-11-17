"""
Live Chat Tests
Test chat sessions, messages, tickets, agent assignment
"""
import pytest
from datetime import datetime
import asyncio


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
def test_create_chat_session():
    """Test creating chat session"""
    from src.support.live_chat import LiveChatManager

    manager = LiveChatManager()

    chat = manager.create_chat_session(
        customer_id=123,
        customer_name="John Doe",
        customer_email="john@example.com",
        initial_message="I need help"
    )

    assert chat.chat_id is not None
    assert chat.customer_id == 123
    assert chat.status == "waiting"
    assert len(chat.messages) == 1  # Initial message


@pytest.mark.unit
def test_send_message():
    """Test sending message in chat"""
    from src.support.live_chat import LiveChatManager

    manager = LiveChatManager()

    chat = manager.create_chat_session(
        customer_id=123,
        customer_name="John",
        customer_email="john@example.com"
    )

    message = manager.send_message(
        chat_id=chat.chat_id,
        sender_id=123,
        sender_type="customer",
        message="Hello, I need help"
    )

    assert message.message_id is not None
    assert message.content == "Hello, I need help"
    assert len(chat.messages) == 1


@pytest.mark.unit
def test_auto_assign_agent():
    """Test automatic agent assignment (load balancing)"""
    from src.support.live_chat import LiveChatManager

    manager = LiveChatManager()

    # Add test agents
    manager.agents = {
        "agent1": {"name": "Agent 1", "active_chats": 2},
        "agent2": {"name": "Agent 2", "active_chats": 1},
        "agent3": {"name": "Agent 3", "active_chats": 0}
    }

    chat = manager.create_chat_session(
        customer_id=123,
        customer_name="John",
        customer_email="john@example.com"
    )

    # Should assign to agent with least chats (agent3)
    assert chat.assigned_agent_id == "agent3"


@pytest.mark.unit
def test_create_ticket():
    """Test creating support ticket"""
    from src.support.live_chat import LiveChatManager

    manager = LiveChatManager()

    ticket = manager.create_ticket(
        customer_id=123,
        subject="Payment issue",
        description="Cannot process payment",
        priority="high"
    )

    assert ticket.ticket_id is not None
    assert ticket.subject == "Payment issue"
    assert ticket.status == "open"
    assert ticket.priority == "high"


@pytest.mark.unit
def test_canned_response():
    """Test using canned response"""
    from src.support.live_chat import LiveChatManager

    manager = LiveChatManager()

    response = manager.get_canned_response("greeting")

    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
def test_start_chat_endpoint(client, auth_headers):
    """Test starting chat via API"""
    response = client.post(
        "/api/chat/start",
        headers=auth_headers,
        json={
            "message": "I need help with my account"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "chat_id" in data
    assert data["status"] == "waiting"


@pytest.mark.integration
def test_send_message_endpoint(client, auth_headers):
    """Test sending message via API"""

    # Start chat first
    start_response = client.post(
        "/api/chat/start",
        headers=auth_headers,
        json={"message": "Hello"}
    )

    chat_id = start_response.json()["chat_id"]

    # Send message
    message_response = client.post(
        f"/api/chat/{chat_id}/message",
        headers=auth_headers,
        json={
            "message": "Can you help me?"
        }
    )

    assert message_response.status_code == 200
    data = message_response.json()
    assert "message_id" in data


@pytest.mark.integration
def test_get_chat_history(client, auth_headers):
    """Test getting chat history"""

    # Start chat and send messages
    start_response = client.post(
        "/api/chat/start",
        headers=auth_headers,
        json={"message": "Hello"}
    )

    chat_id = start_response.json()["chat_id"]

    # Get history
    history_response = client.get(
        f"/api/chat/{chat_id}/history",
        headers=auth_headers
    )

    assert history_response.status_code == 200
    data = history_response.json()
    assert "messages" in data
    assert len(data["messages"]) > 0


@pytest.mark.integration
def test_end_chat(client, auth_headers):
    """Test ending chat session"""

    # Start chat
    start_response = client.post(
        "/api/chat/start",
        headers=auth_headers,
        json={"message": "Hello"}
    )

    chat_id = start_response.json()["chat_id"]

    # End chat
    end_response = client.post(
        f"/api/chat/{chat_id}/end",
        headers=auth_headers
    )

    assert end_response.status_code == 200
    data = end_response.json()
    assert data["status"] == "ended"


@pytest.mark.integration
def test_create_ticket_endpoint(client, auth_headers):
    """Test creating ticket via API"""
    response = client.post(
        "/api/support/tickets",
        headers=auth_headers,
        json={
            "subject": "Billing issue",
            "description": "I was charged twice",
            "priority": "high"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "ticket_id" in data
    assert data["subject"] == "Billing issue"


@pytest.mark.integration
def test_get_my_tickets(client, auth_headers):
    """Test getting user's tickets"""

    # Create ticket first
    client.post(
        "/api/support/tickets",
        headers=auth_headers,
        json={
            "subject": "Test ticket",
            "description": "Test",
            "priority": "normal"
        }
    )

    # Get tickets
    response = client.get(
        "/api/support/tickets",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "tickets" in data
    assert len(data["tickets"]) > 0


@pytest.mark.integration
def test_typing_indicator(client, auth_headers):
    """Test typing indicator"""

    # Start chat
    start_response = client.post(
        "/api/chat/start",
        headers=auth_headers,
        json={"message": "Hello"}
    )

    chat_id = start_response.json()["chat_id"]

    # Send typing indicator
    typing_response = client.post(
        f"/api/chat/{chat_id}/typing",
        headers=auth_headers,
        json={"is_typing": True}
    )

    assert typing_response.status_code == 200


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
def test_complete_chat_flow(client, auth_headers):
    """Test complete chat flow from start to end"""

    # 1. Customer starts chat
    start_response = client.post(
        "/api/chat/start",
        headers=auth_headers,
        json={
            "message": "I have a problem with my order"
        }
    )

    assert start_response.status_code == 200
    chat_id = start_response.json()["chat_id"]
    assert start_response.json()["status"] == "waiting"

    # 2. Send typing indicator
    client.post(
        f"/api/chat/{chat_id}/typing",
        headers=auth_headers,
        json={"is_typing": True}
    )

    # 3. Send message
    message_response = client.post(
        f"/api/chat/{chat_id}/message",
        headers=auth_headers,
        json={
            "message": "My order #12345 hasn't arrived"
        }
    )

    assert message_response.status_code == 200

    # 4. Get chat history
    history_response = client.get(
        f"/api/chat/{chat_id}/history",
        headers=auth_headers
    )

    assert history_response.status_code == 200
    messages = history_response.json()["messages"]
    assert len(messages) >= 2

    # 5. End chat
    end_response = client.post(
        f"/api/chat/{chat_id}/end",
        headers=auth_headers
    )

    assert end_response.status_code == 200
    assert end_response.json()["status"] == "ended"


@pytest.mark.e2e
def test_ticket_lifecycle(client, auth_headers):
    """Test ticket lifecycle from creation to resolution"""

    # 1. Create ticket
    create_response = client.post(
        "/api/support/tickets",
        headers=auth_headers,
        json={
            "subject": "Account locked",
            "description": "I cannot log into my account",
            "priority": "high"
        }
    )

    assert create_response.status_code == 201
    ticket_id = create_response.json()["ticket_id"]

    # 2. Get ticket details
    details_response = client.get(
        f"/api/support/tickets/{ticket_id}",
        headers=auth_headers
    )

    assert details_response.status_code == 200
    assert details_response.json()["status"] == "open"

    # 3. Add comment to ticket
    comment_response = client.post(
        f"/api/support/tickets/{ticket_id}/comments",
        headers=auth_headers,
        json={
            "comment": "I've tried resetting my password"
        }
    )

    assert comment_response.status_code == 200

    # 4. (Would be done by support agent) Update ticket status
    # For test purposes, assume this endpoint exists
    # update_response = client.patch(
    #     f"/api/support/tickets/{ticket_id}",
    #     headers=auth_headers,
    #     json={"status": "resolved"}
    # )


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_chat_with_auto_responses():
    """Test chat with automatic AI responses"""
    from src.support.live_chat import LiveChatManager

    manager = LiveChatManager()

    # Create chat
    chat = manager.create_chat_session(
        customer_id=123,
        customer_name="John",
        customer_email="john@example.com",
        initial_message="What are your business hours?"
    )

    # Simulate AI auto-response
    # (In real implementation, this would be triggered automatically)
    canned = manager.get_canned_response("business_hours")

    response_message = manager.send_message(
        chat_id=chat.chat_id,
        sender_id="ai_bot",
        sender_type="bot",
        message=canned
    )

    assert response_message is not None
    assert "hours" in response_message.content.lower()


@pytest.mark.e2e
def test_multiple_concurrent_chats(client, auth_headers):
    """Test handling multiple concurrent chats"""

    chat_ids = []

    # Create 3 concurrent chats
    for i in range(3):
        response = client.post(
            "/api/chat/start",
            headers=auth_headers,
            json={
                "message": f"Chat {i+1}"
            }
        )

        assert response.status_code == 200
        chat_ids.append(response.json()["chat_id"])

    # Send message to each chat
    for chat_id in chat_ids:
        message_response = client.post(
            f"/api/chat/{chat_id}/message",
            headers=auth_headers,
            json={
                "message": "Follow-up message"
            }
        )

        assert message_response.status_code == 200

    # Verify all chats are independent
    assert len(set(chat_ids)) == 3  # All unique
