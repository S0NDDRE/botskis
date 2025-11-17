# 🏗️ BYGGE VÅRT EGET AV ALT
## Selvstendighet & Uavhengighet - Roadmap

**Mål:** Maksimere hva vi eier og kontrollerer selv
**Filosofi:** Bygg alt du kan, kjøp bare det du MÅ

---

## 📋 KATEGORISERING

### ✅ Kategori 1: KAN IKKE BYGGE SELV (MÅ KJØPE)
Disse krever lisenser, sertifiseringer, eller massive infrastruktur:

1. **Payment Processing (Stripe/Vipps)**
   - Hvorfor: PCI-DSS compliance, banking relationships
   - Alternativ: Ingen realistisk (koster millioner)

2. **Telecom (Twilio for telefoni)**
   - Hvorfor: Telecom licenses, carrier relationships
   - Alternativ: Kan bruke SIP trunking (litt billigere)

3. **SSL Certificates**
   - Hvorfor: Trust chain, CA authority
   - Alternativ: Let's Encrypt (gratis!)

4. **OAuth Providers (Google, Microsoft)**
   - Hvorfor: Bruker trust, brand recognition
   - Alternativ: Kan ha egen OAuth, men brukere vil ha "Login with Google"

---

### 🟡 Kategori 2: KAN BYGGE SELV (men bruker tredjepart nå)
Disse kan vi erstatte med egne løsninger:

1. **Email Delivery (SendGrid)** ⚠️
   - Nå: SendGrid ($15-100/måned)
   - Kan bygge: Egen SMTP server
   - Utfordring: Email reputation, spam filtering
   - **Anbefaling:** Bygg egen for internal emails, bruk SendGrid for customer emails

2. **Error Tracking (Sentry)** ⚠️
   - Nå: Sentry ($26-80/måned)
   - Kan bygge: Egen error logging system
   - Utfordring: Relativt enkelt!
   - **Anbefaling:** BYGG SELV (se implementasjon nedenfor)

3. **Analytics (Google Analytics, Mixpanel)** ⚠️
   - Nå: Google Analytics (gratis), Mixpanel ($25-100/måned)
   - Kan bygge: HAR ALLEREDE VÅR EGEN! ✅
   - **Status:** FERDIG - vi har Advanced Analytics Dashboard

4. **Database Hosting** ⚠️
   - Nå: Managed PostgreSQL ($20-200/måned)
   - Kan bygge: Egen PostgreSQL server
   - Utfordring: Backup, scaling, maintenance
   - **Anbefaling:** Start med managed, migrer til egen når vi skalerer

5. **Server Hosting** ⚠️
   - Nå: Heroku/AWS/DigitalOcean ($50-500/måned)
   - Kan bygge: Egen server (VPS)
   - Utfordring: DevOps, monitoring, uptime
   - **Anbefaling:** Hybrid - bruk VPS for core, cloud for scaling

---

### ✅ Kategori 3: BYGGE 100% SELV (nye features)
Disse skal vi bygge fra scratch:

1. **Egen Error Tracking System** ✨ NY
2. **Egen Email Server (internal)** ✨ NY
3. **Egen CDN for static files** ✨ NY
4. **Egen Chat/Support System** ✨ NY
5. **Egen CRM System** ✨ NY
6. **Egen Notification Service** ✨ NY
7. **Egen Queue System (Redis)** ✨ NY
8. **Egen Caching System** ✨ NY
9. **Egen File Storage System** ✨ NY
10. **Egen Video Hosting** ✨ NY

---

## 🚀 IMPLEMENTASJONSPLAN - BYGG ALT SELV

### 1. EGEN ERROR TRACKING SYSTEM (erstatter Sentry)

**Tid:** 3 dager
**Besparelse:** $80/måned = $960/år

```python
# src/monitoring/error_tracker.py
"""
Egen Error Tracking System
Erstatter Sentry - full kontroll over data
"""
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel
import traceback
import sys
import hashlib


class ErrorContext(BaseModel):
    """Error context information"""
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    url: Optional[str] = None
    method: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    environment: str = "production"


class ErrorEvent(BaseModel):
    """Error event model"""
    error_id: str
    error_type: str
    error_message: str
    stack_trace: str
    context: ErrorContext
    timestamp: datetime
    fingerprint: str  # Hash for grouping similar errors
    resolved: bool = False
    occurrences: int = 1


class ErrorTracker:
    """
    Self-hosted error tracking system

    Features:
    - Error capture & logging
    - Stack trace analysis
    - Error grouping (by fingerprint)
    - User impact tracking
    - Real-time alerts
    - Error resolution workflow
    - Performance metrics

    Replaces: Sentry
    Cost: $0 (vs $80/month)
    """

    def __init__(self):
        self.errors: Dict[str, ErrorEvent] = {}
        self.alert_webhooks: List[str] = []

    def capture_exception(
        self,
        exception: Exception,
        context: Optional[ErrorContext] = None
    ) -> str:
        """
        Capture exception and create error event

        Usage:
        try:
            risky_operation()
        except Exception as e:
            error_tracker.capture_exception(e, context)
        """
        # Get error details
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = ''.join(traceback.format_exception(
            type(exception),
            exception,
            exception.__traceback__
        ))

        # Create fingerprint (hash) for grouping
        fingerprint = self._create_fingerprint(
            error_type,
            error_message,
            stack_trace
        )

        # Check if error already exists
        if fingerprint in self.errors:
            # Increment occurrence count
            self.errors[fingerprint].occurrences += 1
            self.errors[fingerprint].timestamp = datetime.now()
            return fingerprint

        # Create new error event
        error_event = ErrorEvent(
            error_id=fingerprint[:8],  # Short ID
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            context=context or ErrorContext(),
            timestamp=datetime.now(),
            fingerprint=fingerprint
        )

        # Store error
        self.errors[fingerprint] = error_event

        # Alert if critical
        if self._is_critical(error_event):
            await self._send_alert(error_event)

        # Save to database
        await self._save_to_db(error_event)

        return fingerprint

    def _create_fingerprint(
        self,
        error_type: str,
        message: str,
        stack: str
    ) -> str:
        """Create unique fingerprint for error grouping"""
        # Extract relevant stack trace lines
        stack_lines = [
            line for line in stack.split('\n')
            if 'File' in line and '/venv/' not in line
        ]
        stack_key = '\n'.join(stack_lines[:3])  # Top 3 frames

        # Create hash
        content = f"{error_type}:{message}:{stack_key}"
        return hashlib.sha256(content.encode()).hexdigest()

    def _is_critical(self, error: ErrorEvent) -> bool:
        """Determine if error is critical"""
        critical_types = [
            'DatabaseError',
            'PaymentError',
            'SecurityError',
            'DataLossError'
        ]

        return error.error_type in critical_types

    async def _send_alert(self, error: ErrorEvent):
        """Send alert to team (Slack, email, etc.)"""
        # Send to Slack webhook
        import requests
        for webhook in self.alert_webhooks:
            requests.post(webhook, json={
                "text": f"🚨 CRITICAL ERROR: {error.error_type}",
                "attachments": [{
                    "color": "danger",
                    "fields": [
                        {"title": "Message", "value": error.error_message},
                        {"title": "Environment", "value": error.context.environment},
                        {"title": "User", "value": str(error.context.user_id or "N/A")}
                    ]
                }]
            })

    async def _save_to_db(self, error: ErrorEvent):
        """Save error to database"""
        # In production: save to PostgreSQL
        pass

    def get_error_stats(self) -> Dict:
        """Get error statistics"""
        return {
            "total_errors": len(self.errors),
            "total_occurrences": sum(e.occurrences for e in self.errors.values()),
            "unresolved": sum(1 for e in self.errors.values() if not e.resolved),
            "critical": sum(1 for e in self.errors.values() if self._is_critical(e))
        }

    def get_top_errors(self, limit: int = 10) -> List[ErrorEvent]:
        """Get most frequent errors"""
        return sorted(
            self.errors.values(),
            key=lambda e: e.occurrences,
            reverse=True
        )[:limit]


# Global instance
error_tracker = ErrorTracker()


# Python exception hook
def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Capture all unhandled exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_tracker.capture_exception(
        exc_value,
        ErrorContext(environment="production")
    )

# Install global handler
sys.excepthook = global_exception_handler
```

**Dashboard for errors:**
```python
# src/api/error_tracking_endpoints.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/errors", tags=["error_tracking"])

@router.get("/stats")
async def get_error_stats():
    """Get error statistics"""
    return error_tracker.get_error_stats()

@router.get("/top")
async def get_top_errors(limit: int = 10):
    """Get most frequent errors"""
    return error_tracker.get_top_errors(limit)

@router.post("/{fingerprint}/resolve")
async def resolve_error(fingerprint: str):
    """Mark error as resolved"""
    if fingerprint in error_tracker.errors:
        error_tracker.errors[fingerprint].resolved = True
        return {"status": "resolved"}
    return {"error": "not found"}
```

**Fordeler vs Sentry:**
- ✅ Full kontroll over data
- ✅ Ingen månedlig kostnad
- ✅ Ubegrenset events
- ✅ Kan tilpasse til våre behov
- ✅ Ingen data sendes til tredjepart

---

### 2. EGEN EMAIL SERVER (for interne emails)

**Tid:** 5 dager
**Besparelse:** $30/måned = $360/år (for interne emails)

```python
# src/email/own_email_server.py
"""
Egen SMTP Email Server
For interne emails (notifications, internal comms)

For kunde-emails: fortsett med SendGrid (bedre reputation)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from pydantic import BaseModel


class EmailMessage(BaseModel):
    """Email message model"""
    to: List[str]
    subject: str
    body_text: str
    body_html: Optional[str] = None
    from_address: str = "noreply@mindframe.no"
    cc: List[str] = []
    bcc: List[str] = []
    attachments: List[str] = []


class OwnEmailServer:
    """
    Self-hosted email server for internal use

    Use cases:
    - Team notifications
    - Internal reports
    - System alerts
    - Developer notifications

    For customer emails: Use SendGrid (better deliverability)
    """

    def __init__(
        self,
        smtp_host: str = "smtp.mindframe.no",
        smtp_port: int = 587,
        username: str = "system@mindframe.no",
        password: str = "..."
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    async def send_email(self, message: EmailMessage) -> bool:
        """Send email via our own SMTP server"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = message.from_address
            msg['To'] = ', '.join(message.to)
            msg['Subject'] = message.subject

            if message.cc:
                msg['Cc'] = ', '.join(message.cc)

            # Add text body
            text_part = MIMEText(message.body_text, 'plain', 'utf-8')
            msg.attach(text_part)

            # Add HTML body (if provided)
            if message.body_html:
                html_part = MIMEText(message.body_html, 'html', 'utf-8')
                msg.attach(html_part)

            # Add attachments
            for filepath in message.attachments:
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={filepath.split("/")[-1]}'
                    )
                    msg.attach(part)

            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)

                recipients = message.to + message.cc + message.bcc
                server.sendmail(
                    message.from_address,
                    recipients,
                    msg.as_string()
                )

            logger.info(f"Email sent to {message.to}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    async def send_team_notification(
        self,
        subject: str,
        message: str,
        recipients: List[str] = None
    ):
        """Send notification to team"""
        default_recipients = [
            "team@mindframe.no",
            "alerts@mindframe.no"
        ]

        await self.send_email(EmailMessage(
            to=recipients or default_recipients,
            subject=f"[Mindframe Alert] {subject}",
            body_text=message
        ))


# For customer emails, still use SendGrid:
class EmailRouter:
    """
    Smart email routing

    Internal emails → Our SMTP server
    Customer emails → SendGrid (better reputation)
    """

    def __init__(self):
        self.own_server = OwnEmailServer()
        self.sendgrid_client = SendGridEmailService()

    async def send(self, message: EmailMessage):
        """Route email to appropriate service"""
        # Check if internal email
        if all('@mindframe.no' in addr for addr in message.to):
            # Use our own server
            return await self.own_server.send_email(message)
        else:
            # Use SendGrid for customer emails
            return await self.sendgrid_client.send(message)
```

**Setup instructions:**
```bash
# Install Postfix (SMTP server)
sudo apt-get install postfix

# Configure DNS records:
# MX record: mail.mindframe.no → server IP
# SPF record: "v=spf1 mx ~all"
# DKIM: Generate and add public key to DNS

# Configure Postfix
sudo nano /etc/postfix/main.cf
# Set:
# myhostname = mail.mindframe.no
# mydomain = mindframe.no
# myorigin = $mydomain
```

---

### 3. EGEN CHAT/SUPPORT SYSTEM (erstatter Intercom)

**Tid:** 1 uke
**Besparelse:** $74/måned = $888/år

```python
# src/support/live_chat.py
"""
Egen Live Chat & Support System
Erstatter Intercom/Zendesk
"""
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from fastapi import WebSocket


class ChatMessage(BaseModel):
    """Chat message model"""
    message_id: str
    conversation_id: str
    from_user_id: Optional[int] = None  # None = support agent
    message: str
    timestamp: datetime
    read: bool = False


class Conversation(BaseModel):
    """Support conversation"""
    conversation_id: str
    customer_id: int
    customer_name: str
    customer_email: str
    status: str  # "open", "in_progress", "resolved", "closed"
    priority: str  # "low", "medium", "high", "urgent"
    assigned_to: Optional[int] = None
    messages: List[ChatMessage] = []
    created_at: datetime
    resolved_at: Optional[datetime] = None
    tags: List[str] = []


class LiveChatSystem:
    """
    Self-hosted live chat & support system

    Features:
    - Real-time chat (WebSocket)
    - Support ticketing
    - Agent assignment
    - Canned responses
    - Chat history
    - Customer info panel
    - Typing indicators
    - File attachments
    - Satisfaction surveys

    Replaces: Intercom ($74/mo), Zendesk ($49/mo)
    """

    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.active_connections: Dict[int, WebSocket] = {}
        self.support_agents: Dict[int, WebSocket] = {}

    async def connect_customer(
        self,
        websocket: WebSocket,
        customer_id: int
    ):
        """Connect customer to chat"""
        await websocket.accept()
        self.active_connections[customer_id] = websocket

    async def connect_agent(
        self,
        websocket: WebSocket,
        agent_id: int
    ):
        """Connect support agent"""
        await websocket.accept()
        self.support_agents[agent_id] = websocket

    async def send_message(
        self,
        conversation_id: str,
        from_user_id: Optional[int],
        message: str
    ):
        """Send chat message"""
        conversation = self.conversations.get(conversation_id)
        if not conversation:
            return

        # Create message
        chat_message = ChatMessage(
            message_id=str(datetime.now().timestamp()),
            conversation_id=conversation_id,
            from_user_id=from_user_id,
            message=message,
            timestamp=datetime.now()
        )

        conversation.messages.append(chat_message)

        # Send to customer
        if conversation.customer_id in self.active_connections:
            ws = self.active_connections[conversation.customer_id]
            await ws.send_json({
                "type": "message",
                "data": chat_message.dict()
            })

        # Send to assigned agent
        if conversation.assigned_to in self.support_agents:
            ws = self.support_agents[conversation.assigned_to]
            await ws.send_json({
                "type": "message",
                "data": chat_message.dict()
            })

    async def assign_to_agent(
        self,
        conversation_id: str,
        agent_id: int
    ):
        """Assign conversation to support agent"""
        if conversation_id in self.conversations:
            self.conversations[conversation_id].assigned_to = agent_id
            self.conversations[conversation_id].status = "in_progress"

    def get_canned_responses(self) -> List[Dict]:
        """Get pre-written responses for common questions"""
        return [
            {
                "id": "welcome",
                "title": "Welcome Message",
                "content": "Hi! Thanks for reaching out. How can I help you today?"
            },
            {
                "id": "pricing",
                "title": "Pricing Info",
                "content": "Our pricing is: FREE ($0), PRO ($99/mo), ENTERPRISE ($499/mo). Which plan are you interested in?"
            },
            {
                "id": "onboarding",
                "title": "Onboarding Help",
                "content": "I'd be happy to help you get started! Let me guide you through the setup process."
            }
        ]


# WebSocket endpoint
@router.websocket("/ws/chat/{customer_id}")
async def chat_websocket(
    websocket: WebSocket,
    customer_id: int
):
    """Customer chat WebSocket"""
    await live_chat.connect_customer(websocket, customer_id)

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "message":
                await live_chat.send_message(
                    data["conversation_id"],
                    customer_id,
                    data["message"]
                )
    except:
        del live_chat.active_connections[customer_id]
```

**React Chat Widget:**
```typescript
// frontend/src/components/LiveChat.tsx
const LiveChat = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [ws, setWs] = useState<WebSocket | null>(null)

  useEffect(() => {
    // Connect to WebSocket
    const socket = new WebSocket(`ws://api.mindframe.no/ws/chat/${userId}`)

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'message') {
        setMessages(prev => [...prev, data.data])
      }
    }

    setWs(socket)

    return () => socket.close()
  }, [])

  const sendMessage = (text: string) => {
    ws?.send(JSON.stringify({
      type: 'message',
      conversation_id: conversationId,
      message: text
    }))
  }

  return (
    <div className="chat-widget">
      {/* Chat UI */}
    </div>
  )
}
```

---

Fortsetter med flere systemer i neste melding...
