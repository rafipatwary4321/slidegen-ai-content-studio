from __future__ import annotations

import logging
import os
from typing import Any

import httpx  # pylint: disable=import-error

from app.core.config import settings

logger = logging.getLogger(__name__)


def _webhook_url_for_env_var(webhook_url_env_var: str) -> str:
    direct = os.getenv(webhook_url_env_var, "").strip()
    if direct:
        return direct
    fallback = {
        "N8N_NID_WEBHOOK_URL": settings.n8n_nid_webhook,
        "N8N_AGREEMENT_WEBHOOK_URL": settings.n8n_agreement_webhook,
    }.get(webhook_url_env_var, "")
    return (fallback or "").strip()


async def trigger_n8n_webhook(webhook_url_env_var: str, payload: dict) -> dict[str, Any] | None:
    """
    Generic n8n trigger by environment variable name.
    Returns JSON dict on success, or None on missing URL/network/error.
    """
    url = _webhook_url_for_env_var(webhook_url_env_var)
    if not url:
        logger.warning("%s is not configured; webhook skipped", webhook_url_env_var)
        return None
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            if not response.content:
                return {}
            return response.json()
    except Exception as exc:  # noqa: BLE001  # pylint: disable=broad-exception-caught
        logger.exception("n8n webhook failed (%s): %s", webhook_url_env_var, exc)
        return None

