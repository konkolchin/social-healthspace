FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PROJECT_NAME="Social HealthSpace"
ENV VERSION="1.0.0"
ENV API_V1_STR="/api/v1"
ENV JWT_ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES="30"

# Expose port
EXPOSE ${PORT}

# Healthcheck with more debugging
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD sh -c "echo 'Checking health...' && \
               echo 'Network status:' && netstat -tulpn && \
               echo 'Processes:' && ps aux && \
               curl -v http://localhost:${PORT}/health || exit 1"

# Run the application with extensive debugging
CMD ["sh", "-c", "echo 'Starting application with environment variables:' && \
                  env && \
                  echo 'Current directory:' && pwd && ls -la && \
                  echo 'Network interfaces:' && ifconfig && \
                  echo 'Starting uvicorn...' && \
                  uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --log-level debug --reload"] 