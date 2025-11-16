#!/bin/bash
# Start Mindframe AI Frontend (Local Development)

echo "🚀 Starting Mindframe AI Frontend..."

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies (this may take a few minutes)..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found! Creating default..."
    cat > .env.local <<EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
EOF
    echo "✅ Created .env.local - Edit if needed!"
fi

# Start development server
echo "✅ Starting Vite dev server on http://localhost:5173"
echo ""
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop"
echo ""

npm run dev
