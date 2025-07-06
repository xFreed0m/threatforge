from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from app.services.llm_service import LLMProvider

class CompanySize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"

class ThreatActor(str, Enum):
    APT = "apt"
    RANSOMWARE = "ransomware"
    INSIDER = "insider"
    HACKTIVIST = "hacktivist"
    CYBERCRIMINAL = "cybercriminal"

class ScenarioRequest(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    industry: str = Field(..., description="Industry sector")
    company_size: CompanySize = Field(..., description="Size of company")
    technologies: List[str] = Field(default=[], description="Key technologies used")
    threat_actor: ThreatActor = Field(..., description="Type of threat actor")
    scenario_type: str = Field(default="ransomware", description="Type of scenario")
    participants: List[str] = Field(default=["Security Team"], description="Exercise participants")
    duration_hours: int = Field(default=2, ge=1, le=8, description="Exercise duration")
    llm_provider: Optional[LLMProvider] = Field(default=None, description="LLM provider to use")

class ScenarioResponse(BaseModel):
    id: str
    scenario: str
    estimated_cost: float
    provider_used: str
    
class CostEstimate(BaseModel):
    provider: str
    estimated_cost: float
