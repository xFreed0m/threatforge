from openai import AsyncOpenAI
from typing import Optional
from app.services.llm_service import LLMService
from app.core.config import settings

class OpenAIService(LLMService):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.openai_api_key
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"
        
    async def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert creating tabletop exercise scenarios."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI generation failed: {str(e)}")
    
    def estimate_cost(self, prompt: str, max_tokens: int = 2000) -> float:
        # GPT-4 Turbo pricing (as of 2024)
        input_price = 0.01  # per 1K tokens
        output_price = 0.03  # per 1K tokens
        
        # Rough estimation
        prompt_tokens = len(prompt) / 4  # ~4 chars per token
        total_tokens = (prompt_tokens + max_tokens) / 1000
        
        return (prompt_tokens / 1000 * input_price) + (max_tokens / 1000 * output_price)