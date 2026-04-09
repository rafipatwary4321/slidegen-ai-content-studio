from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.listing import Listing


class TourismDetail(Base):
    __tablename__ = "tourism_details"

    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id", ondelete="CASCADE"), primary_key=True
    )
    has_guide: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    local_food_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    adventure_gear_rental: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(
        JSON, nullable=True
    )

    listing: Mapped[Listing] = relationship("Listing", back_populates="tourism_detail")
