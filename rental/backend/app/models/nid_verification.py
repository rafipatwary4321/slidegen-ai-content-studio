from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class NIDVerification(Base):
    __tablename__ = "nid_verifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    image_path: Mapped[str] = mapped_column(String(2048), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="Pending")
    webhook_response: Mapped[str | None] = mapped_column(Text, nullable=True)
    webhook_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship("User")

