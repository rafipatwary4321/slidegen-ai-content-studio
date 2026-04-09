import logging
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.core.config import settings
from app.services import automation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/verify-nid", status_code=status.HTTP_202_ACCEPTED)
async def verify_nid(
    file: Annotated[UploadFile, File(description="NID card image or scan")],
    user_id: Annotated[int, Form(description="User submitting the NID")],
) -> dict[str, str | int | bool | None]:
    """
    Accepts an NID upload, persists it, and forwards metadata to the NID-Verification n8n webhook.
    Always returns **202** with *Verification in Progress*; n8n failures are logged and surfaced
    via `n8n_dispatched` without failing the request.
    """
    try:
        automation.validate_nid_content_type(file.content_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    raw = await file.read()
    try:
        path = await automation.save_nid_upload(raw, file.filename or "nid.jpg")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    n8n_result: dict | None = None
    n8n_error: str | None = None

    if not settings.n8n_nid_webhook:
        n8n_error = "N8N_NID_WEBHOOK is not configured"
        logger.warning(n8n_error)
    else:
        n8n_result = await automation.trigger_nid_verification(path, user_id=user_id)
        if n8n_result is None:
            n8n_error = (
                "n8n did not accept the request (server down, timeout, or non-2xx response). "
                "Check logs; verification can be retried."
            )
            logger.warning("NID n8n dispatch failed for user_id=%s path=%s", user_id, path)

    return {
        "status": "Verification in Progress",
        "user_id": user_id,
        "image_path": str(path),
        "filename": path.name,
        "n8n_dispatched": n8n_result is not None,
        "n8n_detail": n8n_error if n8n_result is None else None,
        "n8n_response": n8n_result,
    }
