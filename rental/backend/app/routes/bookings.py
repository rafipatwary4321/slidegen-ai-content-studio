from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.booking import Booking
from app.models.enums import BookingStatus, ListingCategory
from app.models.listing import Listing
from app.models.user import User
from app.schemas.bookings import (
    BookingConfirmResponse,
    BookingCreate,
    BookingRead,
    BookingSummaryResponse,
    TourismBookingCreate,
    TourismBookingResponse,
)
from app.services import booking_confirmation

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


def _validate_dates(check_in, check_out) -> None:
    if check_out <= check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="check_out must be after check_in",
        )


def _has_confirmed_overlap(db: Session, listing_id: int, check_in, check_out) -> bool:
    stmt = select(Booking.id).where(
        Booking.listing_id == listing_id,
        Booking.status == BookingStatus.CONFIRMED,
        and_(Booking.check_in < check_out, Booking.check_out > check_in),
    )
    return db.scalar(stmt) is not None


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)) -> Booking:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    listing = db.get(Listing, payload.listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    _validate_dates(payload.check_in, payload.check_out)

    if listing.category in {ListingCategory.SHORT_STAY, ListingCategory.TOURISM}:
        if _has_confirmed_overlap(db, listing.id, payload.check_in, payload.check_out):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This room is not available for the selected dates",
            )
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


def _gear_price_from_listing(listing: Listing, selected_gear: list[str]) -> Decimal:
    if not selected_gear:
        return Decimal("0.00")
    catalog = listing.gear_available or listing.available_gear or []
    if not isinstance(catalog, list):
        return Decimal("0.00")
    wanted = {g.strip().lower() for g in selected_gear if g and g.strip()}
    total = Decimal("0.00")
    for item in catalog:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip().lower()
        if not name or name not in wanted:
            continue
        try:
            total += Decimal(str(item.get("price", "0")))
        except Exception:  # noqa: BLE001
            continue
    return total


@router.post("/tourism", response_model=TourismBookingResponse, status_code=status.HTTP_201_CREATED)
def create_tourism_booking(
    payload: TourismBookingCreate,
    db: Session = Depends(get_db),
) -> TourismBookingResponse:
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    listing = db.get(Listing, payload.listing_id)
    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    if listing.category != ListingCategory.TOURISM:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing is not a Tourism category listing",
        )
    _validate_dates(payload.check_in, payload.check_out)
    if _has_confirmed_overlap(db, listing.id, payload.check_in, payload.check_out):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This tourism stay is already booked for the selected dates",
        )
    if listing.price_daily is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tourism listing is missing price_daily",
        )

    nights = (payload.check_out - payload.check_in).days
    base_price = Decimal(listing.price_daily) * Decimal(nights)
    guide_price = Decimal("0.00")
    if payload.include_guide:
        if not listing.has_guide:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Guide service is not available for this listing",
            )
        guide_daily = Decimal(listing.guide_price or Decimal("0.00"))
        guide_price = guide_daily * Decimal(nights)

    gear_price = _gear_price_from_listing(listing, payload.selected_gear)
    total_price = base_price + guide_price + gear_price

    booking = Booking(
        user_id=payload.user_id,
        listing_id=payload.listing_id,
        check_in=payload.check_in,
        check_out=payload.check_out,
        total_amount=total_price,
        status=BookingStatus.PENDING,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    return TourismBookingResponse(
        booking=booking,
        nights=nights,
        base_price=base_price,
        guide_price=guide_price,
        gear_price=gear_price,
        total_price=total_price,
    )


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
