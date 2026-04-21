import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

with patch('redis.Redis') as mock_redis:
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    from main import app

client = TestClient(app)


def test_create_job():
    """POST /jobs should create a job and return a job_id"""
    with patch('main.r') as mock_r:
        mock_r.lpush = MagicMock()
        mock_r.hset = MagicMock()
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()


def test_get_job_found():
    """GET /jobs/{job_id} should return job status when job exists"""
    with patch('main.r') as mock_r:
        mock_r.hget.return_value = b"queued"
        response = client.get("/jobs/test-job-id")
        assert response.status_code == 200
        assert response.json()["status"] == "queued"


def test_get_job_not_found():
    """GET /jobs/{job_id} should return 404 when job does not exist"""
    with patch('main.r') as mock_r:
        mock_r.hget.return_value = None
        response = client.get("/jobs/nonexistent-job")
        assert response.status_code == 404
        assert "error" in response.json()


def test_health_check():
    """GET /health should return healthy status"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_job_returns_unique_ids():
    """POST /jobs should return different job_ids on each call"""
    with patch('main.r') as mock_r:
        mock_r.lpush = MagicMock()
        mock_r.hset = MagicMock()
        response1 = client.post("/jobs")
        response2 = client.post("/jobs")
        assert response1.json()["job_id"] != response2.json()["job_id"]