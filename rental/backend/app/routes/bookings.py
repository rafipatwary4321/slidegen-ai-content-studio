from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.booking import Booking
from app.models.enums import BookingStatus
from app.models.listing import Listing
from app.models.user import User
from app.schemas.bookings import (
    BookingConfirmResponse,
    BookingCreate,
    BookingRead,
    BookingSummaryResponse,
)
from app.services import booking_confirmation

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)) -> Booking:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if db.get(Listing, payload.listing_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    booking = Booking(
        user_id=payload.user_id,
        listing_id=payload.listing_id,
        check_in=payload.check_in,
        check_out=payload.check_out,
        total_amount=payload.total_amount,
        status=BookingStatus.PENDING,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def _summary_from_booking(booking: Booking) -> BookingSummaryResponse:
    listing = booking.listing
    confirmed = booking.status == BookingStatus.CONFIRMED
    return BookingSummaryResponse(
        booking_id=booking.id,
        status=booking.status.value,
        digital_key=booking.digital_key if confirmed else None,
        listing_title=listing.title,
        listing_latitude=listing.latitude,
        listing_longitude=listing.longitude,
        agreement_document_url=booking.agreement_document_url if confirmed else None,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_amount=booking.total_amount,
    )


@router.get("/{booking_id}/summary", response_model=BookingSummaryResponse)
def get_booking_summary(booking_id: int, db: Session = Depends(get_db)) -> BookingSummaryResponse:
    booking = booking_confirmation.get_booking_for_flow(db, booking_id)
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return _summary_from_booking(booking)


@router.post("/{booking_id}/confirm", response_model=BookingConfirmResponse)
def confirm_booking(
    booking_id: int,
    db: Session = Depends(get_db),
) -> BookingConfirmResponse:
    try:
        booking, n8n_attempted = booking_confirmation.confirm_booking(db, booking_id)
    except ValueError as exc:
        detail = str(exc)
        code = (
            status.HTTP_404_NOT_FOUND
            if detail == "Booking not found"
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=detail) from exc

    return BookingConfirmResponse(
        summary=_summary_from_booking(booking),
        n8n_agreement_triggered=n8n_attempted,
    )
