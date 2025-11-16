#!/bin/bash
# Start Mindframe AI Backend (Local Development)

echo "🚀 Starting Mindframe AI Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv venv"
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
