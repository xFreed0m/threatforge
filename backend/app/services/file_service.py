import os
from pathlib import Path
import uuid
from datetime import datetime
from typing import Dict, List
from fastapi import UploadFile
from ..schemas.threat_model import FileUploadResponse, SupportedFileTypes

UPLOAD_DIR = Path(__file__).parent.parent.parent / "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# In-memory metadata store
db_files: Dict[str, FileUploadResponse] = {}

def ensure_upload_dir():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def allowed_file_type(filename: str) -> SupportedFileTypes:
    ext = filename.split(".")[-1].lower()
    for filetype in SupportedFileTypes:
        if ext == filetype.value:
            return filetype
    raise ValueError(f"Unsupported file type: {ext}")

def save_upload(file: UploadFile) -> FileUploadResponse:
    ensure_upload_dir()
    file_type = allowed_file_type(file.filename)
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    contents = file.file.read()
    size = len(contents)
    if size > MAX_FILE_SIZE:
        raise ValueError("File too large (max 10MB)")
    with open(file_path, "wb") as f:
        f.write(contents)
    upload_date = datetime.utcnow()
    meta = FileUploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_type=file_type,
        size=size,
        upload_date=upload_date,
    )
    db_files[file_id] = meta
    return meta

def list_files() -> List[FileUploadResponse]:
    return list(db_files.values())

def delete_file(file_id: str) -> bool:
    meta = db_files.get(file_id)
    if not meta:
        return False
    file_path = UPLOAD_DIR / f"{file_id}_{meta.filename}"
    if file_path.exists():
        file_path.unlink()
    del db_files[file_id]
    return True 