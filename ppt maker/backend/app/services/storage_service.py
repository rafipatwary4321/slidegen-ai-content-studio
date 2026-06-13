"""Blob storage abstraction: local filesystem (dev) with S3-ready interface."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from uuid import uuid4


class BlobStorage(ABC):
    @abstractmethod
    def put(self, key: str, data: bytes, content_type: str) -> str:
        """Persist bytes; return storage URI or path."""

    @abstractmethod
    def resolve_path(self, key: str) -> Path | None:
        """Local path for reading, if applicable."""


class LocalBlobStorage(BlobStorage):
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path(__file__).resolve().parents[2] / "storage" / "uploads"
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, data: bytes, content_type: str) -> str:
        path = self.root / key
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return f"file://{path}"

    def resolve_path(self, key: str) -> Path | None:
        path = self.root / key
        return path if path.is_file() else None


class S3BlobStorage(BlobStorage):
    """
    Production S3 backend (wire when STORAGE_BACKEND=s3).
    Requires: boto3, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_BUCKET, AWS_REGION.
    """

    def __init__(self) -> None:
        raise NotImplementedError(
            "S3 storage is not configured. Set STORAGE_BACKEND=local or implement S3BlobStorage with boto3."
        )

    def put(self, key: str, data: bytes, content_type: str) -> str:
        raise NotImplementedError

    def resolve_path(self, key: str) -> Path | None:
        raise NotImplementedError


def get_blob_storage() -> BlobStorage:
    backend = os.getenv("STORAGE_BACKEND", "local").lower()
    if backend == "s3":
        return S3BlobStorage()
    return LocalBlobStorage()


def store_upload_blob(filename: str, data: bytes, content_type: str) -> str:
    """Save raw upload under a unique key; returns storage key."""
    ext = Path(filename).suffix.lower()
    key = f"{uuid4().hex}{ext}"
    get_blob_storage().put(key, data, content_type)
    return key
