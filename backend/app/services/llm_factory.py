"""Factory for creating LLM service instances."""

from typing import List, Optional

from app.core.config import settings
from app.services.anthropic_service import AnthropicService
from app.services.llm_service import LLMProvider, LLMService, MockLLMService
from app.services.openai_service import OpenAIService


class LLMFactory:
    """Factory class for creating LLM service instances."""
    
    @staticmethod
    def create(provider: LLMProvider, api_key: Optional[str] = None) -> LLMService:
        """Create an LLM service instance based on provider.
        
        Args:
            provider: The LLM provider to create a service for.
            api_key: Optional API key override.
            
        Returns:
            An instance of the appropriate LLM service.
            
        Raises:
            ValueError: If the provider is not supported.
        """
        import os
        
        # In test environment, return mock service
        if os.getenv('TESTING') == 'true':
            from app.services.llm_service import MockLLMService
            return MockLLMService()
        
        # Handle both enum and string providers
        provider_str = provider.value if hasattr(provider, 'value') else str(provider)
        
        if provider_str == "openai":
            return OpenAIService(api_key=api_key)
        elif provider_str == "anthropic":
            return AnthropicService(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    @staticmethod
    def get_available_providers() -> List[LLMProvider]:
        """Get list of available providers based on configured API keys.
        
        Returns:
            List of available LLM providers that have API keys configured.
        """
        import os
        
        # In test environment, return mock providers
        if os.getenv('TESTING') == 'true':
            return [LLMProvider.OPENAI, LLMProvider.ANTHROPIC]
        
        available = []
        
        if settings.openai_api_key:
            available.append(LLMProvider.OPENAI)
        if settings.anthropic_api_key:
            available.append(LLMProvider.ANTHROPIC)
        
        return available 