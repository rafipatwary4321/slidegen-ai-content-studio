import hashlib
from pathlib import Path

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # 25 MB


def get_extension(filename: str | None) -> str:
    if not filename:
        return ""
    return Path(filename).suffix.lower().replace(".", "")


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
