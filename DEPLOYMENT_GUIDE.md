# 🚀 MINDFRAME PRODUCTION DEPLOYMENT GUIDE

**Complete guide to deploying Mindframe to production**

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### ✅ Code Ready
- [x] All features implemented
- [x] Critical bugs fixed
- [x] Security hardening complete
- [x] Legal documents prepared
- [ ] Automated tests passing (if added)

### ✅ Infrastructure
- [ ] Domain registered (mindframe.ai)
- [ ] SSL certificates obtained
- [ ] Server provisioned
- [ ] Database created
- [ ] Redis instance setup
- [ ] CDN configured

### ✅ Third-Party Services
- [ ] Stripe account (payment)
- [ ] SendGrid account (email)
- [ ] OpenAI API key
- [ ] Twilio account (voice AI)
- [ ] Sentry account (monitoring)
- [ ] AWS/DigitalOcean account

### ✅ Environment Variables
- [ ] All secrets configured
- [ ] Production .env file created
- [ ] Secrets stored in vault

---

## 🏗️ INFRASTRUCTURE SETUP

### Option 1: DigitalOcean (Recommended for Start)

**Droplet Specs:**
- CPU: 4 vCPUs
- RAM: 8 GB
- Storage: 160 GB SSD
- Cost: ~$48/month

**Managed Database:**
- PostgreSQL 14
- 2 GB RAM, 1 vCPU
- Cost: ~$15/month

**Managed Redis:**
- 1 GB RAM
- Cost: ~$15/month

**Total:** ~$78/month

### Option 2: AWS (Recommended for Scale)

**EC2 Instance:**
- t3.large (2 vCPUs, 8 GB RAM)
- Cost: ~$60/month

**RDS PostgreSQL:**
- db.t3.small
- Cost: ~$30/month

**ElastiCache Redis:**
- cache.t3.micro
- Cost: ~$15/month

**S3 + CloudFront:**
- Storage + CDN
- Cost: ~$10/month

**Total:** ~$115/month

---

## 📦 BACKEND DEPLOYMENT

### 1. Server Setup (Ubuntu 22.04)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install PostgreSQL client
sudo apt install postgresql-client

# Install Redis tools
sudo apt install redis-tools

# Install Nginx
sudo apt install nginx

# Install Supervisor (for process management)
sudo apt install supervisor

# Install Certbot (SSL)
sudo apt install certbot python3-certbot-nginx
```

### 2. Clone Repository

```bash
# Create app directory
sudo mkdir -p /var/www/mindframe
sudo chown $USER:$USER /var/www/mindframe

# Clone repo
cd /var/www/mindframe
git clone https://github.com/yourusername/mindframe.git .
git checkout main
```

### 3. Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Variables

```bash
# Copy and configure .env
cp .env.example .env
nano .env

# Set production values:
# - DATABASE_URL (PostgreSQL connection string)
# - STRIPE_SECRET_KEY
# - SENDGRID_API_KEY
# - OPENAI_API_KEY
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - ENVIRONMENT=production
# - DEBUG=False
```

### 5. Database Migrations

```bash
# Initialize Alembic (if not done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/mindframe.service
```

```ini
[Unit]
Description=Mindframe FastAPI Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mindframe
Environment="PATH=/var/www/mindframe/venv/bin"
ExecStart=/var/www/mindframe/venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable mindframe
sudo systemctl start mindframe
sudo systemctl status mindframe
```

### 7. Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/mindframe
```

```nginx
# API Server
server {
    listen 80;
    server_name api.mindframe.ai;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Frontend
server {
    listen 80;
    server_name mindframe.ai www.mindframe.ai;

    root /var/www/mindframe/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API proxy
    location /api {
        proxy_pass http://api.mindframe.ai;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/mindframe /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 8. SSL Certificates

```bash
# Get SSL certificates
sudo certbot --nginx -d mindframe.ai -d www.mindframe.ai -d api.mindframe.ai

# Auto-renewal is configured automatically
# Test renewal:
sudo certbot renew --dry-run
```

---

## 🎨 FRONTEND DEPLOYMENT

### 1. Build Frontend

```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Files will be in frontend/dist/
```

### 2. Deploy to Vercel (Alternative)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

**Vercel Configuration (vercel.json):**
```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://api.mindframe.ai/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 🗄️ DATABASE SETUP

### PostgreSQL Configuration

```sql
-- Create database
CREATE DATABASE mindframe;

-- Create user
CREATE USER mindframe_user WITH ENCRYPTED PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mindframe TO mindframe_user;

-- Connect to database
\c mindframe

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO mindframe_user;
```

### Database Backups

```bash
# Create backup script
sudo nano /usr/local/bin/backup-mindframe-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/mindframe"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="mindframe_backup_$DATE.sql"

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U mindframe_user mindframe > $BACKUP_DIR/$FILENAME

# Compress
gzip $BACKUP_DIR/$FILENAME

# Delete backups older than 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete

# Upload to S3 (optional)
# aws s3 cp $BACKUP_DIR/$FILENAME.gz s3://mindframe-backups/
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-mindframe-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
0 2 * * * /usr/local/bin/backup-mindframe-db.sh
```

---

## 📧 SENDGRID SETUP

### 1. Create Account
- Go to sendgrid.com
- Create account
- Verify sender identity

### 2. Create API Key
- Settings → API Keys → Create API Key
- Full Access
- Copy key to .env

### 3. Domain Authentication
- Settings → Sender Authentication
- Authenticate Domain (mindframe.ai)
- Add DNS records

### 4. Test Email
```bash
python -c "
from src.email.email_manager import EmailManager
manager = EmailManager(api_key='your_key')
await manager.send_welcome_email(
    'test@example.com',
    'Test User',
    'https://mindframe.ai/dashboard'
)
"
```

---

## 💳 STRIPE SETUP

### 1. Create Account
- Go to stripe.com
- Create account
- Complete business verification

### 2. Get API Keys
- Developers → API keys
- Copy Publishable key and Secret key
- Add to .env

### 3. Create Products & Prices
```bash
# Pro Plan
stripe products create --name "Mindframe Pro" --description "Pro plan"
stripe prices create --product prod_xxx --unit-amount 9900 --currency usd --recurring[interval]=month

# Enterprise Plan
stripe products create --name "Mindframe Enterprise"
stripe prices create --product prod_xxx --unit-amount 49900 --currency usd --recurring[interval]=month
```

### 4. Setup Webhooks
- Developers → Webhooks → Add endpoint
- Endpoint URL: `https://api.mindframe.ai/webhooks/stripe`
- Select events:
  - customer.subscription.created
  - customer.subscription.updated
  - customer.subscription.deleted
  - invoice.payment_succeeded
  - invoice.payment_failed
- Copy webhook secret to .env

---

## 🔒 SECURITY HARDENING

### 1. Firewall (UFW)

```bash
# Install UFW
sudo apt install ufw

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

### 2. Fail2Ban

```bash
# Install
sudo apt install fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Add SSH protection
[sshd]
enabled = true
maxretry = 3
bantime = 3600

# Start
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Security Headers

Add to Nginx config:
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

---

## 📊 MONITORING SETUP

### 1. Sentry (Error Tracking)

```python
# Already configured in code
# Just need to set SENTRY_DSN in .env
```

### 2. Uptime Monitoring

**Options:**
- UptimeRobot (free)
- Pingdom
- StatusCake

**Configure:**
- Monitor: https://mindframe.ai
- Monitor: https://api.mindframe.ai/health
- Alert: Email + SMS

### 3. Server Monitoring

```bash
# Install monitoring agent (optional)
# Datadog, New Relic, etc.
```

---

## 🧪 TESTING PRODUCTION

### Health Check
```bash
curl https://api.mindframe.ai/health
```

### API Test
```bash
curl https://api.mindframe.ai/api/v1/courses
```

### WebSocket Test
```bash
wscat -c wss://api.mindframe.ai/ws
```

### Load Test
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test
ab -n 1000 -c 10 https://api.mindframe.ai/api/v1/courses
```

---

## 🚦 GO-LIVE CHECKLIST

### Pre-Launch
- [ ] All tests passing
- [ ] Database migrated
- [ ] SSL certificates installed
- [ ] DNS configured
- [ ] Backups automated
- [ ] Monitoring active
- [ ] Secrets secured
- [ ] Legal docs published

### Launch Day
- [ ] Deploy backend
- [ ] Deploy frontend
- [ ] Test all features
- [ ] Monitor logs
- [ ] Check analytics
- [ ] Send launch email

### Post-Launch
- [ ] Monitor errors (Sentry)
- [ ] Check performance
- [ ] Review user feedback
- [ ] Scale if needed
- [ ] Plan improvements

---

## 🆘 TROUBLESHOOTING

### Service Won't Start
```bash
# Check logs
sudo journalctl -u mindframe -f

# Check process
ps aux | grep uvicorn

# Restart
sudo systemctl restart mindframe
```

### Database Connection Issues
```bash
# Test connection
psql -h localhost -U mindframe_user -d mindframe

# Check firewall
sudo ufw status
```

### High CPU Usage
```bash
# Check processes
top

# Increase workers if needed
# Edit /etc/systemd/system/mindframe.service
--workers 8
```

### SSL Certificate Issues
```bash
# Renew
sudo certbot renew --force-renewal

# Check expiry
sudo certbot certificates
```

---

## 📞 SUPPORT CONTACTS

**Technical Issues:**
- Email: tech@mindframe.ai
- Slack: #technical-support

**Infrastructure:**
- DigitalOcean Support
- AWS Support

**Third-Party Services:**
- Stripe Support
- SendGrid Support
- OpenAI Support

---

## 📚 ADDITIONAL RESOURCES

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Nginx Best Practices](https://www.nginx.com/resources/wiki/)
- [PostgreSQL Tuning](https://pgtune.leopard.in.ua/)
- [Stripe Integration](https://stripe.com/docs)
- [SendGrid API](https://docs.sendgrid.com/)

---

**DEPLOYMENT COMPLETE! 🎉**

*Monitor your application and scale as needed.*
*Remember to rotate secrets regularly.*
*Keep backups and have a disaster recovery plan.*
