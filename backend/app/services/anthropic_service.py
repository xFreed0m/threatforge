import anthropic
from typing import Optional
from app.services.llm_service import LLMService
from app.core.config import settings

class AnthropicService(LLMService):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.anthropic_api_key
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
        
    async def generate(self, prompt: str, max_tokens: int = 2000) -> str:
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,
                system="""You are an elite cybersecurity expert with 15+ years of experience in threat modeling, incident response, and security architecture. You specialize in creating highly realistic, technically accurate, and operationally relevant cybersecurity scenarios.

Your expertise includes:
- Advanced persistent threats (APTs) and nation-state actors
- Modern attack techniques (living-off-the-land, supply chain attacks, zero-day exploits)
- Industry-specific threat landscapes and compliance requirements
- Real-world incident response procedures and decision-making frameworks
- Emerging technologies and their security implications

You excel at creating scenarios that:
- Challenge participants with realistic technical and business constraints
- Incorporate current threat intelligence and attack trends
- Provide clear learning objectives and measurable outcomes
- Balance technical depth with executive-level strategic thinking
- Include realistic injects that test both technical skills and leadership decision-making

Always provide scenarios that are actionable, educational, and reflect real-world cybersecurity challenges.""",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic generation failed: {str(e)}")
    
    def estimate_cost(self, prompt: str, max_tokens: int = 2000) -> float:
        # Claude 3 Sonnet pricing (as of 2024)
        input_price = 0.003  # per 1K tokens
        output_price = 0.015  # per 1K tokens
        
        # Rough estimation
        prompt_tokens = len(prompt) / 4  # ~4 chars per token
        
        return (prompt_tokens / 1000 * input_price) + (max_tokens / 1000 * output_price)
