import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope='session', autouse=True)
def set_test_env():
    os.environ['OPENAI_API_KEY'] = 'test-key'
    os.environ['ANTHROPIC_API_KEY'] = 'test-key'
    yield
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
    monkeypatch.setattr('app.services.llm_factory.LLMFactory.create', lambda provider: MockLLM())
    monkeypatch.setattr('app.services.llm_factory.LLMFactory.get_available_providers', lambda: ['openai', 'anthropic'])
    return MockLLM() 