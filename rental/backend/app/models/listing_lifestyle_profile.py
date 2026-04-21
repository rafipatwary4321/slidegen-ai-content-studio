from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import SleepCycle

if TYPE_CHECKING:
    from app.models.listing import Listing


class ListingLifestyleProfile(Base):
    """
    Bachelor-specific lifestyle profile attached to a listing.
    """

    __tablename__ = "listing_lifestyle_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_smoker: Mapped[bool] = mapped_column(nullable=False, default=False)
    job_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    sleep_cycle: Mapped[SleepCycle] = mapped_column(
        SAEnum(SleepCycle, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
    )

    listings: Mapped[list[Listing]] = relationship("Listing", back_populates="lifestyle_profile")

