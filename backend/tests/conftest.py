import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope='session', autouse=True)
def set_test_env():
    os.environ['TESTING'] = 'true'
    os.environ['OPENAI_API_KEY'] = 'test-key'
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    yield
    os.environ.pop('TESTING', None)
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ.pop('ANTHROPIC_API_KEY', None)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_llm(monkeypatch):
    class MockLLM:
        async def generate(self, prompt):
            return 'mocked scenario'
        def estimate_cost(self, prompt):
            return 0.0123
    
    # Mock the LLM factory to use the existing MockLLMService
    from app.services.llm_service import MockLLMService
    monkeypatch.setattr('app.services.llm_factory.LLMFactory.create', lambda provider: MockLLMService())
    monkeypatch.setattr('app.services.llm_factory.LLMFactory.get_available_providers', lambda: ['openai', 'anthropic'])
    
    # Mock the job service to return proper responses
    from app.services.job_service import job_service
    original_create_job = job_service.create_job
    
    def mock_create_job(request):
        job_id = "test-job-id-12345"
        # Create a mock job response
        from app.schemas.threat_model import JobStatusResponse, JobStatus
        from datetime import datetime
        job = JobStatusResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            progress=0,
            message="Job created for testing",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        job_service.jobs[job_id] = job
        return job_id
    
    monkeypatch.setattr(job_service, 'create_job', mock_create_job)
    
    return MockLLM() 