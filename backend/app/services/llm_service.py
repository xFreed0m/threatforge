from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from enum import Enum

class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class LLMService(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def estimate_cost(self, prompt: str, max_tokens: int = 2000) -> float:
        """Estimate cost in USD for the generation"""
        pass
