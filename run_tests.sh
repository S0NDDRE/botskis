#!/bin/bash

# Test Runner Script
# Runs all tests with coverage reporting

set -e

echo "🧪 Running Mindframe Test Suite"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activate virtual environment if exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "${YELLOW}Installing test dependencies...${NC}"
pip install -q pytest pytest-cov pytest-asyncio httpx

echo ""
echo "${YELLOW}Running Unit Tests...${NC}"
pytest tests/ -m unit -v --tb=short

echo ""
echo "${YELLOW}Running Integration Tests...${NC}"
pytest tests/ -m integration -v --tb=short

echo ""
echo "${YELLOW}Running E2E Tests...${NC}"
pytest tests/ -m e2e -v --tb=short

echo ""
echo "${YELLOW}Running All Tests with Coverage...${NC}"
pytest tests/ \
    --cov=src \
    --cov-report=html \
    --cov-report=term \
    --cov-report=json \
    -v

echo ""
echo "${GREEN}✅ Test Suite Complete!${NC}"
echo ""
echo "📊 Coverage Report:"
echo "   HTML: file://$(pwd)/htmlcov/index.html"
echo "   JSON: coverage.json"
echo ""

# Check if coverage meets threshold
coverage_percent=$(python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])")

echo "Coverage: ${coverage_percent}%"

if (( $(echo "$coverage_percent >= 80" | bc -l) )); then
    echo "${GREEN}✅ Coverage threshold met (80%+)${NC}"
    exit 0
else
    echo "${YELLOW}⚠️  Coverage below 80% threshold${NC}"
    exit 1
fi
