from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import NidStatus, UserRole

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.listing import Listing
    from app.models.lifestyle_profile import LifestyleProfile


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        default=UserRole.GUEST,
    )
    nid_status: Mapped[NidStatus] = mapped_column(
        SAEnum(NidStatus, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
        default=NidStatus.UNVERIFIED,
    )
    reputation_score: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False, default=Decimal("0")
    )

    listings: Mapped[list[Listing]] = relationship("Listing", back_populates="owner")
    bookings: Mapped[list[Booking]] = relationship("Booking", back_populates="user")
    lifestyle_profile: Mapped[LifestyleProfile | None] = relationship(
        "LifestyleProfile", back_populates="user", uselist=False
    )
