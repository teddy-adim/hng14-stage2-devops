# Stage 1 - Builder
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json .

# Install dependencies
RUN npm ci --only=production

# Stage 2 - Final image
FROM node:20-alpine

# Create non-root user
RUN adduser -D appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy application code
COPY . .

# Give appuser ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "app.js"]