# Force clean build - 2024-04-11
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE ${PORT}

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Run the application with debugging
CMD ["sh", "-c", "echo 'Starting application...' && \
                  echo 'Current directory:' && pwd && ls -la && \
                  echo 'Environment:' && env && \
                  echo 'Waiting for database...' && \
                  while ! nc -z $DATABASE_HOST $DATABASE_PORT; do \
                    echo 'Waiting for database...'; \
                    sleep 2; \
                  done && \
                  echo 'Database is ready!' && \
                  uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"] 