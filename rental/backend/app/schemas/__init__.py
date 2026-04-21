"""Pydantic schemas for API request/response bodies."""

from app.schemas.bookings import (
    BookingConfirmResponse,
    BookingCreate,
    BookingRead,
    BookingSummaryResponse,
    TourismBookingCreate,
    TourismBookingResponse,
    BookingUpdate,
)
from app.schemas.listing import (
    ListingCreate,
    ListingRead,
    ListingSearchItem,
    ListingSearchResponse,
    ListingUpdate,
)
from app.schemas.listing_core import (
    BachelorListingCreate,
    CoreListingCreate,
    CoreListingRead,
    FamilyListingCreate,
    ListingLifestyleProfileCreate,
    ListingLifestyleProfileRead,
    ShortStayListingCreate,
    TourismListingCreate,
)
from app.schemas.lifestyle_profile import (
    LifestyleProfileCreate,
    LifestyleProfileRead,
    LifestyleProfileUpdate,
    LifestyleProfileUpsert,
)
from app.schemas.tourism_detail import (
    TourismDetailCreate,
    TourismDetailRead,
    TourismDetailUpdate,
    TourismDetailUpsert,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    "BookingConfirmResponse",
    "BookingCreate",
    "BookingRead",
    "BookingSummaryResponse",
    "TourismBookingCreate",
    "TourismBookingResponse",
    "BookingUpdate",
    "ListingCreate",
    "ListingRead",
    "ListingSearchItem",
    "ListingSearchResponse",
    "ListingUpdate",
    "ListingLifestyleProfileCreate",
    "ListingLifestyleProfileRead",
    "CoreListingCreate",
    "CoreListingRead",
    "BachelorListingCreate",
    "ShortStayListingCreate",
    "FamilyListingCreate",
    "TourismListingCreate",
    "LifestyleProfileCreate",
    "LifestyleProfileRead",
    "LifestyleProfileUpdate",
    "LifestyleProfileUpsert",
    "TourismDetailCreate",
    "TourismDetailRead",
    "TourismDetailUpdate",
    "TourismDetailUpsert",
    "UserCreate",
    "UserRead",
    "UserUpdate",
]
