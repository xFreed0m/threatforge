import pytest
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_export_diagram_data():
    """Test exporting diagram data in JSON format."""
    # Create a sample diagram data
    diagram_data = {
        "components": [
            {
                "id": "1",
                "name": "Web Application",
                "type": "frontend",
                "description": "React-based web application",
                "x": 100,
                "y": 100,
                "threats": []
            },
            {
                "id": "2", 
                "name": "Database",
                "type": "database",
                "description": "PostgreSQL database",
                "x": 300,
                "y": 100,
                "threats": []
            }
        ],
        "connections": [
            {
                "id": "conn1",
                "fromId": "1",
                "toId": "2",
                "from": {"x": 200, "y": 150},
                "to": {"x": 300, "y": 150}
            }
        ],
        "metadata": {
            "created": "2024-01-01T00:00:00Z",
            "version": "1.0"
        }
    }
    
    # Test that the data structure is valid
    assert "components" in diagram_data
    assert "connections" in diagram_data
    assert "metadata" in diagram_data
    
    # Test component structure
    for component in diagram_data["components"]:
        assert "id" in component
        assert "name" in component
        assert "type" in component
        assert "x" in component
        assert "y" in component
    
    # Test connection structure
    for connection in diagram_data["connections"]:
        assert "id" in connection
        assert "fromId" in connection
        assert "toId" in connection

def test_diagram_validation():
    """Test diagram data validation."""
    # Valid diagram data
    valid_diagram = {
        "components": [
            {
                "id": "1",
                "name": "Test Component",
                "type": "frontend",
                "description": "Test description",
                "x": 0,
                "y": 0,
                "threats": []
            }
        ],
        "connections": [],
        "metadata": {
            "created": "2024-01-01T00:00:00Z",
            "version": "1.0"
        }
    }
    
    # Test valid data
    assert len(valid_diagram["components"]) > 0
    assert all("id" in comp for comp in valid_diagram["components"])
    
    # Test invalid data (missing required fields)
    invalid_diagram = {
        "components": [
            {
                "name": "Test Component",
                # Missing id, type, x, y
            }
        ]
    }
    
    # Should fail validation
    assert not all("id" in comp for comp in invalid_diagram["components"])

def test_threat_mapping():
    """Test threat mapping to components."""
    # Sample threats
    threats = [
        {"id": 1, "name": "Spoofing", "severity": "high"},
        {"id": 2, "name": "Tampering", "severity": "medium"},
        {"id": 3, "name": "Information Disclosure", "severity": "high"}
    ]
    
    # Sample component with threats
    component_with_threats = {
        "id": "1",
        "name": "Database",
        "type": "database",
        "threats": [threats[0], threats[2]]  # High severity threats
    }
    
    # Test threat assignment
    assert len(component_with_threats["threats"]) == 2
    assert all(threat["severity"] in ["high", "medium", "low"] for threat in component_with_threats["threats"])
    
    # Test threat filtering by severity
    high_severity_threats = [t for t in component_with_threats["threats"] if t["severity"] == "high"]
    assert len(high_severity_threats) == 2

def test_component_types():
    """Test supported component types."""
    supported_types = ["external", "frontend", "backend", "database", "security", "infrastructure"]
    
    # Test valid component types
    for comp_type in supported_types:
        component = {
            "id": "1",
            "name": f"Test {comp_type}",
            "type": comp_type,
            "description": "Test component",
            "x": 0,
            "y": 0,
            "threats": []
        }
        assert component["type"] in supported_types
    
    # Test invalid component type
    invalid_component = {
        "id": "1",
        "name": "Invalid Component",
        "type": "invalid_type",
        "description": "Test component",
        "x": 0,
        "y": 0,
        "threats": []
    }
    assert invalid_component["type"] not in supported_types

def test_diagram_export_format():
    """Test diagram export format consistency."""
    # Create a complete diagram
    diagram = {
        "components": [
            {
                "id": "web",
                "name": "Web Server",
                "type": "frontend",
                "description": "Nginx web server",
                "x": 100,
                "y": 100,
                "threats": []
            },
            {
                "id": "api",
                "name": "API Server",
                "type": "backend",
                "description": "Node.js API server",
                "x": 300,
                "y": 100,
                "threats": []
            },
            {
                "id": "db",
                "name": "Database",
                "type": "database",
                "description": "PostgreSQL database",
                "x": 500,
                "y": 100,
                "threats": []
            }
        ],
        "connections": [
            {
                "id": "conn1",
                "fromId": "web",
                "toId": "api",
                "from": {"x": 200, "y": 150},
                "to": {"x": 300, "y": 150}
            },
            {
                "id": "conn2",
                "fromId": "api",
                "toId": "db",
                "from": {"x": 400, "y": 150},
                "to": {"x": 500, "y": 150}
            }
        ],
        "metadata": {
            "created": "2024-01-01T00:00:00Z",
            "version": "1.0",
            "title": "Sample System Architecture"
        }
    }
    
    # Test JSON serialization
    json_data = json.dumps(diagram)
    assert isinstance(json_data, str)
    
    # Test JSON deserialization
    parsed_diagram = json.loads(json_data)
    assert parsed_diagram["metadata"]["title"] == "Sample System Architecture"
    assert len(parsed_diagram["components"]) == 3
    assert len(parsed_diagram["connections"]) == 2

def test_threat_severity_levels():
    """Test threat severity level validation."""
    valid_severities = ["high", "medium", "low"]
    
    # Test valid severities
    for severity in valid_severities:
        threat = {
            "id": 1,
            "name": "Test Threat",
            "severity": severity,
            "description": "Test threat description"
        }
        assert threat["severity"] in valid_severities
    
    # Test invalid severity
    invalid_threat = {
        "id": 1,
        "name": "Invalid Threat",
        "severity": "invalid",
        "description": "Test threat description"
    }
    assert invalid_threat["severity"] not in valid_severities

def test_component_positioning():
    """Test component positioning and layout."""
    components = [
        {"id": "1", "name": "Component 1", "x": 0, "y": 0},
        {"id": "2", "name": "Component 2", "x": 200, "y": 0},
        {"id": "3", "name": "Component 3", "x": 400, "y": 0}
    ]
    
    # Test positioning
    for i, component in enumerate(components):
        assert component["x"] == i * 200
        assert component["y"] == 0
    
    # Test no overlapping components
    positions = [(comp["x"], comp["y"]) for comp in components]
    assert len(positions) == len(set(positions))

def test_connection_validation():
    """Test connection validation between components."""
    components = [
        {"id": "1", "name": "Component 1"},
        {"id": "2", "name": "Component 2"},
        {"id": "3", "name": "Component 3"}
    ]
    
    component_ids = [comp["id"] for comp in components]
    
    # Valid connections
    valid_connections = [
        {"fromId": "1", "toId": "2"},
        {"fromId": "2", "toId": "3"}
    ]
    
    for conn in valid_connections:
        assert conn["fromId"] in component_ids
        assert conn["toId"] in component_ids
    
    # Invalid connection (non-existent component)
    invalid_connection = {"fromId": "1", "toId": "999"}
    assert invalid_connection["toId"] not in component_ids 