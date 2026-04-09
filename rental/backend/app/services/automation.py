from __future__ import annotations

import logging
import uuid
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

DEFAULT_N8N_TIMEOUT = 120.0
MAX_NID_UPLOAD_BYTES = 10 * 1024 * 1024


async def send_to_n8n(
    webhook_url: str,
    payload: dict[str, Any],
    *,
    timeout: float = DEFAULT_N8N_TIMEOUT,
) -> dict[str, Any] | None:
    """
    POST JSON to an n8n webhook. Returns parsed JSON on success, or None if the URL is empty,
    the server is unreachable, HTTP status is non-success, or the body is not JSON.
    """
    url = (webhook_url or "").strip()
    if not url:
        logger.warning("send_to_n8n: empty webhook_url; skipping")
        return None

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            if not response.content:
                return {}
            return response.json()
    except httpx.HTTPStatusError as exc:
        body = (exc.response.text or "")[:800]
        logger.error(
            "n8n HTTP error %s for %s: %s",
            exc.response.status_code,
            url.split("?", 1)[0],
            body,
        )
        return None
    except httpx.RequestError as exc:
        logger.error("n8n request failed (%s): %s", url.split("?", 1)[0], exc)
        return None
    except ValueError as exc:
        logger.error("n8n response was not valid JSON: %s", exc)
        return None


def send_to_n8n_sync(
    webhook_url: str,
    payload: dict[str, Any],
    *,
    timeout: float = DEFAULT_N8N_TIMEOUT,
) -> dict[str, Any] | None:
    """Blocking variant for sync code paths (e.g. booking confirmation)."""
    url = (webhook_url or "").strip()
    if not url:
        logger.warning("send_to_n8n_sync: empty webhook_url; skipping")
        return None

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            if not response.content:
                return {}
            return response.json()
    except httpx.HTTPStatusError as exc:
        body = (exc.response.text or "")[:800]
        logger.error(
            "n8n HTTP error %s for %s: %s",
            exc.response.status_code,
            url.split("?", 1)[0],
            body,
        )
        return None
    except httpx.RequestError as exc:
        logger.error("n8n request failed (%s): %s", url.split("?", 1)[0], exc)
        return None
    except ValueError as exc:
        logger.error("n8n response was not valid JSON: %s", exc)
        return None


async def trigger_nid_verification(
    image_path: str | Path,
    *,
    user_id: int,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """
    Send NID file metadata and user id to the NID-Verification n8n workflow (N8N_NID_WEBHOOK).
    """
    path = Path(image_path).resolve()
    payload: dict[str, Any] = {
        "event": "nid_verification",
        "user_id": user_id,
        "image_path": str(path),
        "filename": path.name,
        "content_type_hint": "image_or_pdf",
    }
    if extra:
        payload["meta"] = extra

    return await send_to_n8n(settings.n8n_nid_webhook, payload)


def _date_iso(value: date | str) -> str:
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def digital_agreement_payload(
    *,
    booking_id: int,
    listing_id: int,
    listing_title: str,
    guest_email: str,
    host_email: str,
    start_date: date | str,
    end_date: date | str,
    total_price: Decimal | float | str,
    guest_name: str | None = None,
    host_name: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "event": "rental_agreement_pdf",
        "booking_id": booking_id,
        "listing_id": listing_id,
        "listing_title": listing_title,
        "guest_email": guest_email,
        "host_email": host_email,
        "guest_name": guest_name,
        "host_name": host_name,
        "start_date": _date_iso(start_date),
        "end_date": _date_iso(end_date),
        "total_price": str(total_price),
    }
    if extra:
        payload["meta"] = extra
    return payload


def agreement_webhook_url() -> str:
    return (settings.n8n_agreement_webhook or "").strip()


def agreement_url_from_n8n_response(result: dict[str, Any] | None) -> str | None:
    """Read a download URL from common n8n response shapes (flat or one-level `data`)."""
    if not result:
        return None
    keys = (
        "agreement_document_url",
        "agreement_url",
        "pdf_url",
        "document_url",
        "download_url",
        "url",
    )
    for key in keys:
        v = result.get(key)
        if isinstance(v, str) and v.strip().startswith(("http://", "https://")):
            return v.strip()
    nested = result.get("data")
    if isinstance(nested, dict):
        for key in keys:
            v = nested.get(key)
            if isinstance(v, str) and v.strip().startswith(("http://", "https://")):
                return v.strip()
    return None


async def trigger_rental_agreement_n8n(
    *,
    booking_id: int,
    listing_id: int,
    listing_title: str,
    guest_email: str,
    host_email: str,
    start_date: date | str,
    end_date: date | str,
    total_price: Decimal | float | str,
    guest_name: str | None = None,
    host_name: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """When a booking becomes Confirmed: trigger n8n to build/send the PDF rental agreement."""
    payload = digital_agreement_payload(
        booking_id=booking_id,
        listing_id=listing_id,
        listing_title=listing_title,
        guest_email=guest_email,
        host_email=host_email,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        guest_name=guest_name,
        host_name=host_name,
        extra=extra,
    )
    return await send_to_n8n(agreement_webhook_url(), payload)


def trigger_rental_agreement_n8n_sync(
    *,
    booking_id: int,
    listing_id: int,
    listing_title: str,
    guest_email: str,
    host_email: str,
    start_date: date | str,
    end_date: date | str,
    total_price: Decimal | float | str,
    guest_name: str | None = None,
    host_name: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Sync variant used from `booking_confirmation` (non-async SQLAlchemy session)."""
    payload = digital_agreement_payload(
        booking_id=booking_id,
        listing_id=listing_id,
        listing_title=listing_title,
        guest_email=guest_email,
        host_email=host_email,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        guest_name=guest_name,
        host_name=host_name,
        extra=extra,
    )
    return send_to_n8n_sync(agreement_webhook_url(), payload)


# Backwards-compatible names
generate_digital_agreement = trigger_rental_agreement_n8n
generate_digital_agreement_sync = trigger_rental_agreement_n8n_sync


def nid_stored_filename(original_name: str) -> str:
    ext = Path(original_name).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".heic", ".pdf"}:
        ext = ".bin"
    return f"{uuid.uuid4().hex}{ext}"


def validate_nid_content_type(content_type: str | None) -> None:
    ct = (content_type or "").lower()
    if ct.startswith("image/") or ct == "application/pdf":
        return
    raise ValueError("File must be image/* or application/pdf")


async def save_nid_upload(content: bytes, original_filename: str) -> Path:
    if len(content) > MAX_NID_UPLOAD_BYTES:
        raise ValueError(f"File too large (max {MAX_NID_UPLOAD_BYTES // (1024 * 1024)} MB)")

    dest_dir = settings.nid_upload_dir
    dest_dir.mkdir(parents=True, exist_ok=True)
    name = nid_stored_filename(original_filename)
    path = dest_dir / name
    path.write_bytes(content)
    logger.info("Saved NID upload to %s", path)
    return path.resolve()
