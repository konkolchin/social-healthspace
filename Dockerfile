FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    net-tools \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Set environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV PROJECT_NAME="Social HealthSpace"
ENV VERSION="1.0.0"
ENV API_V1_STR="/api/v1"
ENV JWT_ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES="30"
ENV DATABASE_URL="postgresql://postgres:postgres@localhost:5432/social_healthspace"
ENV JWT_SECRET_KEY="your-secret-key-here"

# Expose port
EXPOSE ${PORT}

# Healthcheck with more debugging
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD sh -c "echo 'Checking health...' && \
               echo 'Network status:' && netstat -tulpn && \
               echo 'Processes:' && ps aux && \
               curl -v http://localhost:${PORT}/health || exit 1"

# Run the application using the startup script
CMD ["./start.sh"] 