# Simple Dockerfile for Railway deployment
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies  
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy minimal requirements and install dependencies
COPY requirements_minimal.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_minimal.txt

# Copy application code
COPY backend/ ./backend/
COPY src/ ./src/

ENV PYTHONPATH=/app/src:/app/backend:/app

# Expose port
EXPOSE 8000

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Build frontend first
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Continue with backend and serve both
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy minimal requirements and install dependencies
COPY requirements_minimal.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_minimal.txt

# Copy application code
COPY backend/ ./backend/
COPY src/ ./src/

# Copy built frontend
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public

ENV PYTHONPATH=/app/src:/app/backend:/app

# Expose port
EXPOSE 8000

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the full-stack application
CMD ["uvicorn", "backend.main_fullstack:app", "--host", "0.0.0.0", "--port", "8000"]