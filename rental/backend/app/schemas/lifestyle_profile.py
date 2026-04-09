from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SleepCycle


class LifestyleProfileBase(BaseModel):
    is_smoker: bool = False
    job_type: str | None = Field(None, max_length=128)
    sleep_cycle: SleepCycle
    cleanliness_score: int = Field(..., ge=1, le=10)


class LifestyleProfileCreate(LifestyleProfileBase):
    user_id: int


class LifestyleProfileUpsert(LifestyleProfileBase):
    """Body for PUT /users/{id}/lifestyle-profile (user id is in the path)."""


class LifestyleProfileUpdate(BaseModel):
    is_smoker: bool | None = None
    job_type: str | None = Field(None, max_length=128)
    sleep_cycle: SleepCycle | None = None
    cleanliness_score: int | None = Field(None, ge=1, le=10)


class LifestyleProfileRead(LifestyleProfileBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
