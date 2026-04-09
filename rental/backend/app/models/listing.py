from __future__ import annotations

from typing import TYPE_CHECKING, Any
from decimal import Decimal

from sqlalchemy import Enum as SAEnum, Float, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ListingCategory

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.tourism_detail import TourismDetail
    from app.models.user import User


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[ListingCategory] = mapped_column(
        SAEnum(ListingCategory, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        index=True,
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    price_daily: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    price_monthly: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    amenities: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSONB, nullable=True)

    owner: Mapped[User] = relationship("User", back_populates="listings")
    bookings: Mapped[list[Booking]] = relationship("Booking", back_populates="listing")
    tourism_detail: Mapped[TourismDetail | None] = relationship(
        "TourismDetail", back_populates="listing", uselist=False
    )
