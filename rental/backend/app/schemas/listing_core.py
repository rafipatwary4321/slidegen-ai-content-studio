from __future__ import annotations

from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field  # pylint: disable=import-error

from app.models.enums import ListingCategory, SleepCycle


class ListingLifestyleProfileCreate(BaseModel):
    is_smoker: bool = False
    job_type: str | None = Field(None, max_length=128)
    sleep_cycle: SleepCycle


class ListingLifestyleProfileRead(ListingLifestyleProfileCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CoreListingBase(BaseModel):
    title: str = Field(..., max_length=512)
    description: str | None = None
    price: Decimal = Field(..., gt=0)
    latitude: float
    longitude: float
    category: ListingCategory


class BachelorListingCreate(CoreListingBase):
    category: Literal[ListingCategory.BACHELOR] = ListingCategory.BACHELOR
    lifestyle_profile_id: int | None = None
    lifestyle_profile: ListingLifestyleProfileCreate | None = None


class ShortStayListingCreate(CoreListingBase):
    category: Literal[ListingCategory.SHORT_STAY] = ListingCategory.SHORT_STAY


class FamilyListingCreate(CoreListingBase):
    category: Literal[ListingCategory.FAMILY] = ListingCategory.FAMILY


class TourismListingCreate(CoreListingBase):
    category: Literal[ListingCategory.TOURISM] = ListingCategory.TOURISM
    has_guide: bool = False
    gear_available: list[Any] = Field(default_factory=list)


class CoreListingCreate(CoreListingBase):
    owner_id: int
    lifestyle_profile_id: int | None = None
    lifestyle_profile: ListingLifestyleProfileCreate | None = None
    has_guide: bool = False
    gear_available: list[Any] = Field(default_factory=list)


class CoreListingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    description: str | None
    price: Decimal | None
    latitude: float
    longitude: float
    category: ListingCategory
    lifestyle_profile_id: int | None
    match_score: float | None = None
    has_guide: bool
    gear_available: list[Any] | None

