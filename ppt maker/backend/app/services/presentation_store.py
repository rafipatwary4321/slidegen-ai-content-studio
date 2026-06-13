from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

import bcrypt

from app.models.schemas import (
    AuthUser,
    ExportResult,
    PresentationRecord,
    SavePresentationRequest,
    SlideOutlineItem,
    SignUpRequest,
    SpeakerNoteItem,
    UploadedFileMeta,
)

try:
    from prisma import Prisma
except Exception:  # pragma: no cover - optional runtime dependency
    Prisma = None


class PresentationStore:
    """Prisma-backed store with JSON fallback for local safety."""

    def __init__(self) -> None:
        self.data_dir = Path(__file__).resolve().parents[2] / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "presentations.json"
        self.users_path = self.data_dir / "users.json"
        self.upload_records_path = self.data_dir / "upload_records.json"
        self._lock = Lock()
        self._prisma = None

        if not self.db_path.exists():
            self._write([])

        if not self.users_path.exists():
            self.users_path.write_text("[]", encoding="utf-8")

        if not self.upload_records_path.exists():
            self.upload_records_path.write_text("[]", encoding="utf-8")

        self._enable_prisma = self._can_use_prisma()
        if self._enable_prisma:
            try:
                self._prisma = Prisma()
                self._prisma.connect()
            except Exception:
                self._prisma = None
                self._enable_prisma = False

    def close(self) -> None:
        if self._prisma is not None:
            try:
                self._prisma.disconnect()
            except Exception:
                pass

    def list_presentations(self, user_id: str | None = None) -> list[PresentationRecord]:
        if self._prisma is not None:
            try:
                rows = self._prisma.presentation.find_many(
                    where={"user_id": user_id} if user_id else None,
                    order={"created_at": "desc"},
                    include={"slides": True, "speaker_notes": True},
                )
                return [self._to_record_from_prisma(row) for row in rows]
            except Exception:
                pass

        records = [PresentationRecord.model_validate(item) for item in self._read()]
        if user_id:
            records = [record for record in records if record.user_id == user_id]
        return sorted(records, key=lambda x: self._parse_created_at(x.created_at), reverse=True)

    def get_presentation(self, presentation_id: str, user_id: str | None = None) -> PresentationRecord | None:
        if self._prisma is not None:
            try:
                row = self._prisma.presentation.find_unique(
                    where={"id": presentation_id},
                    include={"slides": True, "speaker_notes": True},
                )
                if row and (not user_id or row.user_id == user_id):
                    return self._to_record_from_prisma(row)
            except Exception:
                pass

        for item in self._read():
            if item.get("id") == presentation_id:
                if user_id and item.get("user_id") != user_id:
                    return None
                return PresentationRecord.model_validate(item)
        return None

    def save_presentation(self, payload: SavePresentationRequest) -> PresentationRecord:
        if self._prisma is not None:
            try:
                uploaded_file = self._prisma.uploadedfile.find_first(
                    where={"filename": payload.uploaded_filename},
                    order={"updated_at": "desc"},
                )
                row = self._prisma.presentation.create(
                    data={
                        "title": payload.title,
                        "uploaded_filename": payload.uploaded_filename,
                        "persona": payload.persona,
                        "theme": payload.theme,
                        "status": "generated",
                        "pptx_file_path": payload.pptx_file_path,
                        "user_id": payload.user_id,
                        "uploaded_file_id": uploaded_file.id if uploaded_file else None,
                        "slides": {
                            "create": [
                                {
                                    "slide_number": slide.slide_number,
                                    "title": slide.title,
                                    "bullets": slide.bullets,
                                }
                                for slide in payload.outline
                            ]
                        },
                        "speaker_notes": {
                            "create": [
                                {"slide_number": note.slide_number, "note": note.note}
                                for note in payload.speaker_notes
                            ]
                        },
                    },
                    include={"slides": True, "speaker_notes": True},
                )
                return self._to_record_from_prisma(row)
            except Exception:
                pass

        now = self._now_iso()
        record = PresentationRecord(
            id=str(uuid4()),
            title=payload.title,
            uploaded_filename=payload.uploaded_filename,
            user_id=payload.user_id,
            persona=payload.persona,
            theme=payload.theme,
            created_at=now,
            outline=payload.outline,
            speaker_notes=payload.speaker_notes,
            pptx_file_path=payload.pptx_file_path,
        )
        items = self._read()
        items.append(record.model_dump())
        self._write(items)
        return record

    def update_pptx_file_path(
        self, presentation_id: str, pptx_file_path: str, user_id: str | None = None
    ) -> PresentationRecord | None:
        if self._prisma is not None:
            try:
                row = self._prisma.presentation.find_unique(where={"id": presentation_id})
                if row is None or (user_id and row.user_id != user_id):
                    return None
                row = self._prisma.presentation.update(
                    where={"id": presentation_id},
                    data={"pptx_file_path": pptx_file_path, "status": "exported"},
                    include={"slides": True, "speaker_notes": True},
                )
                if row:
                    return self._to_record_from_prisma(row)
            except Exception:
                pass

        items = self._read()
        for item in items:
            if item.get("id") == presentation_id:
                if user_id and item.get("user_id") != user_id:
                    return None
                item["pptx_file_path"] = pptx_file_path
                self._write(items)
                return PresentationRecord.model_validate(item)
        return None

    def regenerate_presentation(self, presentation_id: str, user_id: str | None = None) -> PresentationRecord | None:
        if self._prisma is not None:
            try:
                row = self._prisma.presentation.find_unique(where={"id": presentation_id})
                if row is None or (user_id and row.user_id != user_id):
                    return None
                row = self._prisma.presentation.update(
                    where={"id": presentation_id},
                    data={"status": "generated"},
                    include={"slides": True, "speaker_notes": True},
                )
                if row:
                    return self._to_record_from_prisma(row)
            except Exception:
                pass

        items = self._read()
        for item in items:
            if item.get("id") == presentation_id:
                if user_id and item.get("user_id") != user_id:
                    return None
                item["created_at"] = self._now_iso()
                self._write(items)
                return PresentationRecord.model_validate(item)
        return None

    def save_uploaded_file_metadata(self, metadata: UploadedFileMeta, status: str = "uploaded") -> None:
        if self._prisma is None:
            self._append_upload_record_json(metadata, status)
            return

        try:
            self._prisma.uploadedfile.upsert(
                where={"file_hash": metadata.file_hash},
                data={
                    "create": {
                        "filename": metadata.filename,
                        "content_type": metadata.content_type,
                        "extension": metadata.extension,
                        "size_bytes": metadata.size_bytes,
                        "file_hash": metadata.file_hash,
                        "parser_status": metadata.parser_status,
                        "word_count": metadata.word_count,
                        "character_count": metadata.character_count,
                        "preview_snippet": metadata.preview_snippet,
                        "status": status,
                    },
                    "update": {
                        "filename": metadata.filename,
                        "content_type": metadata.content_type,
                        "extension": metadata.extension,
                        "size_bytes": metadata.size_bytes,
                        "parser_status": metadata.parser_status,
                        "word_count": metadata.word_count,
                        "character_count": metadata.character_count,
                        "preview_snippet": metadata.preview_snippet,
                        "status": status,
                    },
                },
            )
        except Exception:
            self._append_upload_record_json(metadata, status)

    def _append_upload_record_json(self, metadata: UploadedFileMeta, status: str) -> None:
        """Local JSON log when PostgreSQL/Prisma is not configured."""
        entry = {
            **metadata.model_dump(),
            "status": status,
            "recorded_at": self._now_iso(),
        }
        with self._lock:
            raw = self.upload_records_path.read_text(encoding="utf-8")
            rows = json.loads(raw) if raw.strip() else []
            if not isinstance(rows, list):
                rows = []
            rows.append(entry)
            self.upload_records_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def save_revision_prompt(
        self,
        presentation_id: str,
        instruction: str,
        previous_outline: list[SlideOutlineItem],
        updated_outline: list[SlideOutlineItem],
        user_id: str | None = None,
    ) -> None:
        if self._prisma is None:
            return

        try:
            presentation = self._prisma.presentation.find_unique(where={"id": presentation_id})
            if presentation is None or (user_id and presentation.user_id != user_id):
                return
            self._prisma.revisionprompt.create(
                data={
                    "presentation_id": presentation_id,
                    "instruction": instruction,
                    "previous_outline": [item.model_dump() for item in previous_outline],
                    "updated_outline": [item.model_dump() for item in updated_outline],
                    "status": "revised",
                }
            )
            self._prisma.presentation.update(
                where={"id": presentation_id},
                data={"status": "revised"},
            )
        except Exception:
            pass

    def save_exported_file(self, presentation_id: str, export: ExportResult, user_id: str | None = None) -> None:
        if self._prisma is None:
            return

        try:
            presentation = self._prisma.presentation.find_unique(where={"id": presentation_id})
            if presentation is None or (user_id and presentation.user_id != user_id):
                return
            self._prisma.exportedfile.create(
                data={
                    "presentation_id": presentation_id,
                    "export_id": export.export_id,
                    "title": export.title,
                    "theme": export.theme,
                    "slide_count": export.slide_count,
                    "file_path": export.file_path,
                    "download_url": export.download_url,
                    "status": "ready",
                }
            )
        except Exception:
            pass

    def _to_record_from_prisma(self, row: Any) -> PresentationRecord:
        slides = sorted(getattr(row, "slides", []) or [], key=lambda s: s.slide_number)
        notes = sorted(getattr(row, "speaker_notes", []) or [], key=lambda n: n.slide_number)

        return PresentationRecord(
            id=row.id,
            title=row.title,
            uploaded_filename=row.uploaded_filename,
            user_id=row.user_id,
            persona=row.persona,
            theme=row.theme,
            created_at=row.created_at.isoformat(),
            outline=[
                SlideOutlineItem(
                    slide_number=slide.slide_number,
                    title=slide.title,
                    bullets=list(slide.bullets) if isinstance(slide.bullets, list) else [],
                )
                for slide in slides
            ],
            speaker_notes=[
                SpeakerNoteItem(slide_number=note.slide_number, note=note.note)
                for note in notes
            ],
            pptx_file_path=row.pptx_file_path,
        )

    def sign_up_user(self, payload: SignUpRequest) -> AuthUser | None:
        if self._prisma is not None:
            try:
                existing = self._prisma.user.find_unique(where={"email": payload.email.lower().strip()})
                if existing is not None:
                    return None
                created = self._prisma.user.create(
                    data={
                        "email": payload.email.lower().strip(),
                        "name": payload.name,
                        "password_hash": self._hash_password(payload.password),
                    }
                )
                return AuthUser(id=created.id, email=created.email, name=created.name)
            except Exception:
                return None

        email = payload.email.lower().strip()
        with self._lock:
            users = self._read_users_raw()
            if any(str(u.get("email", "")).lower() == email for u in users):
                return None
            new_user = {
                "id": str(uuid4()),
                "email": email,
                "name": payload.name,
                "password_hash": self._hash_password(payload.password),
            }
            users.append(new_user)
            self._write_users_raw(users)
        return AuthUser(id=new_user["id"], email=new_user["email"], name=new_user.get("name"))

    def authenticate_user(self, email: str, password: str) -> AuthUser | None:
        if self._prisma is not None:
            try:
                user = self._prisma.user.find_unique(where={"email": email.lower().strip()})
                if user is None:
                    return None
                if not self._verify_password(password, user.password_hash):
                    return None
                return AuthUser(id=user.id, email=user.email, name=user.name)
            except Exception:
                return None

        email_l = email.lower().strip()
        with self._lock:
            users = self._read_users_raw()
            for u in users:
                if str(u.get("email", "")).lower() != email_l:
                    continue
                if self._verify_password(password, str(u.get("password_hash", ""))):
                    return AuthUser(id=str(u["id"]), email=u["email"], name=u.get("name"))
        return None

    def _read_users_raw(self) -> list[dict]:
        raw = self.users_path.read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else []
        return data if isinstance(data, list) else []

    def _write_users_raw(self, users: list[dict]) -> None:
        self.users_path.write_text(json.dumps(users, indent=2), encoding="utf-8")

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        if not password_hash:
            return False
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except (ValueError, TypeError):
            return False

    @staticmethod
    def _can_use_prisma() -> bool:
        if Prisma is None:
            return False
        return bool(os.getenv("DATABASE_URL"))

    def _read(self) -> list[dict]:
        with self._lock:
            raw = self.db_path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else []
            return data if isinstance(data, list) else []

    def _write(self, data: list[dict]) -> None:
        with self._lock:
            self.db_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _parse_created_at(value: str) -> datetime:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.fromtimestamp(0, tz=timezone.utc)
