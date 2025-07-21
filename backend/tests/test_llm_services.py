import pytest
from unittest.mock import patch, MagicMock
from app.services.llm_factory import LLMFactory
from app.services.llm_service import LLMService, LLMProvider

@pytest.fixture
def mock_openai(monkeypatch):
    mock_service = MagicMock(spec=LLMService)
    mock_service.generate.return_value = 'mocked scenario'
    mock_service.estimate_cost.return_value = 0.0123
    monkeypatch.setattr(LLMFactory, 'create', lambda provider: mock_service)
    monkeypatch.setattr(LLMFactory, 'get_available_providers', lambda: [LLMProvider.OPENAI, LLMProvider.ANTHROPIC])
    return mock_service

@pytest.mark.asyncio
async def test_llm_factory_creates_services(mock_openai):
    service = LLMFactory.create(LLMProvider.OPENAI)
    assert isinstance(service, MagicMock)
    service = LLMFactory.create(LLMProvider.ANTHROPIC)
    assert isinstance(service, MagicMock)

@pytest.mark.asyncio
async def test_cost_estimation(mock_openai):
    service = LLMFactory.create(LLMProvider.OPENAI)
    cost = service.estimate_cost('prompt')
    assert isinstance(cost, float)
    assert cost == 0.0123

@pytest.mark.asyncio
async def test_generate_scenario_mocked(mock_openai):
    service = LLMFactory.create(LLMProvider.OPENAI)
    scenario = await service.generate('prompt')
    assert scenario == 'mocked scenario'

@pytest.mark.asyncio
async def test_error_on_missing_api_key(monkeypatch):
    # Simulate missing API key by raising an exception
    monkeypatch.setattr(LLMFactory, 'create', lambda provider: (_ for _ in ()).throw(Exception('Missing API key')))
    with pytest.raises(Exception) as exc:
        LLMFactory.create(LLMProvider.OPENAI)
    assert 'Missing API key' in str(exc.value) 