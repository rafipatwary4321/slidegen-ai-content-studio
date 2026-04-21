from __future__ import annotations

import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.nid_verification import NIDVerification
from app.models.user import User
from app.services import automation
from app.services.automation_service import trigger_n8n_webhook

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["verification"])


@router.post("/verify-nid", status_code=status.HTTP_202_ACCEPTED)
async def verify_nid(
    file: Annotated[UploadFile, File(description="NID card image or scan")],
    user_id: Annotated[int, Form(description="User submitting the NID")],
    db: Session = Depends(get_db),
) -> dict[str, str | int | bool | None]:
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        automation.validate_nid_content_type(file.content_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    raw = await file.read()
    try:
        path = await automation.save_nid_upload(raw, file.filename or "nid.jpg")
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    row = NIDVerification(
        user_id=user_id,
        image_path=str(path),
        status="Pending",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    payload = {
        "event": "nid_verification",
        "verification_id": row.id,
        "user_id": user_id,
        "image_path": str(path),
        "filename": path.name,
    }
    result = await trigger_n8n_webhook("N8N_NID_WEBHOOK_URL", payload)
    if result is not None:
        row.status = "Sent"
        row.webhook_response = json.dumps(result)[:8000]
        row.webhook_error = None
    else:
        row.status = "Failed"
        row.webhook_error = "n8n unavailable or returned error"
        logger.warning("NID webhook failed for verification_id=%s", row.id)
    db.commit()

    return {
        "status": "Verification in Progress",
        "verification_id": row.id,
        "user_id": user_id,
        "image_path": str(path),
        "n8n_dispatched": result is not None,
        "n8n_detail": None if result is not None else row.webhook_error,
    }

import logging
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.services import automation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["verification"])


@router.post("/verify-nid", status_code=status.HTTP_202_ACCEPTED)
async def verify_nid(
    file: Annotated[UploadFile, File(description="NID document image")],
    user_id: Annotated[int | None, Form()] = None,
) -> dict[str, str | int | None]:
    """
    Accepts an NID image upload, stores it under `NID_UPLOAD_DIR`, and forwards the path to n8n.
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

    try:
        result = await automation.trigger_nid_verification(path, user_id=user_id)
    except Exception as exc:  # noqa: BLE001
        logger.exception("n8n NID webhook failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"n8n request failed: {exc}",
        ) from exc

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="N8N_WEBHOOK_URL is not configured",
        )

    return {
        "status": "accepted",
        "image_path": str(path),
        "user_id": user_id,
        "n8n": result,
    }
