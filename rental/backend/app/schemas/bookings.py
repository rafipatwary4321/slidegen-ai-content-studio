from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import BookingStatus


class BookingBase(BaseModel):
    user_id: int
    listing_id: int
    check_in: date
    check_out: date
    total_amount: Decimal


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    check_in: date | None = None
    check_out: date | None = None
    total_amount: Decimal | None = None
    status: BookingStatus | None = None


class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    listing_id: int
    check_in: date
    check_out: date
    total_amount: Decimal
    status: BookingStatus
    digital_key: str | None = None
    agreement_document_url: str | None = None


class BookingSummaryResponse(BaseModel):
    booking_id: int
    status: str
    digital_key: str | None = Field(
        None,
        description="6-digit check-in code when status is Confirmed",
    )
    listing_title: str
    listing_latitude: float
    listing_longitude: float
    agreement_document_url: str | None = Field(
        None,
        description="PDF URL returned by n8n after agreement workflow",
    )
    check_in: date
    check_out: date
    total_amount: Decimal


class BookingConfirmResponse(BaseModel):
    summary: BookingSummaryResponse
    n8n_agreement_triggered: bool = True
