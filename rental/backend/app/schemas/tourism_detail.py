from typing import Any

from pydantic import BaseModel, ConfigDict


class TourismDetailBase(BaseModel):
    has_guide: bool = False
    local_food_available: bool = False
    adventure_gear_rental: dict[str, Any] | list[Any] | None = None


class TourismDetailCreate(TourismDetailBase):
    listing_id: int


class TourismDetailUpsert(TourismDetailBase):
    """Body for PUT /listings/{id}/tourism-detail."""


class TourismDetailUpdate(BaseModel):
    has_guide: bool | None = None
    local_food_available: bool | None = None
    adventure_gear_rental: dict[str, Any] | list[Any] | None = None


class TourismDetailRead(TourismDetailBase):
    model_config = ConfigDict(from_attributes=True)

    listing_id: int
