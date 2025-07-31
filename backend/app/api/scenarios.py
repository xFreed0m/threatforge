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
    
    return f"""# ELITE CYBERSECURITY TABLETOP EXERCISE SCENARIO

## EXECUTIVE SUMMARY
Create a world-class, technically sophisticated cybersecurity tabletop exercise scenario that challenges participants at the highest level while remaining operationally realistic.

## ORGANIZATION PROFILE
- **Company Name**: {request.company_name}
- **Industry**: {request.industry}
- **Organization Size**: {request.company_size.value}
- **Technology Stack**: {', '.join(request.technologies) if request.technologies else 'Standard IT infrastructure'}
- **Threat Actor Profile**: {request.threat_actor.value}
- **Scenario Type**: {request.scenario_type}
- **Exercise Participants**: {', '.join(request.participants)}
- **Exercise Duration**: {request.duration_hours} hours

## SCENARIO REQUIREMENTS

### 1. THREAT ACTOR INTELLIGENCE
- **Actor Profile**: Detailed analysis of the threat actor's capabilities, motivations, and historical TTPs
- **Attack Infrastructure**: Realistic command & control infrastructure, tools, and techniques
- **Timeline**: Sophisticated attack timeline with multiple phases and escalation points
- **Objectives**: Clear strategic and tactical objectives aligned with the threat actor type

### 2. INITIAL COMPROMISE VECTOR
- **Entry Point**: Realistic initial access method (phishing, supply chain, zero-day, etc.)
- **Technical Details**: Specific vulnerabilities, exploits, and attack chains
- **Indicators of Compromise (IoCs)**: Observable artifacts and behavioral patterns
- **Evasion Techniques**: How the attacker avoids detection initially

### 3. ATTACK PROGRESSION & ESCALATION
- **Lateral Movement**: Realistic internal reconnaissance and privilege escalation
- **Persistence Mechanisms**: How the attacker maintains access
- **Data Exfiltration**: Methods and targets for data theft
- **Impact Escalation**: How the attack affects business operations

### 4. CRITICAL DECISION POINTS
- **Technical Decisions**: Incident response, containment, and eradication choices
- **Business Decisions**: Communication, legal, and operational continuity decisions
- **Leadership Decisions**: Executive-level strategic choices and resource allocation
- **External Coordination**: Law enforcement, vendors, and public relations decisions

### 5. REALISTIC INJECTS & EVENTS
- **Technical Injects**: System alerts, log anomalies, network traffic patterns
- **Business Injects**: Customer complaints, regulatory inquiries, media attention
- **Operational Injects**: System outages, data breaches, ransomware demands
- **Timing**: Realistic timing for each inject based on real-world incident timelines

### 6. LEARNING OBJECTIVES & OUTCOMES
- **Technical Skills**: Specific cybersecurity skills to be tested and developed
- **Leadership Skills**: Decision-making, communication, and crisis management
- **Process Improvement**: Incident response procedures and playbook validation
- **Team Dynamics**: Cross-functional collaboration and communication

### 7. REAL-WORLD CONTEXT
- **Industry-Specific Threats**: Threats relevant to the organization's industry
- **Regulatory Implications**: Compliance requirements and legal considerations
- **Stakeholder Impact**: Effects on customers, partners, and shareholders
- **Market Consequences**: Competitive and reputational implications

## DELIVERABLE FORMAT

Structure your response with these sections:
1. **Scenario Overview** - Executive summary and key objectives
2. **Threat Actor Intelligence** - Detailed actor profile and capabilities
3. **Attack Timeline** - Phase-by-phase progression with realistic timing
4. **Technical Details** - Specific vulnerabilities, tools, and techniques
5. **Decision Points** - Critical junctures requiring participant decisions
6. **Injects Schedule** - Timed events and information releases
7. **Expected Outcomes** - Learning objectives and success metrics
8. **Debriefing Guide** - Key discussion points and lessons learned

Ensure the scenario is technically accurate, operationally realistic, and provides genuine learning value for all participant roles."""


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
            "form_data": request.model_dump(),
        })
        return ScenarioResponse(
            id=scenario_id,
            scenario=scenario,
            estimated_cost=cost,
            provider_used=provider if isinstance(provider, str) else provider.value
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
                    provider=provider if isinstance(provider, str) else provider.value,
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
    import os
    if os.getenv('TESTING') == 'true':
        providers = ["openai", "anthropic"]
    else:
        providers = [p.value for p in LLMFactory.get_available_providers()]
    return {
        "providers": providers
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
            f"""# ELITE SCENARIO SECTION REGENERATION

## EXECUTIVE SUMMARY
You are a world-class cybersecurity tabletop exercise designer with 15+ years of experience in creating sophisticated, realistic, and educationally valuable scenarios. You specialize in crafting scenarios that challenge participants at the highest levels while maintaining operational realism.

## TASK REQUIREMENTS
Regenerate ONLY the section titled '{request.section_title}' within the existing scenario framework.

## CONTEXT & CONSTRAINTS

### Original Scenario Parameters:
{request.context}

### Complete Scenario Context:
{request.original_scenario}

### Current Section Content (to be improved):
{request.section_title}:
{request.section_content}

## REGENERATION REQUIREMENTS

### 1. QUALITY STANDARDS
- **Technical Accuracy**: Ensure all technical details are current and accurate
- **Operational Realism**: Maintain realistic business and technical constraints
- **Educational Value**: Provide genuine learning opportunities for participants
- **Engagement**: Create compelling and challenging content that holds attention

### 2. CONTENT ENHANCEMENT
- **Depth**: Add sophisticated technical and strategic elements
- **Realism**: Incorporate current threat intelligence and attack trends
- **Complexity**: Introduce realistic challenges and decision points
- **Clarity**: Maintain clear, actionable information despite increased complexity

### 3. CONSISTENCY REQUIREMENTS
- **Style**: Match the tone, format, and structure of the original scenario
- **Context**: Maintain consistency with all other sections and parameters
- **Timeline**: Ensure temporal consistency with the overall scenario flow
- **Characterization**: Keep threat actors, organizations, and events consistent

### 4. SECTION-SPECIFIC ENHANCEMENTS

#### For Technical Sections:
- Include specific tools, techniques, and procedures (TTPs)
- Add realistic indicators of compromise (IoCs)
- Incorporate current vulnerability information
- Provide technical depth while maintaining accessibility

#### For Strategic Sections:
- Include business impact considerations
- Add stakeholder communication requirements
- Incorporate regulatory and compliance implications
- Address executive-level decision-making challenges

#### For Operational Sections:
- Include realistic resource constraints
- Add time pressure and urgency elements
- Incorporate cross-functional coordination requirements
- Address real-world operational challenges

## DELIVERABLE REQUIREMENTS

1. **Return ONLY** the regenerated content for the '{request.section_title}' section
2. **Maintain** the exact same formatting and structure as the original
3. **Enhance** the content with more sophisticated, realistic, and valuable elements
4. **Ensure** seamless integration with the rest of the scenario
5. **Provide** actionable, educational, and challenging content

## QUALITY ASSURANCE
- Verify technical accuracy and current relevance
- Ensure operational realism and business context
- Confirm educational value and learning objectives
- Validate consistency with overall scenario framework

Focus on creating content that elevates the entire exercise to world-class standards while maintaining perfect integration with the existing scenario structure."""
        )
        new_section = await service.generate(prompt)
        return {"section_title": request.section_title, "new_content": new_section}
    except Exception as e:
        logger.exception(f"Error rerolling section: {e}")
        raise HTTPException(status_code=500, detail=str(e))
