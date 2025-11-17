# 🚢 Deployment Guide

Guide for å deploye Botskis til produksjon.

## 🎯 Pre-Deployment Checklist

- [ ] Alle tester kjører OK
- [ ] Environment variabler konfigurert
- [ ] Database backup tatt
- [ ] API keys gyldige
- [ ] CORS konfigurert riktig
- [ ] SSL sertifikat klar
- [ ] Monitoring setup

## 🚀 Deployment Options

### 1. Railway (Anbefalt)

Railway gir enkel deployment med automatisk SSL, database, og scaling.

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link existing project (valgfritt)
railway link

# Add PostgreSQL database
railway add -d postgres

# Add Redis
railway add -d redis

# Set environment variables
railway variables set OPENAI_API_KEY=sk-...
railway variables set SECRET_KEY=your-secret-key
railway variables set STRIPE_SECRET_KEY=sk_live_...

# Deploy
railway up

# Get deployment URL
railway domain
```

### 2. Docker / VPS

Deploy til din egen VPS med Docker Compose.

```bash
# SSH til serveren
ssh user@your-server.com

# Clone repo
git clone <repo-url>
cd botskis

# Setup environment
cp .env.example .env
nano .env  # Rediger med production values

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose logs -f
```

### 3. Heroku

```bash
# Login
heroku login

# Create app
heroku create botskis-prod

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Scale workers
heroku ps:scale web=1

# Open app
heroku open
```

### 4. AWS / Google Cloud / Azure

Se separate guides for cloud providers:
- [AWS Deployment](./AWS_DEPLOYMENT.md)
- [GCP Deployment](./GCP_DEPLOYMENT.md)
- [Azure Deployment](./AZURE_DEPLOYMENT.md)

## 🔒 Production Environment Variables

```bash
# App
APP_NAME=Botskis
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<generate-strong-key>

# Database (from Railway/Heroku)
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0

# AI
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Stripe
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SENDGRID_API_KEY=SG...
FROM_EMAIL=noreply@botskis.com

# Monitoring
SENTRY_DSN=https://...@sentry.io/...

# Features
ENABLE_MARKETPLACE=true
ENABLE_AUTO_HEALING=true
ENABLE_ANALYTICS=true
```

## 🏗️ Production docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    env_file:
      - .env.production
    restart: always
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    restart: always

  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
    restart: always

volumes:
  postgres_data:
  redis_data:
```

## 📊 Monitoring Setup

### Sentry (Error Tracking)

```bash
# Add to requirements.txt
sentry-sdk==1.39.1

# Configure in settings.py
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=1.0
    )
```

### Prometheus + Grafana

```bash
# Add prometheus endpoint to API
# Already included in /metrics

# Start Prometheus
docker run -d -p 9090:9090 \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Start Grafana
docker run -d -p 3000:3000 grafana/grafana
```

## 🔐 Security Checklist

- [ ] HTTPS enabled (SSL/TLS)
- [ ] API keys rotated
- [ ] Database encrypted
- [ ] Secrets in environment vars (not code)
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Input validation active
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF tokens

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run tests
        run: |
          pip install -r requirements.txt
          python test_system.py

      - name: Deploy to Railway
        run: |
          npm i -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Railway: Auto-scaling enabled
# Heroku:
heroku ps:scale web=5

# Docker:
docker-compose up -d --scale api=5
```

### Database Scaling

```bash
# Railway: Upgrade plan
railway add -d postgres --plan pro

# Heroku:
heroku addons:upgrade heroku-postgresql:standard-0
```

## 💾 Backup Strategy

```bash
# Daily database backups
0 2 * * * pg_dump $DATABASE_URL > /backups/db_$(date +\%Y\%m\%d).sql

# Weekly full backups
0 3 * * 0 tar -czf /backups/full_$(date +\%Y\%m\%d).tar.gz /app

# Backup retention: 30 days
find /backups -mtime +30 -delete
```

## 🆘 Rollback Procedure

```bash
# Railway
railway rollback

# Heroku
heroku releases
heroku rollback v123

# Docker
docker-compose down
git checkout <previous-commit>
docker-compose up -d
```

## ✅ Post-Deployment

- [ ] Verify health endpoint
- [ ] Test key workflows
- [ ] Check error monitoring
- [ ] Monitor performance
- [ ] Update documentation
- [ ] Notify team
- [ ] Announce to users

## 📞 Support

Production issues? Contact:
- Email: ops@botskis.com
- Slack: #production-alerts
- On-call: See PagerDuty
