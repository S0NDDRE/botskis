#!/bin/bash
# Start Mindframe AI Backend (Local Development)

echo "🚀 Starting Mindframe AI Backend..."

# Ensure a compatible Python is used (runs scripts/check_python_version.py)
PY_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PY_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PY_CMD=python
else
  echo "❌ Python not found on PATH. Install Python 3.11 or 3.12 and retry."
  exit 1
fi

# Run version check script; it will exit non-zero on unsupported versions
if [ -f "scripts/check_python_version.py" ]; then
  echo "🔎 Verifying Python version with scripts/check_python_version.py"
  $PY_CMD scripts/check_python_version.py
  if [ $? -ne 0 ]; then
    echo "❌ Unsupported Python version detected. See LOCAL_SETUP.md for recommended versions." 
    exit 1
  fi
else
  echo "⚠️  Version check script not found (scripts/check_python_version.py). Continuing..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: $PY_CMD -m venv venv"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Copying from .env.example..."
    cp .env.example .env
    echo "✅ Created .env - Please edit it with your settings!"
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if PostgreSQL is running (optional for local dev)
if command -v psql &> /dev/null; then
    if pg_isready &> /dev/null; then
        echo "✅ PostgreSQL is running"
    else
        echo "⚠️  PostgreSQL not running - using SQLite for local dev"
        export DATABASE_URL="sqlite:///./mindframe_local.db"
    fi
else
    echo "⚠️  PostgreSQL not installed - using SQLite for local dev"
    export DATABASE_URL="sqlite:///./mindframe_local.db"
fi

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head 2>/dev/null || echo "⚠️  No migrations to run"

# Start backend server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo ""
echo "API Docs: http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
echo ""

uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
