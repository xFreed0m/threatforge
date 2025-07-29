import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.services import file_service

client = TestClient(app)

@pytest.fixture
def sample_drawio_file():
    """Create a temporary .drawio file for testing."""
    content = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="test" name="Test">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="User" style="ellipse;fillColor=#ffcccc;" vertex="1" parent="1">
          <mxGeometry x="80" y="80" width="80" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="Database" style="rounded=1;fillColor=#ccffcc;" vertex="1" parent="1">
          <mxGeometry x="240" y="80" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="4" edge="1" source="2" target="3" style="endArrow=block;strokeColor=#000000;" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.drawio', delete=False) as f:
        f.write(content)
        return f.name

def test_generate_threat_model_success(sample_drawio_file):
    """Test successful threat model generation."""
    # Upload the file first
    with open(sample_drawio_file, 'rb') as f:
        response = client.post("/api/threat-model/upload", files={"file": ("test.drawio", f, "application/octet-stream")})
    
    assert response.status_code == 200
    file_data = response.json()
    file_id = file_data["file_id"]
    
    # Generate threat model with the uploaded file
    response = client.post("/api/threat-model/generate", json={
        "content": "A web application with user authentication and database storage",
        "framework": "STRIDE",
        "file_id": file_id,
        "llm_provider": "openai"
    })
    
    assert response.status_code == 200
    threat_model = response.json()
    
    # Check threat model structure
    assert "id" in threat_model
    assert "threat_model" in threat_model
    assert "estimated_cost" in threat_model
    assert "provider_used" in threat_model
    assert "framework" in threat_model
    assert "content_analyzed" in threat_model
    
    # Check that threat model content was generated
    assert len(threat_model["threat_model"]) > 0
    assert threat_model["framework"] == "STRIDE"
    assert threat_model["provider_used"] == "openai"
    
    # Cleanup
    Path(sample_drawio_file).unlink()

def test_generate_threat_model_text_only():
    """Test threat model generation with text content only."""
    response = client.post("/api/threat-model/generate", json={
        "content": "A simple web application with user login and data storage",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    assert response.status_code == 200
    threat_model = response.json()
    
    # Check threat model structure
    assert "id" in threat_model
    assert "threat_model" in threat_model
    assert "estimated_cost" in threat_model
    assert "provider_used" in threat_model
    assert "framework" in threat_model
    assert "content_analyzed" in threat_model
    
    # Check that threat model content was generated
    assert len(threat_model["threat_model"]) > 0
    assert threat_model["framework"] == "STRIDE"
    assert threat_model["provider_used"] == "openai"

def test_generate_threat_model_nonexistent_file():
    """Test generation with a file that doesn't exist."""
    response = client.post("/api/threat-model/generate", json={
        "content": "Test content",
        "framework": "STRIDE",
        "file_id": "nonexistent-id",
        "llm_provider": "openai"
    })
    
    assert response.status_code == 404
    assert "File not found" in response.json()["detail"]

def test_generate_threat_model_invalid_provider():
    """Test generation with an invalid provider."""
    response = client.post("/api/threat-model/generate", json={
        "content": "Test content",
        "framework": "STRIDE",
        "llm_provider": "invalid-provider"
    })
    
    assert response.status_code == 400
    assert "not available" in response.json()["detail"]

def test_generate_threat_model_different_frameworks():
    """Test threat model generation with different frameworks."""
    frameworks = ["STRIDE", "LINDDUN", "PASTA", "ATTACK_TREES"]
    
    for framework in frameworks:
        response = client.post("/api/threat-model/generate", json={
            "content": "A cloud-based application with microservices architecture",
            "framework": framework,
            "llm_provider": "openai"
        })
        
        assert response.status_code == 200
        threat_model = response.json()
        assert threat_model["framework"] == framework
        assert len(threat_model["threat_model"]) > 0

def test_get_providers():
    """Test getting available providers."""
    response = client.get("/api/threat-model/providers")
    
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert isinstance(data["providers"], list)
    assert len(data["providers"]) > 0 

def test_estimate_cost():
    """Test cost estimation across providers."""
    response = client.post("/api/threat-model/estimate-cost", json={
        "content": "A simple web application with user authentication",
        "framework": "STRIDE",
        "llm_provider": "openai"
    })
    
    assert response.status_code == 200
    estimates = response.json()
    
    assert isinstance(estimates, list)
    assert len(estimates) > 0
    
    for estimate in estimates:
        assert "provider" in estimate
        assert "estimated_cost" in estimate
        assert estimate["provider"] in ["openai", "anthropic"] 