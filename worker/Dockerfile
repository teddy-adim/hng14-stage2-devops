# Stage 1 - Builder
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 - Final image
FROM python:3.12-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Give appuser ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check - checks if the worker process is running
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import redis, os; r = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=int(os.getenv('REDIS_PORT', 6379))); r.ping()"

CMD ["python", "worker.py"]