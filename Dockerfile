# Frontend build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run export || (npm run build && npx next export)

# Backend stage
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (full agent)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY src/ ./src/

# Copy built frontend static export
COPY --from=frontend-builder /app/frontend/out ./frontend/dist
RUN mkdir -p ./frontend/dist

ENV PYTHONPATH=/app/src:/app/backend:/app

# Expose port
EXPOSE 8000

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Environment variable to ensure fullstack mode
ENV APP_MODE=FULLSTACK

# Start unified app (serves API + static)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]