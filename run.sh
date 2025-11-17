#!/bin/bash
# Quick run script for Botskis

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Run ./setup.sh first"
    exit 1
fi

echo "🏭 Starting Botskis..."
echo ""
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "WebSocket: ws://localhost:8000/ws/{user_id}"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the application
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
