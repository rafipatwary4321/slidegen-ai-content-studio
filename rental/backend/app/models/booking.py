from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import BookingStatus

if TYPE_CHECKING:
    from app.models.listing import Listing
    from app.models.user import User


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id", ondelete="CASCADE"), index=True)
    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        SAEnum(BookingStatus, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        default=BookingStatus.PENDING,
    )
    digital_key: Mapped[str | None] = mapped_column(
        String(6), unique=True, index=True, nullable=True
    )
    agreement_document_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    user: Mapped[User] = relationship("User", back_populates="bookings")
    listing: Mapped[Listing] = relationship("Listing", back_populates="bookings")
