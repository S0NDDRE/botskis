# 🎓 MINDFRAME TRAINING COURSE
## Lær hvordan hele plattformen fungerer

**Målgruppe:** Deg (eier) + fremtidige teammedlemmer
**Tid:** 20 timer total (5 moduler × 4 timer)
**Format:** Video + hands-on praksis
**Mål:** Du kan drifte og utvikle plattformen selv

---

## 📚 KURSSTRUKTUR

### MODUL 1: PLATTFORM OVERSIKT (4 timer)
**Mål:** Forstå "big picture" - hvordan alt henger sammen

#### Del 1: Architecture (1 time)
**Hva du lærer:**
- Backend (FastAPI + Python)
- Frontend (React + TypeScript)
- Database (PostgreSQL)
- Hvordan de kommuniserer (REST API)

**Interaktiv øvelse:**
```
1. Åpne browser → localhost:3000
2. Klikk "Login" → Se network tab
3. Se POST request → /api/auth/login
4. Se backend response → JWT token
5. Token lagres i localStorage
6. Alle fremtidige requests bruker token
```

**Output:** Du ser hele requesten fra klikk til respons

---

#### Del 2: Database Structure (1 time)
**Hva du lærer:**
- Users table
- Agents table
- Subscriptions table
- Hvordan de relaterer til hverandre

**Interaktiv øvelse:**
```sql
-- Se alle tabeller
\dt

-- Se users table
SELECT * FROM users LIMIT 5;

-- Se user med subscriptions
SELECT
    u.email,
    s.plan,
    s.status
FROM users u
LEFT JOIN subscriptions s ON u.id = s.user_id
WHERE u.email = 'din@email.com';
```

**Output:** Du forstår data modellen

---

#### Del 3: API Flow (1 time)
**Hva du lærer:**
- Request kommer inn
- Autentisering (JWT token)
- Business logic kjører
- Database query
- Response sendes tilbake

**Interaktiv øvelse:**
```python
# Følg en request gjennom systemet

# 1. Frontend sender request
fetch('/api/agents/customer_support_bot')

# 2. FastAPI router mottar
@router.get("/agents/{agent_id}")
async def get_agent(agent_id: str, user: dict = Depends(get_current_user)):
    # 3. Auth sjekk (get_current_user)
    # 4. Hent fra database
    agent = await db.get_agent(agent_id)
    # 5. Return response
    return {"success": True, "agent": agent}
```

**Output:** Du kan følge en request A-Z

---

#### Del 4: Event Bus Pattern (1 time)
**Hva du lærer:**
- Pub/Sub pattern
- Loose coupling
- Event-driven architecture

**Interaktiv øvelse:**
```python
# Publisher (sender event)
await event_bus.publish(
    event_type="user.registered",
    payload={"user_id": 123, "email": "test@example.com"}
)

# Subscriber (lytter til event)
@event_bus.subscribe("user.registered")
async def on_user_registered(event: Event):
    # Send welcome email
    await send_welcome_email(event.payload["email"])
```

**Oppgave:** Legg til et nytt event og subscriber

**Output:** Du forstår hvorfor vi bruker events

---

### MODUL 2: DEPLOYMENT & OPERATIONS (4 timer)
**Mål:** Drifte plattformen i produksjon

#### Del 1: Server Setup (1 time)
**Hva du lærer:**
- VPS (Virtual Private Server)
- Ubuntu Linux basics
- SSH access
- Firewall setup

**Praktisk:**
```bash
# 1. SSH inn i server
ssh user@your-server.com

# 2. Update system
sudo apt update && sudo apt upgrade

# 3. Install Docker
curl -fsSL https://get.docker.com | sh

# 4. Setup firewall
sudo ufw allow 22  # SSH
sudo ufw allow 80  # HTTP
sudo ufw allow 443 # HTTPS
sudo ufw enable
```

**Output:** Server er klar

---

#### Del 2: Deploy Application (1.5 timer)
**Hva du lærer:**
- Docker deployment
- Environment variables
- Database setup
- Nginx reverse proxy

**Praktisk:**
```bash
# 1. Clone repository
git clone https://github.com/your/mindframe.git
cd mindframe

# 2. Setup environment
cp .env.example .env
nano .env  # Edit secrets

# 3. Build & run with Docker
docker-compose up -d

# 4. Check logs
docker-compose logs -f
```

**Output:** App kjører i produksjon

---

#### Del 3: Database Management (1 time)
**Hva du lærer:**
- Backup & restore
- Migrations
- Performance tuning

**Praktisk:**
```bash
# Backup
pg_dump mindframe > backup_$(date +%Y%m%d).sql

# Restore
psql mindframe < backup_20250116.sql

# Automated backup (cron job)
0 2 * * * pg_dump mindframe > /backups/mindframe_$(date +\%Y\%m\%d).sql

# Keep only last 7 days
find /backups -name "mindframe_*.sql" -mtime +7 -delete
```

**Output:** Data er sikret

---

#### Del 4: Monitoring & Troubleshooting (30 min)
**Hva du lærer:**
- Check logs
- Monitor resources (CPU, RAM, disk)
- Common errors
- How to fix

**Praktisk:**
```bash
# Check app logs
docker-compose logs backend --tail=100 -f

# Check system resources
htop  # CPU & RAM
df -h  # Disk space

# Common issues:
# 1. App won't start → Check docker-compose logs
# 2. Slow performance → Check htop (RAM/CPU)
# 3. Database errors → Check postgres logs
# 4. 500 errors → Check backend logs
```

**Output:** Du kan feilsøke

---

### MODUL 3: ADDING NEW FEATURES (4 timer)
**Mål:** Utvide plattformen selv

#### Del 1: Plugin System (1.5 timer)
**Hva du lærer:**
- Lage ny AI agent
- Hot-reload (ingen restart!)
- Test plugin

**Praktisk - Lag en væragent:**
```python
# src/plugins/weather_agent.py
from src.core.plugin_manager import PluginBase, PluginMetadata, PluginType

class WeatherAgentPlugin(PluginBase):
    @classmethod
    def get_metadata(cls):
        return PluginMetadata(
            id="weather_agent",
            name="Weather Agent",
            version="1.0.0",
            plugin_type=PluginType.AGENT,
            description="Get weather forecast"
        )

    async def on_load(self):
        self.api_key = "YOUR_API_KEY"
        print("Weather agent loaded!")

    async def get_weather(self, city: str):
        # Call weather API
        return {"city": city, "temp": 15, "condition": "Sunny"}

# Last inn plugin (INGEN RESTART!)
await plugin_manager.load_plugin("src/plugins/weather_agent.py")
```

**Oppgave:** Lag din egen agent (f.eks. news agent, stock price agent)

**Output:** Du kan lage nye agenter

---

#### Del 2: API Endpoints (1 time)
**Hva du lærer:**
- Lage nytt API endpoint
- Request/Response modeller
- Error handling

**Praktisk:**
```python
# src/api/my_endpoints.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/my-feature", tags=["My Feature"])

class CreateItemRequest(BaseModel):
    name: str
    description: str

@router.post("/items")
async def create_item(request: CreateItemRequest):
    try:
        # Validate
        if len(request.name) < 3:
            raise HTTPException(400, "Name too short")

        # Save to database
        item = await db.create_item(request.name, request.description)

        return {"success": True, "item": item}
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(500, str(e))
```

**Oppgave:** Lag et endpoint for din egen feature

**Output:** Du kan utvide API

---

#### Del 3: Frontend Components (1 time)
**Hva du lærer:**
- React components
- Connect til API
- State management

**Praktisk:**
```typescript
// frontend/src/components/MyComponent.tsx
import React, { useState, useEffect } from 'react'

export const MyComponent: React.FC = () => {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    try {
      const response = await fetch('/api/my-feature/items')
      const data = await response.json()
      setItems(data.items)
    } catch (error) {
      console.error('Failed to fetch items:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <h1>My Items</h1>
      {items.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  )
}
```

**Oppgave:** Lag en komponent for din feature

**Output:** Du kan bygge UI

---

#### Del 4: Testing (30 min)
**Hva du lærer:**
- Write unit tests
- Test API endpoints
- Debug issues

**Praktisk:**
```python
# tests/test_my_feature.py
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_item():
    response = client.post(
        "/api/my-feature/items",
        json={"name": "Test Item", "description": "Test"}
    )
    assert response.status_code == 200
    assert response.json()["success"] == True

def test_create_item_validation():
    response = client.post(
        "/api/my-feature/items",
        json={"name": "AB", "description": "Too short"}
    )
    assert response.status_code == 400
```

**Output:** Du kan teste kode

---

### MODUL 4: SECURITY & COMPLIANCE (4 timer)
**Mål:** Holde plattformen sikker

#### Del 1: GDPR Compliance (1.5 timer)
**Hva du lærer:**
- User data rights (access, delete, export)
- Cookie consent
- Privacy policy
- Data retention

**Praktisk:**
```python
# Implement GDPR data export
@router.get("/gdpr/export")
async def export_my_data(user: dict = Depends(get_current_user)):
    user_id = user["id"]

    # Gather all user data
    data = {
        "profile": await db.get_user(user_id),
        "subscriptions": await db.get_subscriptions(user_id),
        "agents": await db.get_user_agents(user_id),
        "usage_history": await db.get_usage(user_id)
    }

    # Return as downloadable JSON
    return JSONResponse(data)

# Implement right to be forgotten
@router.delete("/gdpr/delete-me")
async def delete_my_data(user: dict = Depends(get_current_user)):
    user_id = user["id"]

    # Anonymize user data
    await db.anonymize_user(user_id)

    return {"success": True, "message": "Data deleted"}
```

**Output:** GDPR compliant

---

#### Del 2: Security Best Practices (1 time)
**Hva du lærer:**
- SQL injection prevention
- XSS protection
- CSRF tokens
- Rate limiting

**Praktisk:**
```python
# SQL Injection (ALDRI gjør dette!)
❌ BAD:
user = await db.execute(f"SELECT * FROM users WHERE email = '{email}'")

✅ GOOD (parameterized query):
user = await db.execute(
    "SELECT * FROM users WHERE email = :email",
    {"email": email}
)

# XSS Protection
from html import escape
safe_input = escape(user_input)

# Rate Limiting
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/minute")  # Max 5 attempts per minute
async def login(request: Request):
    ...
```

**Output:** Sikker kode

---

#### Del 3: Authentication & Authorization (1 time)
**Hva du lærer:**
- JWT tokens
- Password hashing
- Role-based access (admin, user)

**Praktisk:**
```python
# Password hashing
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])

# Hash password
hashed = pwd_context.hash("user_password")

# Verify password
is_valid = pwd_context.verify("user_password", hashed)

# JWT tokens
from jose import jwt

def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.now() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Role-based access
def require_admin(user: dict = Depends(get_current_user)):
    if not user.get("is_admin"):
        raise HTTPException(403, "Admin access required")
    return user
```

**Output:** Sikker autentisering

---

#### Del 4: Incident Response (30 min)
**Hva du lærer:**
- Hva gjør du hvis det skjer et hack?
- Data breach response
- Customer communication

**Praktisk plan:**
```
1. DETECT breach
   - Monitor alerts
   - User reports

2. CONTAIN
   - Shutdown affected systems
   - Revoke compromised tokens

3. INVESTIGATE
   - Check logs
   - Identify what was accessed

4. REMEDIATE
   - Patch vulnerability
   - Reset passwords

5. COMMUNICATE
   - Notify affected users (within 72h for GDPR)
   - Be transparent

6. LEARN
   - Document incident
   - Update security procedures
```

**Output:** Vet hva du skal gjøre

---

### MODUL 5: SCALING & PERFORMANCE (4 timer)
**Mål:** Håndtere vekst

#### Del 1: Caching Strategies (1.5 timer)
**Hva du lærer:**
- Redis caching
- Cache invalidation
- Query optimization

**Praktisk:**
```python
import redis
cache = redis.Redis(host='localhost', port=6379)

# Cache expensive query
@cache_result(ttl=3600)  # Cache for 1 hour
async def get_agent_marketplace():
    # Expensive database query
    agents = await db.query("SELECT * FROM agents")
    return agents

# Cache invalidation
async def update_agent(agent_id: str, data: dict):
    await db.update_agent(agent_id, data)
    # Clear cache
    cache.delete(f"agent:{agent_id}")
```

**Output:** 10x raskere

---

#### Del 2: Database Optimization (1 time)
**Hva du lærer:**
- Indexing
- Query optimization
- Connection pooling

**Praktisk:**
```sql
-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Add index
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);

-- Optimize query
-- BEFORE (slow - full table scan)
SELECT * FROM users WHERE email LIKE '%@gmail.com';

-- AFTER (fast - uses index)
SELECT * FROM users WHERE email = 'specific@gmail.com';
```

**Output:** Database er rask

---

#### Del 3: Load Balancing (1 time)
**Hva du lærer:**
- Multiple servers
- Load balancer (Nginx)
- Session management

**Praktisk:**
```nginx
# nginx.conf
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }
}
```

**Output:** Kan håndtere mange brukere

---

#### Del 4: Auto-Scaling (30 min)
**Hva du lærer:**
- Kubernetes basics
- Auto-scale basert på load
- Cost optimization

**Praktisk:**
```yaml
# kubernetes-deployment.yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: mindframe-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mindframe-backend
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

**Output:** Automatisk skalering

---

## 📊 LEARNING PATHS

### PATH 1: OPERATIONS (for drift)
**Fokus:** Holde ting kjørende
**Moduler:** 1, 2, 4
**Tid:** 12 timer
**Resultat:** Kan drifte plattformen

### PATH 2: DEVELOPMENT (for utvikling)
**Fokus:** Bygge nye features
**Moduler:** 1, 3, 4
**Tid:** 12 timer
**Resultat:** Kan utvide plattformen

### PATH 3: FULL STACK (alt)
**Fokus:** Komplett forståelse
**Moduler:** 1, 2, 3, 4, 5
**Tid:** 20 timer
**Resultat:** Full kontroll

---

## 🎯 PRAKTISKE OPPGAVER

### Oppgave 1: Deploy til produksjon
1. Sett opp VPS
2. Deploy app
3. Setup monitoring
4. Test med reell traffic

### Oppgave 2: Lag en ny agent
1. Bruk plugin system
2. Implementer business logic
3. Test
4. Deploy uten restart

### Oppgave 3: Handle en incident
1. Simuler error
2. Detect med monitoring
3. Fix
4. Document

---

## ✅ COMPLETION CRITERIA

Du har fullført kurset når du kan:

- [ ] Deploy app til produksjon selv
- [ ] Handle database backup/restore
- [ ] Lage ny AI agent
- [ ] Legge til nytt API endpoint
- [ ] Feilsøke common issues
- [ ] Optimize performance
- [ ] Handle security incident

**Estimert tid:** 20 timer over 1 uke

---

## 🚀 NESTE STEG

**Vil du at jeg:**
1. Lager video tutorials?
2. Starter med Modul 1 (live walkthrough)?
3. Fokuserer på spesifikk modul?

**Jeg kan også:**
- Lage interaktiv quiz for hver modul
- Gi deg hands-on oppgaver
- Code review av dine changes

**Hva vil du starte med?** 🎓
