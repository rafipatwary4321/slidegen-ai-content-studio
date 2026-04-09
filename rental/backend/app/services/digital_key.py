from __future__ import annotations

import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking


def generate_unique_digital_key(db: Session) -> str:
    """Cryptographic 6-digit code (100000–999999), unique among bookings with a digital_key set."""
    for _ in range(64):
        otp = str(secrets.randbelow(900_000) + 100_000)
        taken = db.scalar(select(Booking.id).where(Booking.digital_key == otp))
        if taken is None:
            return otp
    raise RuntimeError("Could not allocate a unique digital key")
