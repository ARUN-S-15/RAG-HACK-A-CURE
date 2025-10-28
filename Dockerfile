FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Build vector store with placeholder data
RUN python ingest.py || echo "Warning: Vector store build failed, will use runtime build"

# Expose port
EXPOSE 10000

# Set environment variable for port
ENV PORT=10000

# Command to run the application
CMD ["python", "app.py"]
