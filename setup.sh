#!/bin/bash
# Setup script for Botskis

set -e  # Exit on error

echo "🏭 Botskis Setup Script"
echo "======================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo "   - OPENAI_API_KEY"
    echo "   - SECRET_KEY (generate with: openssl rand -hex 32)"
    echo "   - DATABASE_URL (if using external DB)"
fi

# Create logs directory
mkdir -p logs
echo "✓ Logs directory created"

# Initialize database (if using SQLite for development)
echo ""
echo "Do you want to initialize the database now? (y/n)"
read -r init_db
if [ "$init_db" = "y" ]; then
    echo "Initializing database..."
    python3 -c "from src.database.connection import init_db; init_db()"
    echo "✓ Database initialized"

    # Create first migration
    echo ""
    echo "Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
    echo "✓ Migrations applied"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API keys"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: python src/api/main.py"
echo "  4. Or run: ./run.sh"
echo ""
echo "API will be at: http://localhost:8000"
echo "Docs will be at: http://localhost:8000/docs"
echo ""
