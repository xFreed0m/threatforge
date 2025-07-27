"""Main FastAPI application module for ThreatForge."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.scenarios import router as scenarios_router
from app.api import threat_model

app = FastAPI(
    title="ThreatForge",
    description="AI-powered cybersecurity tabletop exercise scenario generator",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scenarios_router)
app.include_router(threat_model.router)

@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to ThreatForge API"}

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health_check() -> dict[str, str]:
    """API health check endpoint."""
    return {"status": "healthy"}
