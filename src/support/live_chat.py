"""
Self-Hosted Live Chat & Support System
Replaces Intercom ($74/month)

Features:
- Real-time chat via WebSocket
- Support ticketing
- Canned responses
- Chat history
- Online/offline status
- Typing indicators
- File sharing
- Chat analytics

Savings: $74/month = $888/year
"""
from typing import Dict, List, Optional, Set
from pydantic import BaseModel
from datetime import datetime, timedelta
from enum import Enum
from loguru import logger
import uuid
import json


# ============================================================================
# ENUMS & MODELS
# ============================================================================

class ChatStatus(str, Enum):
    """Chat session status"""
    ACTIVE = "active"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"


class MessageType(str, Enum):
    """Message types"""
    TEXT = "text"
    FILE = "file"
    SYSTEM = "system"
    TYPING = "typing"


class TicketPriority(str, Enum):
    """Support ticket priority"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(str, Enum):
    """Support ticket status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ChatMessage(BaseModel):
    """Chat message"""
    message_id: str
    chat_id: str
    sender_id: int
    sender_name: str
    sender_type: str  # "customer" or "agent"
    message_type: MessageType
    content: str
    timestamp: datetime
    read: bool = False
    file_url: Optional[str] = None


class ChatSession(BaseModel):
    """Chat session"""
    chat_id: str
    customer_id: int
    customer_name: str
    customer_email: str
    agent_id: Optional[int] = None
    agent_name: Optional[str] = None
    status: ChatStatus
    created_at: datetime
    last_message_at: datetime
    messages: List[ChatMessage] = []
    tags: List[str] = []
    customer_online: bool = False
    agent_online: bool = False


class SupportTicket(BaseModel):
    """Support ticket"""
    ticket_id: str
    customer_id: int
    customer_name: str
    customer_email: str
    subject: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    assigned_to: Optional[int] = None
    assigned_to_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    tags: List[str] = []
    chat_id: Optional[str] = None


class CannedResponse(BaseModel):
    """Pre-written response template"""
    response_id: str
    title: str
    content: str
    category: str
    shortcut: str  # e.g., "/greeting", "/hours"
    usage_count: int = 0


class AgentPresence(BaseModel):
    """Agent online/offline status"""
    agent_id: int
    agent_name: str
    online: bool
    last_seen: datetime
    active_chats: int = 0


# ============================================================================
# LIVE CHAT MANAGER
# ============================================================================

class LiveChatManager:
    """
    Self-Hosted Live Chat & Support System

    Features:
    - Real-time WebSocket chat
    - Support ticketing
    - Canned responses
    - Chat routing to available agents
    - Typing indicators
    - File sharing
    - Chat history & analytics

    Replaces: Intercom ($74/month)
    Cost: $0
    Savings: $888/year
    """

    def __init__(self):
        # Active chat sessions
        self.chats: Dict[str, ChatSession] = {}

        # Support tickets
        self.tickets: Dict[str, SupportTicket] = {}

        # Canned responses
        self.canned_responses: Dict[str, CannedResponse] = {}

        # WebSocket connections
        self.connections: Dict[str, any] = {}  # chat_id -> websocket

        # Agent presence
        self.agents: Dict[int, AgentPresence] = {}

        # Typing indicators
        self.typing: Dict[str, Set[int]] = {}  # chat_id -> set of user_ids

        # Load default canned responses
        self._load_default_canned_responses()

    # ========================================================================
    # CHAT MANAGEMENT
    # ========================================================================

    def create_chat_session(
        self,
        customer_id: int,
        customer_name: str,
        customer_email: str,
        initial_message: Optional[str] = None
    ) -> ChatSession:
        """
        Create new chat session

        Args:
            customer_id: Customer user ID
            customer_name: Customer name
            customer_email: Customer email
            initial_message: Optional first message

        Returns:
            Created chat session

        Example:
        ```python
        chat = chat_manager.create_chat_session(
            customer_id=123,
            customer_name="John Doe",
            customer_email="john@example.com",
            initial_message="Hi, I need help with payment"
        )
        ```
        """
        chat_id = str(uuid.uuid4())
        now = datetime.now()

        chat = ChatSession(
            chat_id=chat_id,
            customer_id=customer_id,
            customer_name=customer_name,
            customer_email=customer_email,
            status=ChatStatus.WAITING,
            created_at=now,
            last_message_at=now,
            customer_online=True
        )

        # Add initial message
        if initial_message:
            message = ChatMessage(
                message_id=str(uuid.uuid4()),
                chat_id=chat_id,
                sender_id=customer_id,
                sender_name=customer_name,
                sender_type="customer",
                message_type=MessageType.TEXT,
                content=initial_message,
                timestamp=now
            )
            chat.messages.append(message)

        self.chats[chat_id] = chat

        # Auto-assign to available agent
        self._auto_assign_agent(chat)

        logger.info(f"📱 New chat session created: {chat_id} - {customer_name}")
        return chat

    def _auto_assign_agent(self, chat: ChatSession):
        """Auto-assign chat to available agent (lowest workload)"""
        # Get online agents
        online_agents = [a for a in self.agents.values() if a.online]

        if not online_agents:
            logger.warning("No agents available for assignment")
            return

        # Find agent with fewest active chats
        agent = min(online_agents, key=lambda a: a.active_chats)

        # Assign
        chat.agent_id = agent.agent_id
        chat.agent_name = agent.agent_name
        chat.status = ChatStatus.ACTIVE
        agent.active_chats += 1

        # Send system message
        self.add_message(
            chat_id=chat.chat_id,
            sender_id=0,
            sender_name="System",
            sender_type="system",
            message_type=MessageType.SYSTEM,
            content=f"{agent.agent_name} has joined the chat"
        )

        logger.info(f"✅ Chat {chat.chat_id} assigned to agent {agent.agent_name}")

    def add_message(
        self,
        chat_id: str,
        sender_id: int,
        sender_name: str,
        sender_type: str,
        message_type: MessageType,
        content: str,
        file_url: Optional[str] = None
    ) -> ChatMessage:
        """
        Add message to chat

        Automatically broadcasts to WebSocket connections
        """
        if chat_id not in self.chats:
            raise ValueError(f"Chat {chat_id} not found")

        chat = self.chats[chat_id]

        message = ChatMessage(
            message_id=str(uuid.uuid4()),
            chat_id=chat_id,
            sender_id=sender_id,
            sender_name=sender_name,
            sender_type=sender_type,
            message_type=message_type,
            content=content,
            timestamp=datetime.now(),
            file_url=file_url
        )

        chat.messages.append(message)
        chat.last_message_at = datetime.now()

        # Broadcast to WebSocket connections
        self._broadcast_message(chat_id, message)

        logger.info(f"💬 Message added to chat {chat_id}: {content[:50]}")
        return message

    async def _broadcast_message(self, chat_id: str, message: ChatMessage):
        """Broadcast message to WebSocket connections"""
        if chat_id in self.connections:
            try:
                websocket = self.connections[chat_id]
                await websocket.send_json({
                    "type": "message",
                    "data": message.dict()
                })
            except Exception as e:
                logger.error(f"Failed to broadcast message: {e}")

    # ========================================================================
    # TYPING INDICATORS
    # ========================================================================

    async def set_typing(self, chat_id: str, user_id: int, typing: bool):
        """
        Set typing indicator

        Args:
            chat_id: Chat session ID
            user_id: User who is typing
            typing: True if typing, False if stopped

        Broadcasts typing status to other participants
        """
        if chat_id not in self.typing:
            self.typing[chat_id] = set()

        if typing:
            self.typing[chat_id].add(user_id)
        else:
            self.typing[chat_id].discard(user_id)

        # Broadcast typing indicator
        if chat_id in self.connections:
            try:
                websocket = self.connections[chat_id]
                await websocket.send_json({
                    "type": "typing",
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "typing": typing
                })
            except Exception as e:
                logger.error(f"Failed to broadcast typing indicator: {e}")

    def get_typing_users(self, chat_id: str) -> List[int]:
        """Get users currently typing in chat"""
        return list(self.typing.get(chat_id, set()))

    # ========================================================================
    # SUPPORT TICKETS
    # ========================================================================

    def create_ticket(
        self,
        customer_id: int,
        customer_name: str,
        customer_email: str,
        subject: str,
        description: str,
        priority: TicketPriority = TicketPriority.NORMAL,
        chat_id: Optional[str] = None
    ) -> SupportTicket:
        """
        Create support ticket

        Can be created from chat session or standalone

        Example:
        ```python
        ticket = chat_manager.create_ticket(
            customer_id=123,
            customer_name="John Doe",
            customer_email="john@example.com",
            subject="Payment issue",
            description="Cannot complete payment",
            priority=TicketPriority.HIGH
        )
        ```
        """
        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now()

        ticket = SupportTicket(
            ticket_id=ticket_id,
            customer_id=customer_id,
            customer_name=customer_name,
            customer_email=customer_email,
            subject=subject,
            description=description,
            priority=priority,
            status=TicketStatus.OPEN,
            created_at=now,
            updated_at=now,
            chat_id=chat_id
        )

        self.tickets[ticket_id] = ticket

        logger.info(f"🎫 Support ticket created: {ticket_id} - {subject}")
        return ticket

    def assign_ticket(self, ticket_id: str, agent_id: int, agent_name: str):
        """Assign ticket to agent"""
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")

        ticket = self.tickets[ticket_id]
        ticket.assigned_to = agent_id
        ticket.assigned_to_name = agent_name
        ticket.status = TicketStatus.IN_PROGRESS
        ticket.updated_at = datetime.now()

        logger.info(f"✅ Ticket {ticket_id} assigned to {agent_name}")

    def resolve_ticket(self, ticket_id: str):
        """Mark ticket as resolved"""
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")

        ticket = self.tickets[ticket_id]
        ticket.status = TicketStatus.RESOLVED
        ticket.resolved_at = datetime.now()
        ticket.updated_at = datetime.now()

        logger.info(f"✅ Ticket {ticket_id} resolved")

    # ========================================================================
    # CANNED RESPONSES
    # ========================================================================

    def _load_default_canned_responses(self):
        """Load default canned responses"""
        defaults = [
            CannedResponse(
                response_id="greeting",
                title="Greeting",
                content="Hi! Thanks for reaching out. How can I help you today?",
                category="General",
                shortcut="/greeting"
            ),
            CannedResponse(
                response_id="hours",
                title="Business Hours",
                content="Our support hours are Monday-Friday 9:00-17:00 CET. We'll respond to your message as soon as possible!",
                category="General",
                shortcut="/hours"
            ),
            CannedResponse(
                response_id="payment_issue",
                title="Payment Issue",
                content="I understand you're having payment issues. Can you please provide more details about the error message you're seeing?",
                category="Payment",
                shortcut="/payment"
            ),
            CannedResponse(
                response_id="account_help",
                title="Account Help",
                content="I'd be happy to help with your account. For security purposes, can you please verify your email address?",
                category="Account",
                shortcut="/account"
            ),
            CannedResponse(
                response_id="closing",
                title="Closing",
                content="Is there anything else I can help you with today?",
                category="General",
                shortcut="/closing"
            ),
            CannedResponse(
                response_id="resolved",
                title="Issue Resolved",
                content="Great! I'm glad we could resolve this. Feel free to reach out if you need anything else!",
                category="General",
                shortcut="/resolved"
            )
        ]

        for response in defaults:
            self.canned_responses[response.response_id] = response

    def get_canned_response(self, shortcut: str) -> Optional[str]:
        """
        Get canned response by shortcut

        Args:
            shortcut: Shortcut code (e.g., "/greeting")

        Returns:
            Response content or None if not found
        """
        for response in self.canned_responses.values():
            if response.shortcut == shortcut:
                response.usage_count += 1
                return response.content
        return None

    def add_canned_response(
        self,
        title: str,
        content: str,
        category: str,
        shortcut: str
    ) -> CannedResponse:
        """Add new canned response"""
        response_id = str(uuid.uuid4())

        response = CannedResponse(
            response_id=response_id,
            title=title,
            content=content,
            category=category,
            shortcut=shortcut
        )

        self.canned_responses[response_id] = response
        return response

    # ========================================================================
    # AGENT PRESENCE
    # ========================================================================

    def set_agent_online(self, agent_id: int, agent_name: str):
        """Mark agent as online"""
        if agent_id not in self.agents:
            self.agents[agent_id] = AgentPresence(
                agent_id=agent_id,
                agent_name=agent_name,
                online=True,
                last_seen=datetime.now()
            )
        else:
            self.agents[agent_id].online = True
            self.agents[agent_id].last_seen = datetime.now()

        logger.info(f"✅ Agent {agent_name} is now online")

    def set_agent_offline(self, agent_id: int):
        """Mark agent as offline"""
        if agent_id in self.agents:
            self.agents[agent_id].online = False
            self.agents[agent_id].last_seen = datetime.now()
            logger.info(f"⏸️  Agent {self.agents[agent_id].agent_name} is now offline")

    def get_online_agents(self) -> List[AgentPresence]:
        """Get list of online agents"""
        return [a for a in self.agents.values() if a.online]

    # ========================================================================
    # ANALYTICS
    # ========================================================================

    def get_chat_stats(self, time_range: Optional[timedelta] = None) -> Dict:
        """
        Get chat statistics

        Returns:
        - Total chats
        - Active chats
        - Average response time
        - Resolution rate
        - By status breakdown
        """
        chats_list = list(self.chats.values())

        # Filter by time range
        if time_range:
            cutoff = datetime.now() - time_range
            chats_list = [c for c in chats_list if c.created_at >= cutoff]

        # Calculate stats
        total_chats = len(chats_list)
        active_chats = len([c for c in chats_list if c.status == ChatStatus.ACTIVE])
        resolved_chats = len([c for c in chats_list if c.status == ChatStatus.RESOLVED])

        # Calculate average response time (first agent message after customer message)
        response_times = []
        for chat in chats_list:
            customer_msg = None
            for msg in chat.messages:
                if msg.sender_type == "customer" and not customer_msg:
                    customer_msg = msg
                elif msg.sender_type == "agent" and customer_msg:
                    response_time = (msg.timestamp - customer_msg.timestamp).total_seconds()
                    response_times.append(response_time)
                    break

        avg_response_time = (
            sum(response_times) / len(response_times)
            if response_times else 0
        )

        return {
            "total_chats": total_chats,
            "active_chats": active_chats,
            "waiting_chats": len([c for c in chats_list if c.status == ChatStatus.WAITING]),
            "resolved_chats": resolved_chats,
            "avg_response_time_seconds": avg_response_time,
            "resolution_rate": (
                (resolved_chats / total_chats * 100)
                if total_chats > 0 else 0
            ),
            "online_agents": len(self.get_online_agents())
        }

    def get_ticket_stats(self, time_range: Optional[timedelta] = None) -> Dict:
        """Get support ticket statistics"""
        tickets_list = list(self.tickets.values())

        if time_range:
            cutoff = datetime.now() - time_range
            tickets_list = [t for t in tickets_list if t.created_at >= cutoff]

        return {
            "total_tickets": len(tickets_list),
            "open_tickets": len([t for t in tickets_list if t.status == TicketStatus.OPEN]),
            "in_progress": len([t for t in tickets_list if t.status == TicketStatus.IN_PROGRESS]),
            "resolved_tickets": len([t for t in tickets_list if t.status == TicketStatus.RESOLVED]),
            "by_priority": {
                "urgent": len([t for t in tickets_list if t.priority == TicketPriority.URGENT]),
                "high": len([t for t in tickets_list if t.priority == TicketPriority.HIGH]),
                "normal": len([t for t in tickets_list if t.priority == TicketPriority.NORMAL]),
                "low": len([t for t in tickets_list if t.priority == TicketPriority.LOW])
            }
        }


# ============================================================================
# GLOBAL INSTANCE
# ============================================================================

# Singleton instance
chat_manager = LiveChatManager()


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'LiveChatManager',
    'ChatSession',
    'ChatMessage',
    'SupportTicket',
    'CannedResponse',
    'AgentPresence',
    'ChatStatus',
    'MessageType',
    'TicketPriority',
    'TicketStatus',
    'chat_manager'
]
