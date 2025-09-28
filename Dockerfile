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

# Start the minimal application
CMD ["uvicorn", "backend.main_minimal:app", "--host", "0.0.0.0", "--port", "8000"]