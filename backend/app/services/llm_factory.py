from typing import Optional
from app.services.llm_service import LLMService, LLMProvider
from app.services.openai_service import OpenAIService
from app.services.anthropic_service import AnthropicService
from app.core.config import settings

class LLMFactory:
    @staticmethod
    def create(provider: LLMProvider, api_key: Optional[str] = None) -> LLMService:
        """Create an LLM service instance based on provider"""
        
        if provider == LLMProvider.OPENAI:
            return OpenAIService(api_key=api_key)
        elif provider == LLMProvider.ANTHROPIC:
            return AnthropicService(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    @staticmethod
    def get_available_providers() -> list[LLMProvider]:
        """Get list of available providers based on configured API keys"""
        available = []
        
        if settings.openai_api_key:
            available.append(LLMProvider.OPENAI)
        if settings.anthropic_api_key:
            available.append(LLMProvider.ANTHROPIC)
            
        return available
