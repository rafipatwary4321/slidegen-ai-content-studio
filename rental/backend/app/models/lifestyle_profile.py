from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, Enum as SAEnum, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import SleepCycle

if TYPE_CHECKING:
    from app.models.user import User


class LifestyleProfile(Base):
    __tablename__ = "lifestyle_profiles"

    __table_args__ = (
        CheckConstraint(
            "cleanliness_score >= 1 AND cleanliness_score <= 10",
            name="ck_lifestyle_cleanliness_score",
        ),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    is_smoker: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    job_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    sleep_cycle: Mapped[SleepCycle] = mapped_column(
        SAEnum(SleepCycle, values_callable=lambda x: [e.value for e in x], native_enum=False),
        nullable=False,
    )
    cleanliness_score: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    user: Mapped[User] = relationship("User", back_populates="lifestyle_profile")
