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
        
        return f"""# ELITE THREAT MODELING ANALYSIS

## EXECUTIVE SUMMARY
You are a world-class cybersecurity expert with 20+ years of experience in threat modeling, security architecture, and risk assessment. You specialize in identifying sophisticated attack vectors and providing actionable security recommendations.

## ANALYSIS FRAMEWORK
**Primary Framework**: {request.framework}
**Analysis Depth**: Comprehensive threat modeling with real-world attack scenarios

## SYSTEM UNDER ANALYSIS
{content_to_analyze}

## THREAT MODELING REQUIREMENTS

### 1. SYSTEM ARCHITECTURE ANALYSIS
- **Component Inventory**: Complete mapping of all system components, data flows, and trust boundaries
- **Technology Stack Assessment**: Security implications of each technology choice
- **Integration Points**: External dependencies, APIs, and third-party services
- **Data Classification**: Sensitivity levels and regulatory requirements for all data types

### 2. THREAT ACTOR PROFILING
- **Adversary Types**: Nation-state actors, organized crime, insider threats, hacktivists
- **Capability Assessment**: Technical sophistication, resources, and persistence
- **Motivation Analysis**: Financial gain, espionage, sabotage, reputation damage
- **Attack Surface Mapping**: All potential entry points and attack vectors

### 3. COMPREHENSIVE THREAT ANALYSIS
Using the {request.framework} framework, analyze each component for:

#### STRIDE Threats (if applicable):
- **Spoofing**: Identity impersonation, credential theft, session hijacking
- **Tampering**: Data manipulation, code injection, configuration changes
- **Repudiation**: Audit log deletion, transaction denial, evidence destruction
- **Information Disclosure**: Data breaches, information leakage, side-channel attacks
- **Denial of Service**: Resource exhaustion, service disruption, availability attacks
- **Elevation of Privilege**: Privilege escalation, access control bypass, admin compromise

#### Additional Threat Categories:
- **Supply Chain Attacks**: Compromised dependencies, vendor risks, build system attacks
- **Social Engineering**: Phishing, pretexting, baiting, quid pro quo
- **Physical Security**: Physical access, hardware tampering, environmental threats
- **Emerging Threats**: AI/ML attacks, quantum computing risks, zero-day exploits

### 4. RISK ASSESSMENT & PRIORITIZATION
- **Threat Likelihood**: Based on attacker capabilities, system exposure, and historical data
- **Impact Assessment**: Business impact, financial loss, regulatory consequences
- **Risk Scoring**: Quantitative risk assessment using industry-standard methodologies
- **Priority Ranking**: Critical, High, Medium, Low based on likelihood × impact

### 5. MITIGATION STRATEGY DEVELOPMENT
- **Defense in Depth**: Multiple layers of security controls
- **Zero Trust Architecture**: Never trust, always verify principles
- **Security Controls**: Technical, administrative, and physical safeguards
- **Monitoring & Detection**: Real-time threat detection and response capabilities
- **Incident Response**: Preparedness and recovery procedures

### 6. COMPLIANCE & REGULATORY CONSIDERATIONS
- **Industry Standards**: ISO 27001, NIST, CIS Controls, OWASP
- **Regulatory Requirements**: GDPR, HIPAA, SOX, PCI-DSS as applicable
- **Best Practices**: Industry-specific security frameworks and guidelines

## DELIVERABLE FORMAT

Structure your analysis with these sections:

### 1. EXECUTIVE SUMMARY
- Key findings and critical risks
- Overall security posture assessment
- Strategic recommendations

### 2. SYSTEM OVERVIEW
- Architecture description and component mapping
- Data flow analysis and trust boundaries
- Technology stack security assessment

### 3. THREAT LANDSCAPE
- Threat actor profiles and capabilities
- Attack surface analysis
- Historical threat intelligence

### 4. DETAILED THREAT ANALYSIS
- Component-by-component threat assessment
- Specific attack scenarios and vectors
- Vulnerability analysis and exploitability

### 5. RISK ASSESSMENT
- Risk matrix with likelihood and impact
- Priority ranking of threats
- Risk acceptance criteria

### 6. MITIGATION STRATEGIES
- Technical controls and countermeasures
- Process improvements and policies
- Monitoring and detection capabilities

### 7. SECURITY ROADMAP
- Short-term (0-3 months) critical fixes
- Medium-term (3-12 months) improvements
- Long-term (1+ years) strategic initiatives

### 8. COMPLIANCE ASSESSMENT
- Regulatory gap analysis
- Standards compliance status
- Remediation requirements

Ensure your analysis is technically accurate, actionable, and provides clear guidance for security improvement initiatives."""
    
    def create_job(self, request: AsyncThreatModelRequest) -> str:
        """Create a new async job for threat model generation."""
        job_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Check cache first
        cache_key = getattr(request, 'cache_key', None) or self._generate_cache_key(request)
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
            import os
            if os.getenv('TESTING') == 'true':
                available_providers = ["openai", "anthropic"]
            else:
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