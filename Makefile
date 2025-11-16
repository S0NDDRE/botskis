.PHONY: help install dev test clean docker deploy

help:
	@echo "🤖 Botskis - Available Commands"
	@echo "================================"
	@echo "make install    - Install dependencies"
	@echo "make dev        - Start development server"
	@echo "make test       - Run system tests"
	@echo "make clean      - Clean cache files"
	@echo "make docker     - Start with Docker Compose"
	@echo "make deploy     - Deploy to production"
	@echo "make health     - Check system health"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

dev:
	@echo "🚀 Starting development server..."
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	@echo "🧪 Running system tests..."
	python test_system.py

clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✅ Cleaned!"

docker:
	@echo "🐳 Starting Docker Compose..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"

docker-build:
	@echo "🏗️  Building Docker images..."
	docker-compose build

docker-logs:
	@echo "📋 Showing logs..."
	docker-compose logs -f

docker-stop:
	@echo "🛑 Stopping services..."
	docker-compose down

deploy:
	@echo "🚀 Deploying to production..."
	@echo "⚠️  Make sure you've configured environment variables!"
	railway up

health:
	@echo "🏥 Checking system health..."
	curl -s http://localhost:8000/health | jq

init-db:
	@echo "💾 Initializing database..."
	python -c "from src.database.connection import init_db; init_db()"
	@echo "✅ Database initialized!"

migration:
	@echo "🔄 Running database migrations..."
	alembic upgrade head

marketplace-stats:
	@echo "📊 Marketplace statistics..."
	curl -s http://localhost:8000/api/v1/marketplace/stats | jq
