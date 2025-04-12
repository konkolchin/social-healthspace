# Use Node.js to build frontend
FROM node:18 AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Backend image
FROM python:3.9-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with verbose output
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -v

# Copy application code
COPY . .

# Copy built frontend from frontend-builder
COPY --from=frontend-builder /frontend/dist /app/frontend/dist

# Set environment variables
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE ${PORT}

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]