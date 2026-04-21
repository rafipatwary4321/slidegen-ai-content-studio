from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ListingCategory


class ListingBase(BaseModel):
    title: str = Field(..., max_length=512)
    description: str | None = None
    category: ListingCategory
    latitude: float
    longitude: float
    price: Decimal | None = None
    price_daily: Decimal | None = None
    price_monthly: Decimal | None = None
    lifestyle_profile_id: int | None = None
    has_guide: bool = False
    gear_rental: list[Any] | None = None
    gear_available: list[Any] | None = None
    guide_price: Decimal | None = None
    available_gear: list[Any] | None = None
    amenities: dict[str, Any] | list[Any] | None = None


class ListingCreate(ListingBase):
    owner_id: int


class ListingUpdate(BaseModel):
    title: str | None = Field(None, max_length=512)
    description: str | None = None
    category: ListingCategory | None = None
    latitude: float | None = None
    longitude: float | None = None
    price_daily: Decimal | None = None
    price_monthly: Decimal | None = None
    has_guide: bool | None = None
    gear_rental: list[Any] | None = None
    guide_price: Decimal | None = None
    gear_available: list[Any] | None = None
    available_gear: list[Any] | None = None
    amenities: dict[str, Any] | list[Any] | None = None


class ListingRead(ListingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int


class ListingSearchItem(BaseModel):
    """Geo search result row."""

    id: int
    title: str
    category: str
    latitude: float
    longitude: float
    distance_km: float = Field(..., description="Great-circle distance from search point (km)")
    host_reputation_score: float = Field(
        ...,
        description="Owner's reputation_score (higher listed first at equal distance)",
    )
    compatibility_percent: float | None = Field(
        None,
        description="Bachelor-only: mean compatibility % vs mess (smoking, sleep, job)",
    )
    match_score: float | None = Field(
        None,
        description="Bachelor-only matchmaking score (0-100) based on smoking, sleep cycle and job type",
    )
    female_only_host: bool = Field(
        False,
        description="True when amenities include female_only (Safety Mode filter)",
    )
    price_daily: float | None = None
    price_monthly: float | None = None


class ListingSearchResponse(BaseModel):
    items: list[ListingSearchItem]


class ListingExploreItem(ListingRead):
    match_score: float | None = None
