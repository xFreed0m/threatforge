"""Pydantic models for scenario-related data structures."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from app.services.llm_service import LLMProvider


class CompanySize(str, Enum):
    """Company size enumeration."""
    
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class ThreatActor(str, Enum):
    """Threat actor types enumeration."""
    
    APT = "apt"
    RANSOMWARE = "ransomware"
    INSIDER = "insider"
    HACKTIVIST = "hacktivist"
    CYBERCRIMINAL = "cybercriminal"
    COMPETITOR = "competitor"


class ScenarioRequest(BaseModel):
    """Request model for scenario generation."""
    
    company_name: str = Field(
        ..., 
        description="Name of the target company for the scenario"
    )
    industry: str = Field(
        ..., 
        description="Industry sector of the company"
    )
    company_size: CompanySize = Field(
        ..., 
        description="Size classification of the company"
    )
    technologies: List[str] = Field(
        default=[], 
        description="Key technologies and systems used by the company"
    )
    threat_actor: ThreatActor = Field(
        ..., 
        description="Type of threat actor to simulate"
    )
    scenario_type: str = Field(
        default="ransomware", 
        description="Type of cybersecurity incident scenario"
    )
    participants: List[str] = Field(
        default=["Security Team"], 
        description="Roles and teams participating in the exercise"
    )
    duration_hours: int = Field(
        default=2, 
        ge=1, 
        le=8, 
        description="Duration of the exercise in hours"
    )
    llm_provider: Optional[LLMProvider] = Field(
        default=None, 
        description="Specific LLM provider to use for generation"
    )


class ScenarioResponse(BaseModel):
    """Response model for generated scenarios."""
    
    id: str = Field(description="Unique identifier for the scenario")
    scenario: str = Field(description="The generated scenario content")
    estimated_cost: float = Field(description="Estimated cost of generation")
    provider_used: str = Field(description="LLM provider used for generation")


class CostEstimate(BaseModel):
    """Model for cost estimation per provider."""
    
    provider: str = Field(description="Name of the LLM provider")
    estimated_cost: float = Field(description="Estimated cost for this provider")


class RerollSectionRequest(BaseModel):
    original_scenario: str = Field(..., description="The full original scenario text")
    section_title: str = Field(..., description="Title of the section to regenerate")
    section_content: str = Field(..., description="Current content of that section")
    context: dict = Field(..., description="Original form data/context for scenario generation")
    llm_provider: Optional[LLMProvider] = Field(default=None, description="LLM provider to use")
