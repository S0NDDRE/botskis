# 🏠 LOKAL SETUP - Mindframe AI
**Kjør Mindframe AI lokalt på din maskin**

---

## 🚀 QUICK START (5 minutter)

### Enkleste måten:
```bash
./start_all.sh
```

**Ferdig!** 🎉
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📋 DETALJERT SETUP

### 1. Forutsetninger

**Må ha installert:**
- Python 3.11+ (sjekk: `python3 --version`)
- Node.js 18+ (sjekk: `node --version`)
- npm eller yarn

**Anbefalt (men ikke påkrevd):**
- PostgreSQL 14+ (bruker SQLite hvis ikke installert)
- Redis (for caching - valgfritt)

### 2. Backend Setup

#### Steg 1: Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# eller
venv\Scripts\activate     # Windows
```

#### Steg 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Steg 3: Environment Variables
```bash
cp .env.example .env
# Rediger .env med dine innstillinger
```

**Minimum .env for lokal testing:**
```env
# Database (SQLite for lokal utvikling)
DATABASE_URL=sqlite:///./mindframe_local.db

# Secret key (generer med: openssl rand -hex 32)
SECRET_KEY=din-secret-key-her

# API Keys (valgfritt for lokal test)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Stripe (test mode)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Email (valgfritt)
SENDGRID_API_KEY=SG...
```

#### Steg 4: Database Migrations
```bash
alembic upgrade head
```

#### Steg 5: Start Backend
```bash
./start_backend.sh
# eller
uvicorn src.api.main:app --reload
```

**Backend kjører nå på:** http://localhost:8000

### 3. Frontend Setup

#### Steg 1: Install Dependencies
```bash
cd frontend
npm install
```

#### Steg 2: Environment Variables
```bash
# Lag frontend/.env.local
cat > .env.local <<EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
EOF
```

#### Steg 3: Start Frontend
```bash
npm run dev
# eller bruk scriptet:
cd ..
./start_frontend.sh
```

**Frontend kjører nå på:** http://localhost:5173

---

## 🎯 STARTUP SCRIPTS

### Start Alt (Anbefalt)
```bash
./start_all.sh
```

Starter både backend og frontend i ett kommando.

### Start Backend Alene
```bash
./start_backend.sh
```

### Start Frontend Alene
```bash
./start_frontend.sh
```

---

## 🔧 KONFIGURASJON

### Database Valg

**SQLite (Standard for lokal)**
```env
DATABASE_URL=sqlite:///./mindframe_local.db
```
✅ Ingen setup påkrevd
✅ Perfekt for testing
❌ Ikke for produksjon

**PostgreSQL (Anbefalt for testing prod-lignende)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/mindframe
```
✅ Produksjonslignende
✅ Bedre ytelse
⚠️  Må installere PostgreSQL

### Redis (Valgfritt)

For caching og background jobs:
```env
REDIS_URL=redis://localhost:6379/0
```

Installer Redis:
```bash
# Mac
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo systemctl start redis
```

### API Keys (Valgfritt for lokal testing)

**OpenAI:**
```env
OPENAI_API_KEY=sk-...
```
Få key fra: https://platform.openai.com/api-keys

**Anthropic (Claude):**
```env
ANTHROPIC_API_KEY=sk-ant-...
```
Få key fra: https://console.anthropic.com/

**Stripe (Test Mode):**
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```
Få keys fra: https://dashboard.stripe.com/test/apikeys

---

## 🧪 TESTING

### Kjør Alle Tester
```bash
./run_tests.sh
# eller
pytest
```

### Kjør Med Coverage
```bash
pytest --cov=src --cov-report=html
```

Se coverage rapport i: `htmlcov/index.html`

### Kjør Spesifikk Test
```bash
pytest tests/test_agents.py
pytest tests/test_payments.py -v
```

---

## 🌐 TILGANG

Når alt kjører:

**Frontend:**
- URL: http://localhost:5173
- Login: Lag konto via `/signup`

**Backend API:**
- URL: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

**Database:**
- SQLite: `mindframe_local.db` (vis med: `sqlite3 mindframe_local.db`)
- PostgreSQL: `psql mindframe`

---

## 🐛 FEILSØKING

### Backend starter ikke

**Problem:** `ModuleNotFoundError`
```bash
# Løsning: Installer dependencies
pip install -r requirements.txt
```

**Problem:** `Database connection failed`
```bash
# Løsning: Bruk SQLite
export DATABASE_URL="sqlite:///./mindframe_local.db"
```

**Problem:** `Port 8000 already in use`
```bash
# Løsning: Finn og drep prosess
lsof -ti:8000 | xargs kill -9
# eller bruk annen port
uvicorn src.api.main:app --port 8001
```

### Frontend starter ikke

**Problem:** `node_modules not found`
```bash
# Løsning: Install
cd frontend && npm install
```

**Problem:** `Port 5173 already in use`
```bash
# Løsning: Vite velger automatisk neste ledige port
# eller spesifiser:
npm run dev -- --port 5174
```

**Problem:** `API calls fail (CORS)`
```bash
# Sjekk at backend kjører på localhost:8000
# Sjekk at VITE_API_URL er korrekt i .env.local
```

### Database problemer

**Problem:** `Alembic migration failed`
```bash
# Løsning: Reset database
rm mindframe_local.db
alembic upgrade head
```

**Problem:** `PostgreSQL connection refused`
```bash
# Sjekk at PostgreSQL kjører:
pg_isready

# Start PostgreSQL:
# Mac: brew services start postgresql
# Ubuntu: sudo systemctl start postgresql
```

---

## 📊 SYSTEMKRAV

### Minimum
- CPU: 2 cores
- RAM: 4GB
- Disk: 2GB ledig plass
- OS: Linux, macOS, Windows (WSL)

### Anbefalt
- CPU: 4+ cores
- RAM: 8GB+
- Disk: 10GB+ ledig plass
- SSD

---

## 🔐 SIKKERHET (Lokal Utvikling)

### IKKE gjør dette lokalt:
- ❌ Bruk ekte production API keys
- ❌ Bruk ekte customer data
- ❌ Eksponer port 8000 til internett
- ❌ Commit .env fil til git

### GJØR dette:
- ✅ Bruk test mode for Stripe/Vipps
- ✅ Bruk fake/test data
- ✅ Hold backend på localhost
- ✅ Bruk .env.example som template

---

## 🚀 DEPLOYMENT

Når du er klar for production, se:
- `DEPLOYMENT_GUIDE.md` - Full deployment guide
- `docker-compose.yml` - Docker setup
- `deployment/` - Deployment scripts

---

## 📚 NESTE STEG

1. ✅ Start plattformen lokalt
2. ✅ Lag en test-bruker
3. ✅ Test AI-agenter
4. ✅ Test billing flow (test mode)
5. ✅ Se dokumentasjon i `/docs`
6. ✅ Les API docs på `/docs`
7. ✅ Kjør tester
8. ✅ Les `DEPLOYMENT_GUIDE.md` for prod

---

## 💡 TIPS

### Hot Reload
Både backend og frontend har hot reload:
- Endre Python kode → Backend restarter automatisk
- Endre React kode → Frontend oppdaterer automatisk

### Database GUI
Vis database med:
```bash
# SQLite
sqlite3 mindframe_local.db
.tables
.schema users

# PostgreSQL
psql mindframe
\dt
\d users
```

### Logs
Backend logger til:
- Console (se terminal)
- `logs/` directory

Frontend logger til:
- Browser console (F12)

### API Testing
Test API med:
- Swagger UI: http://localhost:8000/docs
- cURL: `curl http://localhost:8000/api/v1/health`
- Postman/Insomnia

---

## 🆘 HJELP

**Problem du ikke finner løsning på?**

1. Sjekk `FEILSØKING` seksjonen over
2. Se `README.md` for mer info
3. Sjekk logs i `logs/` directory
4. Kjør tester: `pytest -v`
5. Reset alt:
```bash
# Backend
rm mindframe_local.db
alembic upgrade head

# Frontend
cd frontend
rm -rf node_modules
npm install
```

---

## ✅ QUICK CHECKLIST

- [ ] Python 3.11+ installert
- [ ] Node.js 18+ installert
- [ ] Virtual environment aktivert
- [ ] `pip install -r requirements.txt` kjørt
- [ ] `.env` fil opprettet
- [ ] `npm install` kjørt i `frontend/`
- [ ] `frontend/.env.local` opprettet
- [ ] Database migrert (`alembic upgrade head`)
- [ ] Backend starter (`./start_backend.sh`)
- [ ] Frontend starter (`./start_frontend.sh`)
- [ ] http://localhost:8000/docs laster
- [ ] http://localhost:5173 laster

**Alle checks? Du er klar! 🎉**

---

**Lykke til med utvikling! 🚀**

**Mindframe AI - Lokal Development**
