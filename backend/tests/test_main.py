import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to ThreatForge API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_list_delete_file(client):
    # Prepare a small PNG file in memory
    file_content = b"\x89PNG\r\n\x1a\n" + b"0" * 100  # minimal PNG header + data
    files = {"file": ("test.png", file_content, "image/png")}
    # Upload
    response = client.post("/api/threat-model/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.png"
    assert data["file_type"] == "png"
    file_id = data["file_id"]
    # List
    response = client.get("/api/threat-model/files")
    assert response.status_code == 200
    files_list = response.json()
    assert any(f["file_id"] == file_id for f in files_list)
    # Delete
    response = client.delete(f"/api/threat-model/files/{file_id}")
    assert response.status_code == 200
    # Confirm deletion
    response = client.get("/api/threat-model/files")
    assert all(f["file_id"] != file_id for f in response.json())

def test_upload_invalid_type(client):
    file_content = b"not a real file"
    files = {"file": ("test.exe", file_content, "application/octet-stream")}
    response = client.post("/api/threat-model/upload", files=files)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_upload_too_large(client):
    file_content = b"0" * (10 * 1024 * 1024 + 1)  # 10MB + 1 byte
    files = {"file": ("big.png", file_content, "image/png")}
    response = client.post("/api/threat-model/upload", files=files)
    assert response.status_code == 400
    assert "File too large" in response.json()["detail"]
