"""Abstract base classes and enums for LLM services."""

from abc import ABC, abstractmethod
from enum import Enum


class LLMProvider(str, Enum):
    """Enumeration of supported LLM providers."""
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMService(ABC):
    """Abstract base class for LLM providers.
    
    This class defines the interface that all LLM service implementations
    must follow for text generation and cost estimation.
    """
    
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate text from a prompt.
        
        Args:
            prompt: The input prompt for text generation.
            max_tokens: Maximum number of tokens to generate.
            
        Returns:
            The generated text response.
            
        Raises:
            Exception: If generation fails.
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, prompt: str, max_tokens: int = 2000) -> float:
        """Estimate cost in USD for the generation.
        
        Args:
            prompt: The input prompt for cost estimation.
            max_tokens: Maximum number of tokens to estimate for.
            
        Returns:
            Estimated cost in USD.
        """
        pass
