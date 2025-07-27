"""Service for managing async threat model generation jobs."""

import asyncio
import uuid
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from threading import Lock

from app.schemas.threat_model import (
    JobStatus, JobStatusResponse, ThreatModelResponse, 
    AsyncThreatModelRequest, CacheEntry
)
from app.services.llm_factory import LLMFactory
from app.services import file_service
import logging

logger = logging.getLogger("job_service")

class JobService:
    """Service for managing async threat model generation jobs."""
    
    def __init__(self):
        self.jobs: Dict[str, JobStatusResponse] = {}
        self.cache: Dict[str, CacheEntry] = {}
        self.jobs_lock = Lock()
        self.cache_lock = Lock()
        
    def _generate_cache_key(self, request: AsyncThreatModelRequest) -> str:
        """Generate a cache key based on request parameters."""
        # Create a hash of the request content and parameters
        content = f"{request.content}:{request.framework}:{request.file_id}:{request.llm_provider}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_file_content(self, file_id: Optional[str]) -> Optional[str]:
        """Get file content if file_id is provided."""
        if not file_id:
            return None
            
        meta = file_service.db_files.get(file_id)
        if not meta:
            return None
            
        if meta.file_type in ("drawio", "xml"):
            return f"Diagram file: {meta.filename} (type: {meta.file_type})"
        else:
            return f"Image file: {meta.filename} (type: {meta.file_type})"
    
    def _build_prompt(self, request: AsyncThreatModelRequest, file_content: Optional[str] = None) -> str:
        """Build the prompt for threat modeling generation."""
        content_to_analyze = request.content
        if file_content:
            content_to_analyze = f"Diagram Content:\n{file_content}\n\nAdditional Context:\n{request.content}"
        
        return f"""You are a cybersecurity expert performing threat modeling analysis. 

Please analyze the following system using the {request.framework} framework:

{content_to_analyze}

Generate a comprehensive threat model that includes:

1. **System Overview**: Brief description of the system being analyzed
2. **Asset Identification**: Key assets, data, and components
3. **Threat Actors**: Potential attackers and their motivations
4. **Threat Analysis**: For each asset, identify potential threats using {request.framework}:
   - Spoofing: Authentication/identity threats
   - Tampering: Data integrity threats  
   - Repudiation: Non-repudiation threats
   - Information Disclosure: Confidentiality threats
   - Denial of Service: Availability threats
   - Elevation of Privilege: Authorization threats
5. **Risk Assessment**: Rate each threat (High/Medium/Low) based on likelihood and impact
6. **Mitigation Strategies**: Recommended controls and countermeasures
7. **Security Recommendations**: Overall security posture improvements

Format the response in clear sections with actionable insights."""
    
    def create_job(self, request: AsyncThreatModelRequest) -> str:
        """Create a new async job for threat model generation."""
        job_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Check cache first
        cache_key = request.cache_key or self._generate_cache_key(request)
        with self.cache_lock:
            if cache_key in self.cache:
                # Return cached result immediately
                cached_entry = self.cache[cache_key]
                cached_entry.access_count += 1
                cached_entry.last_accessed = now
                
                # Create a completed job with cached result
                job = JobStatusResponse(
                    job_id=job_id,
                    status=JobStatus.COMPLETED,
                    progress=100,
                    message="Result retrieved from cache",
                    result=cached_entry.threat_model,
                    created_at=now,
                    updated_at=now
                )
                with self.jobs_lock:
                    self.jobs[job_id] = job
                return job_id
        
        # Create new job
        job = JobStatusResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            progress=0,
            message="Job created, waiting to start",
            created_at=now,
            updated_at=now,
            estimated_completion=now + timedelta(minutes=5)  # Rough estimate
        )
        
        with self.jobs_lock:
            self.jobs[job_id] = job
        
        # Start async processing
        asyncio.create_task(self._process_job(job_id, request, cache_key))
        
        return job_id
    
    async def _process_job(self, job_id: str, request: AsyncThreatModelRequest, cache_key: str):
        """Process a threat model generation job asynchronously."""
        try:
            # Update status to processing
            self._update_job_status(job_id, JobStatus.PROCESSING, 10, "Starting threat model generation...")
            
            # Get available providers
            available_providers = LLMFactory.get_available_providers()
            if not available_providers:
                raise Exception("No LLM providers configured")
            
            # Select provider
            provider = request.llm_provider or available_providers[0]
            if provider not in available_providers:
                raise Exception(f"Provider {provider} not available")
            
            self._update_job_status(job_id, JobStatus.PROCESSING, 20, f"Using {provider} provider...")
            
            # Get file content if provided
            file_content = self._get_file_content(request.file_id)
            if file_content:
                self._update_job_status(job_id, JobStatus.PROCESSING, 30, "Processing uploaded diagram...")
            
            # Build prompt
            prompt = self._build_prompt(request, file_content)
            self._update_job_status(job_id, JobStatus.PROCESSING, 40, "Building analysis prompt...")
            
            # Create service and generate
            service = LLMFactory.create(provider)
            self._update_job_status(job_id, JobStatus.PROCESSING, 50, "Generating threat model with AI...")
            
            threat_model = await service.generate(prompt)
            cost = service.estimate_cost(prompt)
            
            self._update_job_status(job_id, JobStatus.PROCESSING, 80, "Finalizing threat model...")
            
            # Create result
            result = ThreatModelResponse(
                id=str(uuid.uuid4()),
                threat_model=threat_model,
                estimated_cost=cost,
                provider_used=provider,
                framework=request.framework,
                content_analyzed=request.content
            )
            
            # Cache the result
            with self.cache_lock:
                self.cache[cache_key] = CacheEntry(
                    cache_key=cache_key,
                    threat_model=result,
                    created_at=datetime.now(),
                    access_count=1,
                    last_accessed=datetime.now()
                )
            
            # Complete the job
            self._update_job_status(job_id, JobStatus.COMPLETED, 100, "Threat model generation completed", result=result)
            
        except Exception as e:
            logger.exception(f"Error processing job {job_id}: {e}")
            self._update_job_status(job_id, JobStatus.FAILED, 0, f"Job failed: {str(e)}", error=str(e))
    
    def _update_job_status(self, job_id: str, status: JobStatus, progress: int, message: str, 
                          result: Optional[ThreatModelResponse] = None, error: Optional[str] = None):
        """Update job status and progress."""
        with self.jobs_lock:
            if job_id in self.jobs:
                job = self.jobs[job_id]
                job.status = status
                job.progress = progress
                job.message = message
                job.updated_at = datetime.now()
                if result:
                    job.result = result
                if error:
                    job.error = error
    
    def get_job_status(self, job_id: str) -> Optional[JobStatusResponse]:
        """Get the status of a job."""
        with self.jobs_lock:
            return self.jobs.get(job_id)
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending or processing job."""
        with self.jobs_lock:
            if job_id in self.jobs:
                job = self.jobs[job_id]
                if job.status in [JobStatus.PENDING, JobStatus.PROCESSING]:
                    job.status = JobStatus.CANCELLED
                    job.message = "Job cancelled by user"
                    job.updated_at = datetime.now()
                    return True
        return False
    
    def list_jobs(self, limit: int = 50) -> List[JobStatusResponse]:
        """List recent jobs."""
        with self.jobs_lock:
            jobs = list(self.jobs.values())
            jobs.sort(key=lambda x: x.created_at, reverse=True)
            return jobs[:limit]
    
    def cleanup_old_jobs(self, days: int = 7):
        """Clean up old completed/failed jobs."""
        cutoff = datetime.now() - timedelta(days=days)
        with self.jobs_lock:
            jobs_to_remove = [
                job_id for job_id, job in self.jobs.items()
                if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]
                and job.created_at < cutoff
            ]
            for job_id in jobs_to_remove:
                del self.jobs[job_id]
    
    def cleanup_old_cache(self, days: int = 30):
        """Clean up old cache entries."""
        cutoff = datetime.now() - timedelta(days=days)
        with self.cache_lock:
            cache_to_remove = [
                cache_key for cache_key, entry in self.cache.items()
                if entry.created_at < cutoff
            ]
            for cache_key in cache_to_remove:
                del self.cache[cache_key]

# Global job service instance
job_service = JobService() 