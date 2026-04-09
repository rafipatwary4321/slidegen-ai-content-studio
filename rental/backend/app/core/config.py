import os
from functools import lru_cache
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent


def _nid_upload_dir() -> Path:
    raw = os.getenv("NID_UPLOAD_DIR", "").strip()
    if raw:
        return Path(raw).expanduser().resolve()
    return (_BACKEND_ROOT / "uploads" / "nid").resolve()


def _first_env(*keys: str) -> str:
    for key in keys:
        val = os.getenv(key, "").strip()
        if val:
            return val
    return ""


class Settings:
    """Application settings from environment (use `uvicorn --env-file .env` or export vars)."""

    database_url: str = os.getenv("DATABASE_URL", "")
    # n8n: prefer new names; fall back to legacy vars for existing deployments
    n8n_nid_webhook: str = _first_env("N8N_NID_WEBHOOK", "N8N_WEBHOOK_URL")
    n8n_agreement_webhook: str = _first_env(
        "N8N_AGREEMENT_WEBHOOK",
        "N8N_AGREEMENT_WEBHOOK_URL",
        "N8N_WEBHOOK_URL",
    )
    nid_upload_dir: Path = _nid_upload_dir()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
