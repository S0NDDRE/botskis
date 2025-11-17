#!/bin/bash
# Start Mindframe AI (Full Stack - Local Development)

echo "🚀 Starting Mindframe AI - Full Stack"
echo "======================================"
echo ""

# Make scripts executable
chmod +x start_backend.sh
chmod +x start_frontend.sh

# Ensure Python version is compatible before starting anything
PY_CMD=""
if command -v python3 >/dev/null 2>&1; then
  PY_CMD=python3
elif command -v python >/dev/null 2>&1; then
  PY_CMD=python
else
  echo "❌ Python not found on PATH. Install Python 3.11 or 3.12 and retry."
  exit 1
fi

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

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT TERM

# Start backend in background
echo "1️⃣  Starting Backend..."
./start_backend.sh &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo ""

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo "2️⃣  Starting Frontend..."
./start_frontend.sh &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo ""

echo "======================================"
echo "✅ Mindframe AI is running!"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🔌 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "======================================"
echo ""

# Wait for processes
wait
