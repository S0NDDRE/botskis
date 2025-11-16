# Mindframe AI - Production Dockerfile
# Multi-stage build for optimized production image

# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy frontend source
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 2: Python backend
FROM python:3.11-slim AS backend

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    redis-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 mindframe && \
    mkdir -p /app && \
    chown -R mindframe:mindframe /app

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies including production server
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY --chown=mindframe:mindframe . .

# Copy built frontend from previous stage
COPY --from=frontend-builder --chown=mindframe:mindframe /app/frontend/dist ./frontend/dist

# Switch to non-root user
USER mindframe

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application with Gunicorn for production
CMD ["gunicorn", "src.api.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
