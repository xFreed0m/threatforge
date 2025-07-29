import pytest
import asyncio
import tempfile
import time
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.services import file_service
from app.services.job_service import job_service
from app.schemas.threat_model import JobStatus

client = TestClient(app)

@pytest.fixture
def sample_drawio_file():
    """Create a temporary .drawio file for testing."""
    content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="test" name="Test">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="User" style="ellipse;fillColor=#ffcccc;" vertex="1" parent="1">
          <mxGeometry x="80" y="80" width="80" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="Database" style="rounded=1;fillColor=#ccffcc;" vertex="1" parent="1">
          <mxGeometry x="240" y="80" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="4" edge="1" source="2" target="3" style="endArrow=block;strokeColor=#000000;" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.drawio', delete=False) as f:
        f.write(content)
        return f.name

@pytest.fixture(autouse=True)
def cleanup_jobs():
    """Clean up jobs before and after each test."""
    # Clear all jobs before test
    job_service.jobs.clear()
    job_service.cache.clear()
    yield
    # Clear all jobs after test
    job_service.jobs.clear()
    job_service.cache.clear()

def test_create_async_job():
    """Test creating an async threat model generation job."""
    response = client.post("/api/threat-model/generate-async", json={
        "content": "A web application with user authentication",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "job_id" in data
    # Job creation only returns job_id, status is retrieved via separate endpoint

def test_get_job_status():
    """Test getting job status."""
    # Create a job first
    create_response = client.post("/api/threat-model/generate-async", json={
        "content": "Test system description",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    job_id = create_response.json()["job_id"]
    
    # Get job status
    response = client.get(f"/api/threat-model/jobs/{job_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["job_id"] == job_id
    assert "status" in data
    assert "progress" in data
    assert "message" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_nonexistent_job():
    """Test getting status of a job that doesn't exist."""
    response = client.get("/api/threat-model/jobs/nonexistent-id")
    
    assert response.status_code == 404
    assert "Job not found" in response.json()["detail"]

def test_cancel_job():
    """Test cancelling a job."""
    # Create a job first
    create_response = client.post("/api/threat-model/generate-async", json={
        "content": "Test system description",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    job_id = create_response.json()["job_id"]
    
    # Cancel the job immediately
    response = client.delete(f"/api/threat-model/jobs/{job_id}")
    
    # In test environment, job might complete quickly, so we accept either success or not found
    if response.status_code == 200:
        assert "cancelled successfully" in response.json()["detail"]
        # Check that job status is cancelled
        status_response = client.get(f"/api/threat-model/jobs/{job_id}")
        assert status_response.json()["status"] == "cancelled"
    elif response.status_code == 404:
        # Job completed before we could cancel it, which is acceptable in test environment
        status_response = client.get(f"/api/threat-model/jobs/{job_id}")
        assert status_response.json()["status"] in ["completed", "failed"]
    else:
        assert False, f"Unexpected status code: {response.status_code}"

def test_cancel_nonexistent_job():
    """Test cancelling a job that doesn't exist."""
    response = client.delete("/api/threat-model/jobs/nonexistent-id")
    
    assert response.status_code == 400
    assert "Invalid job ID format" in response.json()["detail"]

def test_list_jobs():
    """Test listing jobs."""
    # Create multiple jobs
    for i in range(3):
        client.post("/api/threat-model/generate-async", json={
            "content": f"Test system {i}",
            "framework": "STRIDE",
            "llm_provider": "openai"
        })
    
    # List jobs
    response = client.get("/api/threat-model/jobs")
    
    assert response.status_code == 200
    jobs = response.json()
    
    assert isinstance(jobs, list)
    assert len(jobs) >= 3
    
    # Check job structure
    for job in jobs:
        assert "job_id" in job
        assert "status" in job
        assert "progress" in job
        assert "message" in job
        assert "created_at" in job

def test_list_jobs_with_limit():
    """Test listing jobs with limit parameter."""
    # Create multiple jobs
    for i in range(5):
        client.post("/api/threat-model/generate-async", json={
            "content": f"Test system {i}",
            "framework": "STRIDE",
            "llm_provider": "openai"
        })
    
    # List jobs with limit
    response = client.get("/api/threat-model/jobs?limit=2")
    
    assert response.status_code == 200
    jobs = response.json()
    
    assert len(jobs) <= 2

def test_async_job_with_file(sample_drawio_file):
    """Test async job creation with uploaded file."""
    # Upload a file first
    with open(sample_drawio_file, 'rb') as f:
        upload_response = client.post("/api/threat-model/upload", files={"file": ("test.drawio", f, "application/octet-stream")})
    
    assert upload_response.status_code == 200
    file_data = upload_response.json()
    file_id = file_data["file_id"]
    
    # Create async job with file
    response = client.post("/api/threat-model/generate-async", json={
        "content": "A web application with user authentication and database storage",
        "framework": "STRIDE",
        "file_id": file_id,
        "llm_provider": "openai"
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "job_id" in data
    # Job creation only returns job_id, status is retrieved via separate endpoint
    
    # Cleanup
    Path(sample_drawio_file).unlink()

def test_cache_functionality():
    """Test that identical requests can be processed."""
    # Create first job
    response1 = client.post("/api/threat-model/generate-async", json={
        "content": "Identical test content",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    assert response1.status_code == 200
    job1_data = response1.json()
    
    # Create second identical job
    response2 = client.post("/api/threat-model/generate-async", json={
        "content": "Identical test content",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    assert response2.status_code == 200
    job2_data = response2.json()
    
    # Both jobs should be created successfully
    assert job1_data["job_id"] != job2_data["job_id"]
    
    # Check that both jobs exist and have valid status
    status1_response = client.get(f"/api/threat-model/jobs/{job1_data['job_id']}")
    status2_response = client.get(f"/api/threat-model/jobs/{job2_data['job_id']}")
    
    assert status1_response.status_code == 200
    assert status2_response.status_code == 200
    
    status1_data = status1_response.json()
    status2_data = status2_response.json()
    
    # Both jobs should have valid statuses
    assert status1_data["status"] in ["pending", "processing", "completed", "failed"]
    assert status2_data["status"] in ["pending", "processing", "completed", "failed"]

def test_job_progress_tracking():
    """Test that job progress is tracked properly."""
    # Create a job
    response = client.post("/api/threat-model/generate-async", json={
        "content": "Test system for progress tracking",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    
    # Wait a bit for processing to start
    time.sleep(1)
    
    # Check progress
    status_response = client.get(f"/api/threat-model/jobs/{job_id}")
    data = status_response.json()
    
    assert "progress" in data
    assert isinstance(data["progress"], int)
    assert 0 <= data["progress"] <= 100

def test_job_error_handling():
    """Test job error handling."""
    # Create a job with invalid provider
    response = client.post("/api/threat-model/generate-async", json={
        "content": "Test system",
        "framework": "STRIDE",
        "llm_provider": "invalid-provider"
    })
    
    assert response.status_code == 200  # Job creation succeeds
    job_id = response.json()["job_id"]
    
    # Wait for job to fail
    time.sleep(2)
    
    # Check that job failed
    status_response = client.get(f"/api/threat-model/jobs/{job_id}")
    data = status_response.json()
    
    assert data["status"] == "failed"
    assert "error" in data
    assert data["error"] is not None

def test_cleanup_old_jobs():
    """Test cleanup of old jobs."""
    # Create some jobs
    for i in range(3):
        client.post("/api/threat-model/generate-async", json={
            "content": f"Test system {i}",
            "framework": "STRIDE",
            "llm_provider": "openai"
        })
    
    # Manually mark some jobs as old
    for job_id in list(job_service.jobs.keys())[:2]:
        job_service.jobs[job_id].created_at = job_service.jobs[job_id].created_at.replace(year=2020)
        job_service.jobs[job_id].status = JobStatus.COMPLETED
    
    # Run cleanup
    job_service.cleanup_old_jobs(days=1)
    
    # Check that old jobs are removed
    response = client.get("/api/threat-model/jobs")
    jobs = response.json()
    
    # Should have fewer jobs after cleanup
    assert len(jobs) < 3

def test_cleanup_old_cache():
    """Test cleanup of old cache entries."""
    # Create some cache entries
    for i in range(3):
        client.post("/api/threat-model/generate-async", json={
            "content": f"Cache test {i}",
            "framework": "STRIDE",
            "llm_provider": "openai"
        })
    
    # Manually mark some cache entries as old
    for cache_key in list(job_service.cache.keys())[:2]:
        job_service.cache[cache_key].created_at = job_service.cache[cache_key].created_at.replace(year=2020)
    
    # Run cleanup
    job_service.cleanup_old_cache(days=1)
    
    # Check that old cache entries are removed
    assert len(job_service.cache) < 3 