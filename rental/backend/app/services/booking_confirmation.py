from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.booking import Booking
from app.models.enums import BookingStatus
from app.models.listing import Listing
from app.services.automation import (
    agreement_url_from_n8n_response,
    generate_digital_agreement_sync,
)
from app.services.digital_key import generate_unique_digital_key

logger = logging.getLogger(__name__)


def get_booking_for_flow(db: Session, booking_id: int) -> Booking | None:
    stmt = (
        select(Booking)
        .where(Booking.id == booking_id)
        .options(
            joinedload(Booking.user),
            joinedload(Booking.listing).joinedload(Listing.owner),
        )
    )
    return db.scalars(stmt).unique().one_or_none()


def confirm_booking(db: Session, booking_id: int) -> tuple[Booking, bool]:
    """
    Mark booking Confirmed, assign a unique 6-digit digital_key, and trigger n8n PDF flow.

    Returns `(booking, agreement_webhook_attempted)` where `agreement_webhook_attempted` is
    True only when this call transitioned Pending → Confirmed and invoked n8n.
    """
    booking = get_booking_for_flow(db, booking_id)
    if booking is None:
        raise ValueError("Booking not found")

    if booking.status == BookingStatus.COMPLETED:
        raise ValueError("Completed bookings cannot be confirmed")

    if booking.status == BookingStatus.CONFIRMED:
        if not booking.digital_key:
            booking.digital_key = generate_unique_digital_key(db)
            db.commit()
            db.refresh(booking)
        return booking, False

    booking.status = BookingStatus.CONFIRMED
    booking.digital_key = generate_unique_digital_key(db)
    db.commit()
    db.refresh(booking)

    listing = booking.listing
    guest = booking.user
    host = listing.owner

    try:
        n8n_result = generate_digital_agreement_sync(
            booking_id=booking.id,
            listing_id=listing.id,
            listing_title=listing.title,
            guest_email=guest.email,
            host_email=host.email,
            start_date=booking.check_in,
            end_date=booking.check_out,
            total_price=booking.total_amount,
            guest_name=guest.full_name,
            host_name=host.full_name,
            extra={"digital_key": booking.digital_key},
        )
        url = agreement_url_from_n8n_response(n8n_result)
        if url:
            booking.agreement_document_url = url
            db.commit()
            db.refresh(booking)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Digital agreement n8n call failed (booking still confirmed): %s", exc)

    return booking, True
