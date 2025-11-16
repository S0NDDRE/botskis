# 🚀 Quick Start Guide

Kom i gang med Botskis på 5 minutter!

## 📦 Installasjon

### Metode 1: Docker (Anbefalt)

```bash
# Clone repo
git clone <repo-url>
cd botskis

# Kopier environment template
cp .env.example .env

# Rediger .env med dine API keys
nano .env

# Start alt
docker-compose up -d

# Sjekk at alt kjører
docker-compose ps

# Se logs
docker-compose logs -f api
```

API kjører nå på http://localhost:8000

### Metode 2: Lokal Python

```bash
# Opprett virtual environment
python3 -m venv venv
source venv/bin/activate

# Installer dependencies
pip install -r requirements.txt

# Setup database
python -c "from src.database.connection import init_db; init_db()"

# Start API
uvicorn src.api.main:app --reload
```

## ✅ Verifiser Installasjon

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-11-16T...",
  "components": {...}
}
```

## 🎯 Din første Agent

### 1. Opprett bruker

```bash
curl -X POST http://localhost:8000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User",
    "company": "Test AS"
  }'
```

### 2. Start Onboarding

```bash
curl -X POST http://localhost:8000/api/v1/onboarding/start \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'
```

### 3. Se Marketplace

```bash
# Hent alle templates
curl http://localhost:8000/api/v1/marketplace/templates

# Se featured templates
curl http://localhost:8000/api/v1/marketplace/featured

# Se populære templates
curl http://localhost:8000/api/v1/marketplace/popular
```

### 4. Deploy Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": 1,
    "custom_config": {}
  }' \
  -G -d "user_id=1"
```

🎉 **Gratulerer!** Du har nå en kjørende agent!

## 📚 Neste Steg

1. Utforsk API docs: http://localhost:8000/docs
2. Deploy flere agenter fra marketplace
3. Sjekk monitoring dashboard
4. Konfigurer auto-healing
5. Inviter team members

## 🔧 Troubleshooting

### Database Connection Error

```bash
# Sjekk at PostgreSQL kjører
docker-compose ps db

# Restart database
docker-compose restart db
```

### API ikke startet

```bash
# Sjekk logs
docker-compose logs api

# Restart API
docker-compose restart api
```

### Import errors

```bash
# Reinstaller dependencies
pip install -r requirements.txt --force-reinstall
```

## 💡 Tips

- Bruk Swagger UI på `/docs` for interaktiv API testing
- Sjekk `/metrics` for system stats
- Use `/health` for monitoring
- Start med featured templates
- Test i development mode først

## 🆘 Hjelp

- Email: support@botskis.com
- Docs: docs.botskis.com
- Issues: github.com/botskis/issues
