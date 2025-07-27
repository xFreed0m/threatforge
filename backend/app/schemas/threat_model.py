from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class SupportedFileTypes(str, Enum):
    DRAWIO = "drawio"
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    XML = "xml"

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: SupportedFileTypes
    size: int
    upload_date: datetime

class DiagramAnalysisRequest(BaseModel):
    file_id: str
    framework: str = Field(default="STRIDE")

class ThreatModelRequest(BaseModel):
    """Request model for threat modeling generation."""
    content: str = Field(..., description="Text description of the system to analyze")
    framework: str = Field(default="STRIDE", description="Threat modeling framework to use")
    file_id: Optional[str] = Field(default=None, description="Optional file ID if analyzing uploaded diagram")
    llm_provider: Optional[str] = Field(default=None, description="Specific LLM provider to use")

class ThreatModelResponse(BaseModel):
    """Response model for generated threat models."""
    id: str = Field(description="Unique identifier for the threat model")
    threat_model: str = Field(description="The generated threat model content")
    estimated_cost: float = Field(description="Estimated cost of generation")
    provider_used: str = Field(description="LLM provider used for generation")
    framework: str = Field(description="Framework used for analysis")
    content_analyzed: str = Field(description="Content that was analyzed") 