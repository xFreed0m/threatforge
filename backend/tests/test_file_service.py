import os
import shutil
import pytest
from pathlib import Path
from fastapi import UploadFile
from io import BytesIO
from app.services import file_service
from app.schemas.threat_model import SupportedFileTypes

UPLOADS_PATH = Path(__file__).parent.parent / "uploads"

def cleanup_uploads():
    if UPLOADS_PATH.exists():
        shutil.rmtree(UPLOADS_PATH)

class DummyUploadFile:
    def __init__(self, filename, content):
        self.filename = filename
        self.file = BytesIO(content)

@pytest.fixture(autouse=True)
def run_around_tests():
    cleanup_uploads()
    file_service.db_files.clear()
    yield
    cleanup_uploads()
    file_service.db_files.clear()

def test_allowed_file_type():
    assert file_service.allowed_file_type("diagram.drawio") == SupportedFileTypes.DRAWIO
    assert file_service.allowed_file_type("image.png") == SupportedFileTypes.PNG
    assert file_service.allowed_file_type("photo.jpg") == SupportedFileTypes.JPG
    assert file_service.allowed_file_type("vector.svg") == SupportedFileTypes.SVG
    assert file_service.allowed_file_type("data.xml") == SupportedFileTypes.XML
    with pytest.raises(ValueError):
        file_service.allowed_file_type("malware.exe")

def test_save_upload_and_list():
    file = DummyUploadFile("diagram.drawio", b"<xml>drawio</xml>")
    meta = file_service.save_upload(file)
    assert meta.filename == "diagram.drawio"
    assert meta.file_type == SupportedFileTypes.DRAWIO
    assert meta.size == len(b"<xml>drawio</xml>")
    files = file_service.list_files()
    assert any(f.file_id == meta.file_id for f in files)

def test_save_upload_too_large():
    file = DummyUploadFile("big.png", b"0" * (10 * 1024 * 1024 + 1))
    with pytest.raises(ValueError):
        file_service.save_upload(file)

def test_delete_file():
    file = DummyUploadFile("diagram.svg", b"<svg></svg>")
    meta = file_service.save_upload(file)
    assert file_service.delete_file(meta.file_id) is True
    assert file_service.delete_file(meta.file_id) is False
    assert all(f.file_id != meta.file_id for f in file_service.list_files()) 