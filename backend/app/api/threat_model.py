from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from ..services import file_service
from ..schemas.threat_model import (
    FileUploadResponse, ThreatModelRequest, ThreatModelResponse,
    AsyncThreatModelRequest, JobResponse, JobStatusResponse, JobStatus
)
from ..services.llm_factory import LLMFactory
from ..services.job_service import job_service
import uuid
import datetime
import logging

router = APIRouter(prefix="/api/threat-model", tags=["Threat Model"])

logger = logging.getLogger("threat_model")

def build_threat_model_prompt(request: ThreatModelRequest, file_content: str = None) -> str:
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

@router.post("/generate", response_model=ThreatModelResponse)
async def generate_threat_model(request: ThreatModelRequest) -> ThreatModelResponse:
    """Generate a threat model using AI analysis.
    
    Args:
        request: The threat modeling request containing content and framework.
        
    Returns:
        The generated threat model response.
        
    Raises:
        HTTPException: If no providers are available or generation fails.
    """
    # Get available providers
    available_providers = LLMFactory.get_available_providers()
    if not available_providers:
        raise HTTPException(status_code=500, detail="No LLM providers configured")
    
    # Select provider
    provider = request.llm_provider or available_providers[0]
    if provider not in available_providers:
        raise HTTPException(status_code=400, detail=f"Provider {provider} not available")
    
    # Get file content if file_id is provided
    file_content = None
    if request.file_id:
        meta = file_service.db_files.get(request.file_id)
        if not meta:
            raise HTTPException(status_code=404, detail="File not found")
        
        # For now, we'll use a placeholder for file content
        # In a real implementation, you'd parse the file and extract meaningful content
        if meta.file_type in ("drawio", "xml"):
            file_content = f"Diagram file: {meta.filename} (type: {meta.file_type})"
        else:
            file_content = f"Image file: {meta.filename} (type: {meta.file_type})"
    
    # Create service and generate
    try:
        service = LLMFactory.create(provider)
        prompt = build_threat_model_prompt(request, file_content)
        threat_model = await service.generate(prompt)
        cost = service.estimate_cost(prompt)
        threat_model_id = str(uuid.uuid4())
        
        return ThreatModelResponse(
            id=threat_model_id,
            threat_model=threat_model,
            estimated_cost=cost,
            provider_used=provider,
            framework=request.framework,
            content_analyzed=request.content
        )
    except Exception as e:
        logger.exception(f"Error generating threat model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-async", response_model=JobResponse)
async def generate_threat_model_async(request: AsyncThreatModelRequest) -> JobResponse:
    """Generate a threat model asynchronously.
    
    Args:
        request: The async threat modeling request.
        
    Returns:
        Job response with job ID and initial status.
    """
    try:
        job_id = job_service.create_job(request)
        job_status = job_service.get_job_status(job_id)
        
        return JobResponse(
            job_id=job_id,
            status=job_status.status,
            message=job_status.message,
            estimated_completion=job_status.estimated_completion
        )
    except Exception as e:
        logger.exception(f"Error creating async job: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str) -> JobStatusResponse:
    """Get the status of an async job.
    
    Args:
        job_id: The job identifier.
        
    Returns:
        Current job status and progress.
        
    Raises:
        HTTPException: If job not found.
    """
    job_status = job_service.get_job_status(job_id)
    if not job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job_status

@router.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """Cancel an async job.
    
    Args:
        job_id: The job identifier.
        
    Returns:
        Success message if job was cancelled.
        
    Raises:
        HTTPException: If job not found or cannot be cancelled.
    """
    success = job_service.cancel_job(job_id)
    if not success:
        raise HTTPException(status_code=400, detail="Job not found or cannot be cancelled")
    
    return {"detail": "Job cancelled successfully"}

@router.get("/jobs", response_model=List[JobStatusResponse])
async def list_jobs(limit: int = 50) -> List[JobStatusResponse]:
    """List recent jobs.
    
    Args:
        limit: Maximum number of jobs to return.
        
    Returns:
        List of recent jobs.
    """
    return job_service.list_jobs(limit)

@router.post("/estimate-cost")
async def estimate_cost(request: ThreatModelRequest):
    """Estimate costs for threat model generation across all providers.
    
    Args:
        request: The threat modeling request to estimate costs for.
        
    Returns:
        List of cost estimates for each available provider.
    """
    available_providers = LLMFactory.get_available_providers()
    if not available_providers:
        raise HTTPException(status_code=500, detail="No LLM providers configured")
    
    # Get file content if file_id is provided
    file_content = None
    if request.file_id:
        meta = file_service.db_files.get(request.file_id)
        if not meta:
            raise HTTPException(status_code=404, detail="File not found")
        
        if meta.file_type in ("drawio", "xml"):
            file_content = f"Diagram file: {meta.filename} (type: {meta.file_type})"
        else:
            file_content = f"Image file: {meta.filename} (type: {meta.file_type})"
    
    estimates = []
    prompt = build_threat_model_prompt(request, file_content)
    
    for provider in available_providers:
        try:
            service = LLMFactory.create(provider)
            cost = service.estimate_cost(prompt)
            estimates.append({
                "provider": provider.value,
                "estimated_cost": cost
            })
        except Exception as e:
            logger.warning(f"Failed to estimate cost for {provider.value}: {e}")
            estimates.append({
                "provider": provider.value,
                "estimated_cost": None,
                "error": str(e)
            })
    
    return estimates

@router.get("/providers")
async def get_providers():
    """Get available LLM providers for threat modeling."""
    available_providers = LLMFactory.get_available_providers()
    return {"providers": [p.value for p in available_providers]}

@router.post("/upload", response_model=FileUploadResponse)
async def upload_diagram(file: UploadFile = File(...)):
    try:
        meta = file_service.save_upload(file)
        return meta
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/files", response_model=List[FileUploadResponse])
async def list_files():
    return file_service.list_files()

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    success = file_service.delete_file(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"detail": "File deleted"} 