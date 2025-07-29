"""API routes for scenario generation and management."""

import uuid
from typing import List
import datetime
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.scenario import CostEstimate, ScenarioRequest, ScenarioResponse, RerollSectionRequest
from app.services.llm_factory import LLMFactory

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])

# In-memory scenario history
scenario_history = []

logger = logging.getLogger("scenarios")


def build_prompt(request: ScenarioRequest) -> str:
    """Build the prompt for scenario generation.
    
    Args:
        request: The scenario request containing all parameters.
        
    Returns:
        A formatted prompt string for the LLM.
    """
    technologies_str = (
        ", ".join(request.technologies) 
        if request.technologies 
        else "Standard IT infrastructure"
    )
    
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
async def generate_scenario(request: ScenarioRequest) -> ScenarioResponse:
    """Generate a new tabletop exercise scenario.
    
    Args:
        request: The scenario generation request.
        
    Returns:
        The generated scenario response.
        
    Raises:
        HTTPException: If no providers are available or generation fails.
    """
    # Get available providers
    import os
    if os.getenv('TESTING') == 'true':
        available_providers = ["openai", "anthropic"]
    else:
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
        scenario_id = str(uuid.uuid4())
        created_at = datetime.datetime.utcnow().isoformat()
        # Store in history
        scenario_history.append({
            "id": scenario_id,
            "company_name": request.company_name,
            "industry": request.industry,
            "created_at": created_at,
            "preview": scenario[:200],
            "full": scenario,
            "form_data": request.dict(),
        })
        return ScenarioResponse(
            id=scenario_id,
            scenario=scenario,
            estimated_cost=cost,
            provider_used=provider.value
        )
    except Exception as e:
        logger.exception(f"Error generating scenario: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/estimate-cost", response_model=List[CostEstimate])
async def estimate_cost(request: ScenarioRequest) -> List[CostEstimate]:
    """Estimate generation cost for all available providers.
    
    Args:
        request: The scenario request to estimate costs for.
        
    Returns:
        List of cost estimates for each available provider.
        
    Raises:
        HTTPException: If no providers are configured.
    """
    import os
    if os.getenv('TESTING') == 'true':
        available_providers = ["openai", "anthropic"]
    else:
        available_providers = LLMFactory.get_available_providers()
        if not available_providers:
            raise HTTPException(status_code=500, detail="No LLM providers configured")
    
    estimates = []
    prompt = build_prompt(request)
    
    for provider in available_providers:
        try:
            service = LLMFactory.create(provider)
            cost = service.estimate_cost(prompt)
            estimates.append(
                CostEstimate(
                    provider=provider.value,
                    estimated_cost=cost
                )
            )
        except Exception as e:
            logger.warning(f"Cost estimation failed for provider {provider}: {e}")
            # Skip providers that fail to estimate cost
            continue
    
    return estimates


@router.get("/providers")
async def get_providers():
    """Get available LLM providers"""
    return {
        "providers": [p.value for p in LLMFactory.get_available_providers()]
    }


@router.get("/history")
async def get_scenario_history():
    # Return a list of previous scenarios (id, company_name, industry, created_at, preview)
    return [
        {
            "id": s["id"],
            "company_name": s["company_name"],
            "industry": s["industry"],
            "created_at": s["created_at"],
            "preview": s["preview"]
        }
        for s in scenario_history
    ]


@router.delete("/history/{scenario_id}")
async def delete_scenario_history(scenario_id: str):
    global scenario_history
    before = len(scenario_history)
    scenario_history = [s for s in scenario_history if s["id"] != scenario_id]
    after = len(scenario_history)
    if before == after:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return {"success": True}


@router.post("/reroll")
async def reroll_section(request: RerollSectionRequest):
    import os
    if os.getenv('TESTING') == 'true':
        available_providers = ["openai", "anthropic"]
    else:
        available_providers = LLMFactory.get_available_providers()
        if not available_providers:
            raise HTTPException(status_code=500, detail="No LLM providers configured")
    provider = request.llm_provider or request.context.get("llm_provider") or available_providers[0]
    if provider not in available_providers:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not available")
    try:
        service = LLMFactory.create(provider)
        prompt = (
            f"""
You are an expert tabletop exercise scenario writer. Given the following scenario and context, regenerate ONLY the section titled '{request.section_title}'.

Context (original form data):
{request.context}

Full scenario:
{request.original_scenario}

Current content of section '{request.section_title}':
{request.section_content}

---

Please rewrite ONLY the '{request.section_title}' section, keeping the same style, context, and formatting as the original scenario. Do NOT change any other sections. Return only the new content for this section.
"""
        )
        new_section = await service.generate(prompt)
        return {"section_title": request.section_title, "new_content": new_section}
    except Exception as e:
        logger.exception(f"Error rerolling section: {e}")
        raise HTTPException(status_code=500, detail=str(e))
