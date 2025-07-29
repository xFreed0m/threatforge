"""Threat model schemas for request/response models."""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
import re

class SupportedFileTypes(str, Enum):
    """Supported file types for upload."""
    DRAWIO = "drawio"
    PNG = "png"
    JPG = "jpg"
    SVG = "svg"
    XML = "xml"

class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class FileUploadResponse(BaseModel):
    """Response model for file upload."""
    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="File type")
    size: int = Field(..., description="File size in bytes")
    upload_date: datetime = Field(..., description="Upload timestamp")
    content_hash: Optional[str] = Field(None, description="SHA-256 hash of file content")
    file_path: Optional[str] = Field(None, description="Path to stored file")
    
    @field_validator('file_id')
    @classmethod
    def validate_file_id(cls, v):
        if not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid file ID format')
        return v
    
    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v):
        if len(v) > 255:
            raise ValueError('Filename too long')
        if any(char in v for char in ['<', '>', ':', '"', '|', '?', '*', '\\', '/']):
            raise ValueError('Filename contains invalid characters')
        return v
    
    @field_validator('size')
    @classmethod
    def validate_size(cls, v):
        if v <= 0:
            raise ValueError('File size must be positive')
        if v > 10 * 1024 * 1024:  # 10MB
            raise ValueError('File size too large')
        return v

class DiagramAnalysisRequest(BaseModel):
    """Request model for diagram analysis."""
    file_id: str = Field(..., description="File ID to analyze")
    framework: str = Field(default="STRIDE", description="Threat modeling framework")
    
    @field_validator('file_id')
    @classmethod
    def validate_file_id(cls, v):
        if not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid file ID format')
        return v
    
    @field_validator('framework')
    @classmethod
    def validate_framework(cls, v):
        valid_frameworks = ['STRIDE', 'LINDDUN', 'PASTA', 'Attack Trees', 'ATTACK_TREES']
        if v not in valid_frameworks:
            raise ValueError(f'Invalid framework. Must be one of: {", ".join(valid_frameworks)}')
        return v

class ThreatModelRequest(BaseModel):
    """Request model for threat model generation."""
    content: str = Field(..., description="System description or content to analyze")
    framework: str = Field(default="STRIDE", description="Threat modeling framework")
    file_id: Optional[str] = Field(None, description="Optional file ID for diagram analysis")
    llm_provider: Optional[str] = Field(None, description="LLM provider to use")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        if len(v) > 50000:  # 50KB limit
            raise ValueError('Content too long (max 50KB)')
        
        # Check for potentially dangerous content
        dangerous_patterns = [
            r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Content contains potentially dangerous elements')
        
        return v.strip()
    
    @field_validator('framework')
    @classmethod
    def validate_framework(cls, v):
        valid_frameworks = ['STRIDE', 'LINDDUN', 'PASTA', 'Attack Trees']
        if v not in valid_frameworks:
            raise ValueError(f'Invalid framework. Must be one of: {", ".join(valid_frameworks)}')
        return v
    
    @field_validator('file_id')
    @classmethod
    def validate_file_id(cls, v):
        if v is not None and not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid file ID format')
        return v

class ThreatModelResponse(BaseModel):
    """Response model for threat model generation."""
    id: str = Field(..., description="Unique threat model identifier")
    threat_model: str = Field(..., description="Generated threat model content")
    estimated_cost: float = Field(..., description="Estimated cost in USD")
    provider_used: str = Field(..., description="LLM provider used")
    framework: str = Field(..., description="Framework used for analysis")
    content_analyzed: str = Field(..., description="Content that was analyzed")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Generation timestamp")
    processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
    
    @field_validator('id')

    
    @classmethod
    def validate_id(cls, v):
        if not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid ID format')
        return v
    
    @field_validator('estimated_cost')

    
    @classmethod
    def validate_cost(cls, v):
        if v < 0:
            raise ValueError('Cost cannot be negative')
        return round(v, 4)
    
    @field_validator('processing_time_ms')

    
    @classmethod
    def validate_processing_time(cls, v):
        if v is not None and v < 0:
            raise ValueError('Processing time cannot be negative')
        return v

class AsyncThreatModelRequest(BaseModel):
    """Request model for async threat model generation."""
    content: str = Field(..., description="System description or content to analyze")
    framework: str = Field(default="STRIDE", description="Threat modeling framework")
    file_id: Optional[str] = Field(None, description="Optional file ID for diagram analysis")
    llm_provider: Optional[str] = Field(None, description="LLM provider to use")
    priority: str = Field(default="normal", description="Job priority (low, normal, high)")
    
    @field_validator('content')

    
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty')
        if len(v) > 50000:  # 50KB limit
            raise ValueError('Content too long (max 50KB)')
        
        # Check for potentially dangerous content
        dangerous_patterns = [
            r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, v, re.IGNORECASE):
                raise ValueError('Content contains potentially dangerous elements')
        
        return v.strip()
    
    @field_validator('framework')

    
    @classmethod
    def validate_framework(cls, v):
        valid_frameworks = ['STRIDE', 'LINDDUN', 'PASTA', 'Attack Trees', 'ATTACK_TREES']
        if v not in valid_frameworks:
            raise ValueError(f'Invalid framework. Must be one of: {", ".join(valid_frameworks)}')
        return v

    @field_validator('file_id')


    @classmethod
    def validate_file_id(cls, v):
        if v is not None and not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid file ID format')
        return v

    @field_validator('priority')


    @classmethod
    def validate_priority(cls, v):
        valid_priorities = ['low', 'normal', 'high']
        if v not in valid_priorities:
            raise ValueError(f'Invalid priority. Must be one of: {", ".join(valid_priorities)}')
        return v

class JobResponse(BaseModel):
    """Response model for job creation."""
    job_id: str = Field(..., description="Unique job identifier")
    
    @field_validator('job_id')

    
    @classmethod
    def validate_job_id(cls, v):
        if not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid job ID format')
        return v

class JobStatusResponse(BaseModel):
    """Response model for job status."""
    job_id: str = Field(..., description="Unique job identifier")
    status: JobStatus = Field(..., description="Current job status")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    message: str = Field(..., description="Status message")
    created_at: datetime = Field(..., description="Job creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    result: Optional[ThreatModelResponse] = Field(None, description="Job result if completed")
    error: Optional[str] = Field(None, description="Error message if failed")
    processing_time_ms: Optional[int] = Field(None, description="Total processing time")
    
    @field_validator('job_id')

    
    @classmethod
    def validate_job_id(cls, v):
        if not re.match(r'^[a-f0-9\-]+$', v):
            raise ValueError('Invalid job ID format')
        return v
    
    @field_validator('progress')

    
    @classmethod
    def validate_progress(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Progress must be between 0 and 100')
        return v
    
    @field_validator('processing_time_ms')

    
    @classmethod
    def validate_processing_time(cls, v):
        if v is not None and v < 0:
            raise ValueError('Processing time cannot be negative')
        return v

class CacheEntry(BaseModel):
    """Model for cache entries."""
    cache_key: str = Field(..., description="Cache key")
    threat_model: ThreatModelResponse = Field(..., description="Cached threat model")
    created_at: datetime = Field(..., description="Cache entry creation time")
    access_count: int = Field(default=1, ge=0, description="Number of times accessed")
    last_accessed: datetime = Field(..., description="Last access time")
    expires_at: Optional[datetime] = Field(None, description="Expiration time")
    
    @field_validator('access_count')

    
    @classmethod
    def validate_access_count(cls, v):
        if v < 0:
            raise ValueError('Access count cannot be negative')
        return v

class ThreatModelMetadata(BaseModel):
    """Metadata for threat model analysis."""
    system_name: Optional[str] = Field(None, description="Name of the analyzed system")
    analysis_date: datetime = Field(default_factory=datetime.utcnow, description="Analysis date")
    analyst: Optional[str] = Field(None, description="Name of the analyst")
    version: str = Field(default="1.0", description="Analysis version")
    tags: List[str] = Field(default_factory=list, description="Analysis tags")
    notes: Optional[str] = Field(None, description="Additional notes")
    
    @field_validator('system_name')

    
    @classmethod
    def validate_system_name(cls, v):
        if v is not None and len(v) > 100:
            raise ValueError('System name too long (max 100 characters)')
        return v
    
    @field_validator('analyst')

    
    @classmethod
    def validate_analyst(cls, v):
        if v is not None and len(v) > 50:
            raise ValueError('Analyst name too long (max 50 characters)')
        return v
    
    @field_validator('tags')

    
    @classmethod
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError('Too many tags (max 10)')
        for tag in v:
            if len(tag) > 20:
                raise ValueError('Tag too long (max 20 characters)')
        return v

class ThreatModelExport(BaseModel):
    """Model for threat model export configuration."""
    format: str = Field(..., description="Export format (pdf, docx, json, html)")
    include_metadata: bool = Field(default=True, description="Include metadata in export")
    include_diagrams: bool = Field(default=True, description="Include diagrams in export")
    include_recommendations: bool = Field(default=True, description="Include recommendations")
    template: Optional[str] = Field(None, description="Custom template to use")
    language: str = Field(default="en", description="Export language")
    
    @field_validator('format')

    
    @classmethod
    def validate_format(cls, v):
        valid_formats = ['pdf', 'docx', 'json', 'html', 'markdown']
        if v not in valid_formats:
            raise ValueError(f'Invalid format. Must be one of: {", ".join(valid_formats)}')
        return v
    
    @field_validator('language')

    
    @classmethod
    def validate_language(cls, v):
        if not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', v):
            raise ValueError('Invalid language code format')
        return v 