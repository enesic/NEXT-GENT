# Backend Dockerfile for NextGent
# Python 3.11 Slim Image for optimal size/performance/compatibility
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install system dependencies
# gcc and libpq-dev are needed for psycopg2 (PostgreSQL adapter)
# postgresql-client is needed for pg_isready command
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev postgresql-client dos2unix \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy and set permissions for entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

# Expose port (FastAPI default)
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
