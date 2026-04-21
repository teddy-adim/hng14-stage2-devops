# HNG Stage 2 — Containerized Job Processing System

A microservices job processing application containerized with Docker and deployed via a full CI/CD pipeline.

## Services

| Service | Technology | Port |
|---|---|---|
| Frontend | Node.js / Express | 3000 |
| API | Python / FastAPI | 8000 |
| Worker | Python | internal only |
| Redis | Redis 7 | internal only |

## Prerequisites

Make sure you have the following installed on your machine:

- Docker v20+
- Docker Compose v2+
- Git

## Getting Started

### 1. Clone the repository

    git clone https://github.com/Teddy-adim/hng14-stage2-devops.git
    cd hng14-stage2-devops

### 2. Set up environment variables

    cp .env.example .env

### 3. Start the full stack

    docker compose up --build

### 4. Verify it is running

You should see the following output in your terminal:

    frontend | Frontend running on port 3000
    api      | INFO: Uvicorn running on http://0.0.0.0:8000

All services start in the correct order:

- Redis starts first
- API and Worker start after Redis is confirmed healthy
- Frontend starts after API is confirmed healthy

### 5. Open the app

Visit http://localhost:3000 in your browser.

Click Submit New Job to create a job. The status updates automatically from queued to completed.

## How It Works

    User clicks Submit
          |
          v
    Frontend POST /submit --> API POST /jobs
          |
          v
    API creates job ID, pushes to Redis queue
          |
          v
    Worker picks job from queue, processes it
          |
          v
    Worker updates job status to completed in Redis
          |
          v
    Frontend polls every 2 seconds until status = completed

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /jobs | Create a new job |
| GET | /jobs/{job_id} | Get job status |
| GET | /health | Health check |

## Stopping the Stack

    docker compose down

To remove all containers and volumes:

    docker compose down -v

## Running Tests Locally

    cd api
    pip install -r requirements.txt
    pip install pytest pytest-cov httpx fakeredis
    pytest tests/ -v

## CI/CD Pipeline

Every push to main triggers the following pipeline stages in order:

    lint --> test --> build --> security scan --> integration test --> deploy

- Lint: flake8 for Python, eslint for JavaScript, hadolint for Dockerfiles
- Test: pytest with Redis mocked, coverage report uploaded as artifact
- Build: Docker images built and tagged with git SHA and latest
- Security Scan: Trivy scans all images for CRITICAL vulnerabilities
- Integration Test: full stack started, real job submitted and verified complete
- Deploy: rolling update with health check verification before old container stops

## Environment Variables

See .env.example for all required variables.

| Variable | Description | Default |
|---|---|---|
| REDIS_HOST | Redis service hostname | redis |
| REDIS_PORT | Redis port | 6379 |
| API_URL | API service URL for frontend | http://api:8000 |

## Bug Fixes

All bugs found in the original source code are documented in FIXES.md.
