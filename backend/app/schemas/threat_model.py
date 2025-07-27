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

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

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

class AsyncThreatModelRequest(BaseModel):
    """Request model for async threat modeling generation."""
    content: str = Field(..., description="Text description of the system to analyze")
    framework: str = Field(default="STRIDE", description="Threat modeling framework to use")
    file_id: Optional[str] = Field(default=None, description="Optional file ID if analyzing uploaded diagram")
    llm_provider: Optional[str] = Field(default=None, description="Specific LLM provider to use")
    cache_key: Optional[str] = Field(default=None, description="Optional cache key for similar requests")

class JobResponse(BaseModel):
    """Response model for async job submission."""
    job_id: str = Field(description="Unique job identifier")
    status: JobStatus = Field(description="Current job status")
    message: str = Field(description="Status message")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion time")

class JobStatusResponse(BaseModel):
    """Response model for job status queries."""
    job_id: str = Field(description="Job identifier")
    status: JobStatus = Field(description="Current job status")
    progress: int = Field(description="Progress percentage (0-100)")
    message: str = Field(description="Current status message")
    result: Optional[ThreatModelResponse] = Field(default=None, description="Job result if completed")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    created_at: datetime = Field(description="Job creation time")
    updated_at: datetime = Field(description="Last update time")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion time")

class CacheEntry(BaseModel):
    """Model for cached threat model results."""
    cache_key: str = Field(description="Unique cache key")
    threat_model: ThreatModelResponse = Field(description="Cached threat model")
    created_at: datetime = Field(description="Cache creation time")
    access_count: int = Field(default=0, description="Number of times accessed")
    last_accessed: datetime = Field(description="Last access time") 