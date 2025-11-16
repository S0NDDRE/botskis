"""
R-Learning Engine Tests
Test Q-Learning, experience replay, agent improvement
"""
import pytest
from datetime import datetime
import asyncio


# ============================================================================
# UNIT TESTS
# ============================================================================

@pytest.mark.unit
def test_q_learning_agent_initialization():
    """Test Q-Learning agent initialization"""
    from src.ai.r_learning_engine import QLearningAgent

    agent = QLearningAgent(
        agent_id="test_agent",
        learning_rate=0.1,
        discount_factor=0.95,
        epsilon=0.1
    )

    assert agent.agent_id == "test_agent"
    assert agent.learning_rate == 0.1
    assert agent.discount_factor == 0.95
    assert len(agent.q_table) == 0


@pytest.mark.unit
def test_choose_action_exploration():
    """Test action selection with exploration"""
    from src.ai.r_learning_engine import QLearningAgent

    agent = QLearningAgent(
        agent_id="test",
        epsilon=1.0  # Always explore
    )

    state = {"context": "greeting"}
    available_actions = ["action_a", "action_b", "action_c"]

    action = agent.choose_action(state, available_actions)

    # Should choose random action (exploration)
    assert action in available_actions


@pytest.mark.unit
def test_choose_action_exploitation():
    """Test action selection with exploitation"""
    from src.ai.r_learning_engine import QLearningAgent

    agent = QLearningAgent(
        agent_id="test",
        epsilon=0.0  # Never explore, always exploit
    )

    state = {"context": "greeting"}
    available_actions = ["good_action", "bad_action"]

    # Manually set Q-values
    state_key = agent._state_to_key(state)
    agent.q_table[state_key] = {
        "good_action": 10.0,
        "bad_action": 1.0
    }

    action = agent.choose_action(state, available_actions)

    # Should choose best action
    assert action == "good_action"


@pytest.mark.unit
def test_q_value_update():
    """Test Q-value update using Bellman equation"""
    from src.ai.r_learning_engine import QLearningAgent, Reward

    agent = QLearningAgent(
        agent_id="test",
        learning_rate=0.1,
        discount_factor=0.9
    )

    state = {"context": "test"}
    action = "action_a"
    reward = Reward(reward_value=10.0, reason="success")
    next_state = {"context": "next"}

    # Update Q-value
    agent.update(state, action, reward, next_state, done=False)

    # Q-value should be updated
    state_key = agent._state_to_key(state)
    assert state_key in agent.q_table
    assert "action_a" in agent.q_table[state_key]
    assert agent.q_table[state_key]["action_a"] > 0


@pytest.mark.unit
def test_experience_replay():
    """Test experience replay buffer"""
    from src.ai.r_learning_engine import ExperienceReplayBuffer, Experience

    buffer = ExperienceReplayBuffer(max_size=100)

    # Add experiences
    for i in range(10):
        experience = Experience(
            state={"step": i},
            action=f"action_{i}",
            reward=float(i),
            next_state={"step": i + 1},
            done=False,
            timestamp=datetime.now()
        )
        buffer.add(experience)

    assert len(buffer.buffer) == 10

    # Sample experiences
    batch = buffer.sample(batch_size=5)
    assert len(batch) == 5


@pytest.mark.unit
def test_reward_calculation():
    """Test reward calculation"""
    from src.ai.r_learning_engine import calculate_reward

    # Positive outcomes
    positive_reward = calculate_reward(
        outcome="success",
        user_satisfaction=0.9,
        task_completion_time=5.0
    )
    assert positive_reward.reward_value > 0

    # Negative outcomes
    negative_reward = calculate_reward(
        outcome="failure",
        user_satisfaction=0.2,
        task_completion_time=60.0
    )
    assert negative_reward.reward_value < 0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_training_loop():
    """Test agent training over multiple episodes"""
    from src.ai.r_learning_engine import QLearningAgent, Reward

    agent = QLearningAgent(
        agent_id="training_test",
        learning_rate=0.1,
        discount_factor=0.95,
        epsilon=0.2
    )

    # Simulate 100 training episodes
    for episode in range(100):
        state = {"episode": episode, "context": "training"}
        action = agent.choose_action(state, ["action_a", "action_b"])

        # Simulate outcome
        if action == "action_a":
            reward = Reward(reward_value=10.0, reason="good choice")
        else:
            reward = Reward(reward_value=-5.0, reason="bad choice")

        next_state = {"episode": episode + 1, "context": "training"}

        agent.update(state, action, reward, next_state, done=True)

    # After training, agent should prefer action_a
    test_state = {"episode": 101, "context": "training"}

    # Test multiple times to account for epsilon-greedy
    action_counts = {"action_a": 0, "action_b": 0}
    for _ in range(100):
        action = agent.choose_action(test_state, ["action_a", "action_b"])
        action_counts[action] += 1

    # Should choose action_a more often
    assert action_counts["action_a"] > action_counts["action_b"]


@pytest.mark.integration
@pytest.mark.asyncio
async def test_r_learning_engine_integration():
    """Test R-Learning engine integration with agent manager"""
    from src.ai.r_learning_engine import RLearningEngine

    engine = RLearningEngine()

    # Register agent
    agent_id = await engine.register_agent(
        agent_id="customer_support_bot",
        agent_type="support"
    )

    assert agent_id == "customer_support_bot"
    assert agent_id in engine.agents

    # Track interaction
    await engine.track_interaction(
        agent_id=agent_id,
        state={"user_query": "How do I reset password?"},
        action="provide_reset_link",
        outcome="success",
        user_satisfaction=0.95
    )

    # Get agent performance
    performance = await engine.get_agent_performance(agent_id)

    assert performance["total_interactions"] == 1
    assert performance["success_rate"] >= 0


@pytest.mark.integration
def test_get_learning_metrics(client, auth_headers):
    """Test getting R-Learning metrics via API"""
    response = client.get(
        "/api/ai/r-learning/metrics",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()

    assert "total_agents" in data
    assert "total_interactions" in data
    assert "average_improvement" in data


@pytest.mark.integration
def test_get_agent_performance(client, auth_headers):
    """Test getting specific agent performance"""
    response = client.get(
        "/api/ai/r-learning/agents/customer_support_bot/performance",
        headers=auth_headers
    )

    # Will be 404 if agent doesn't exist, 200 if found
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "success_rate" in data
        assert "total_interactions" in data


# ============================================================================
# E2E TESTS
# ============================================================================

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_complete_learning_cycle():
    """Test complete learning cycle: register → train → improve → validate"""
    from src.ai.r_learning_engine import RLearningEngine, Reward

    engine = RLearningEngine()

    # 1. Register agent
    agent_id = "email_responder"
    await engine.register_agent(agent_id, agent_type="email")

    # 2. Initial performance (should be poor)
    initial_perf = await engine.get_agent_performance(agent_id)
    initial_success = initial_perf.get("success_rate", 0)

    # 3. Training phase - 1000 interactions
    for i in range(1000):
        state = {"email_type": "inquiry", "urgency": "normal"}

        # Get action from agent
        agent = engine.agents[agent_id]
        action = agent.choose_action(
            state,
            ["template_a", "template_b", "template_c"]
        )

        # Simulate outcome (template_b is best)
        if action == "template_b":
            reward = Reward(reward_value=10.0, reason="best template")
            outcome = "success"
            satisfaction = 0.95
        elif action == "template_a":
            reward = Reward(reward_value=5.0, reason="okay template")
            outcome = "success"
            satisfaction = 0.7
        else:
            reward = Reward(reward_value=-2.0, reason="poor template")
            outcome = "failure"
            satisfaction = 0.3

        # Track interaction
        await engine.track_interaction(
            agent_id=agent_id,
            state=state,
            action=action,
            outcome=outcome,
            user_satisfaction=satisfaction
        )

    # 4. Validate improvement
    final_perf = await engine.get_agent_performance(agent_id)
    final_success = final_perf["success_rate"]

    # Success rate should improve significantly
    assert final_success > initial_success
    # Should reach at least 70% success rate
    assert final_success >= 0.7

    # 5. Test learned behavior
    test_state = {"email_type": "inquiry", "urgency": "normal"}

    # Test 100 times
    action_counts = {
        "template_a": 0,
        "template_b": 0,
        "template_c": 0
    }

    for _ in range(100):
        action = agent.choose_action(
            test_state,
            ["template_a", "template_b", "template_c"]
        )
        action_counts[action] += 1

    # Should primarily choose template_b (the best one)
    assert action_counts["template_b"] > action_counts["template_a"]
    assert action_counts["template_b"] > action_counts["template_c"]


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_multi_agent_learning():
    """Test multiple agents learning simultaneously"""
    from src.ai.r_learning_engine import RLearningEngine

    engine = RLearningEngine()

    # Register multiple agents
    agents = ["support_bot", "sales_bot", "onboarding_bot"]

    for agent_id in agents:
        await engine.register_agent(agent_id, agent_type="chat")

    # Train all agents
    for agent_id in agents:
        for i in range(100):
            await engine.track_interaction(
                agent_id=agent_id,
                state={"interaction": i},
                action="action_1",
                outcome="success",
                user_satisfaction=0.8
            )

    # All agents should have performance data
    for agent_id in agents:
        perf = await engine.get_agent_performance(agent_id)
        assert perf["total_interactions"] == 100


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_ab_testing_with_learning():
    """Test A/B testing different agent strategies"""
    from src.ai.r_learning_engine import RLearningEngine

    engine = RLearningEngine()

    # Create two versions of agent
    await engine.register_agent("agent_v1", agent_type="test")
    await engine.register_agent("agent_v2", agent_type="test")

    # Train with different strategies
    # V1: Learns from positive rewards only
    # V2: Learns from both positive and negative

    for i in range(500):
        # V1 training
        await engine.track_interaction(
            agent_id="agent_v1",
            state={"test": i},
            action="action",
            outcome="success",
            user_satisfaction=0.9
        )

        # V2 training (includes failures)
        outcome = "success" if i % 2 == 0 else "failure"
        satisfaction = 0.9 if outcome == "success" else 0.3

        await engine.track_interaction(
            agent_id="agent_v2",
            state={"test": i},
            action="action",
            outcome=outcome,
            user_satisfaction=satisfaction
        )

    # Compare performance
    v1_perf = await engine.get_agent_performance("agent_v1")
    v2_perf = await engine.get_agent_performance("agent_v2")

    # Both should have learned, but V2 might be more robust
    assert v1_perf["success_rate"] > 0
    assert v2_perf["success_rate"] > 0


@pytest.mark.e2e
def test_learning_dashboard(client, auth_headers):
    """Test R-Learning dashboard endpoints"""

    # 1. Get overview
    overview_response = client.get(
        "/api/ai/r-learning/overview",
        headers=auth_headers
    )
    assert overview_response.status_code == 200

    # 2. Get agent list
    agents_response = client.get(
        "/api/ai/r-learning/agents",
        headers=auth_headers
    )
    assert agents_response.status_code == 200

    # 3. Get improvement trends
    trends_response = client.get(
        "/api/ai/r-learning/trends?days=30",
        headers=auth_headers
    )
    assert trends_response.status_code == 200

    # 4. Get top performing agents
    top_response = client.get(
        "/api/ai/r-learning/top-performers?limit=10",
        headers=auth_headers
    )
    assert top_response.status_code == 200
