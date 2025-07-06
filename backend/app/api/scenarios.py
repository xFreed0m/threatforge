from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from app.schemas.scenario import ScenarioRequest, ScenarioResponse, CostEstimate
from app.services.llm_factory import LLMFactory, LLMProvider
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])

def build_prompt(request: ScenarioRequest) -> str:
    """Build the prompt for scenario generation"""
    return f"""Create a detailed cybersecurity tabletop exercise scenario with the following parameters:

Company: {request.company_name}
Industry: {request.industry}
Size: {request.company_size.value}
Technologies: {', '.join(request.technologies) if request.technologies else 'Standard IT infrastructure'}
Threat Actor: {request.threat_actor.value}
Scenario Type: {request.scenario_type}
Participants: {', '.join(request.participants)}
Duration: {request.duration_hours} hours

Please create a realistic scenario that includes:
1. Initial compromise details
2. Attack progression timeline
3. Key decision points for participants
4. Injects (events that occur during exercise)
5. Expected outcomes and lessons learned

Format the response in clear sections."""

@router.post("/generate", response_model=ScenarioResponse)
async def generate_scenario(request: ScenarioRequest):
    """Generate a new tabletop exercise scenario"""
    
    # Get available providers
    available_providers = LLMFactory.get_available_providers()
    if not available_providers:
        raise HTTPException(status_code=500, detail="No LLM providers configured")
    
    # Select provider
    provider = request.llm_provider or available_providers[0]
    if provider not in available_providers:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not available")
    
    # Create service and generate
    try:
        service = LLMFactory.create(provider)
        prompt = build_prompt(request)
        scenario = await service.generate(prompt)
        cost = service.estimate_cost(prompt)
        
        return ScenarioResponse(
            id=str(uuid.uuid4()),
            scenario=scenario,
            estimated_cost=cost,
            provider_used=provider.value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/estimate-cost", response_model=List[CostEstimate])
async def estimate_cost(request: ScenarioRequest):
    """Estimate generation cost for all available providers"""
    
    available_providers = LLMFactory.get_available_providers()
    if not available_providers:
        raise HTTPException(status_code=500, detail="No LLM providers configured")
    
    estimates = []
    prompt = build_prompt(request)
    
    for provider in available_providers:
        try:
            service = LLMFactory.create(provider)
            cost = service.estimate_cost(prompt)
            estimates.append(CostEstimate(
                provider=provider.value,
                estimated_cost=cost
            ))
        except Exception:
            continue
    
    return estimates

@router.get("/providers")
async def get_providers():
    """Get available LLM providers"""
    return {
        "providers": [p.value for p in LLMFactory.get_available_providers()]
    }
