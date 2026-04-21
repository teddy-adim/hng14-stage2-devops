# Stage 1 - Builder
# We use this stage to install dependencies only
# This stage will NOT be in the final image
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy only requirements first
# Docker caches this layer - if requirements don't change, pip install is skipped on rebuild
COPY requirements.txt .

# Install dependencies into a separate folder
# This makes it easy to copy just the dependencies to the final stage
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 - Final image
# This is the clean image that actually runs in production
FROM python:3.12-slim

# Create a non-root user for security
# Running as root inside a container is dangerous - if the container is compromised
# the attacker gets root access to the host
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Give appuser ownership of the app files
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Tell Docker this container listens on port 8000
EXPOSE 8000

# Health check - Docker will hit this endpoint every 30 seconds
# If it fails 3 times in a row Docker marks the container as unhealthy
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]